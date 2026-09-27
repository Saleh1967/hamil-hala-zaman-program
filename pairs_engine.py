# pairs_engine.py — الأزواج الدنيا: محاكاة المدلول من الدال وحده (مادة ثابتة × هيئة وحدة).
# الشرط المُسجَّل قبل العدّ (عرض المالك): الاختلاف يقع غالبًا في الوحدة الأخيرة (الإعراب)
# أو الوحدتين الأوليين (هيئة الفعل) — والفئة «وسط» فمُ الكسر المعلن لا مكبوته.
# تعريف معلن: زوج دنيا = هيئتان مرصودتان لنفس الهيكل الحرفي، تختلفان في حالة وحدةٍ واحدة.
# الاستقراء: ON = الأزواج نفسها · FOR = من موضع الاختلاف إلى جنس التغاير ·
# FROM = طبقات الجذر الموروثة (قوالب I · سندو الخواتم) لا من الصفر.
import sys, os, json
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from induction_engine import parse_verses

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")

def classify(pos, n):
    if pos == n - 1: return "خاتمة-الإعراب"
    if pos == 0: return "الوحدة-الأولى"
    if pos == 1: return "الوحدة-الثانية"
    return "وسط-كاسر"

def main():
    verses = parse_verses(CORPUS)
    families = defaultdict(Counter)      # هيكل ⟼ عدّ هيئاته المرصودة
    for v in verses:
        for w in v:
            sk = tuple(c for c, _ in w)
            families[sk][tuple(st for _, st in w)] += 1

    dist = Counter(); fams = 0; pairs = 0
    ex = defaultdict(list)
    voice = Counter(); triples = 0; triples_ex = []
    for sk, c in families.items():
        forms = sorted(c)
        if len(forms) < 2: continue
        fam_hit = False
        for i in range(len(forms)):
            for j in range(i + 1, len(forms)):
                a, b = forms[i], forms[j]
                if len(a) != len(sk) or len(b) != len(sk): continue
                diff = [k for k in range(len(a)) if a[k] != b[k]]
                if len(diff) != 1: continue
                pos = diff[0]; cls = classify(pos, len(a))
                dist[cls] += 1; pairs += 1; fam_hit = True
                if len(ex[cls]) < 6:
                    ex[cls].append(("".join(x[0]+y for x, y in zip(sk, a)),
                                    "".join(x[0]+y for x, y in zip(sk, b)), pos + 1))
                # FOR: جنس التغاير من الموضع والقالب
                if len(sk) == 3 and pos in (0, 1):        # ثلاثي، اختلاف في هيئة الفعل
                    ea, eb = a[1], b[1]
                    fa, fb = a[0], b[0]
                    if {a[pos], b[pos]} == {"فتحة", "ضمة"}:
                        if ea == eb == "كسرة": voice["علم/عُلم (عين كسرة)"] += 1
                        elif pos == 0 and fa == fb: voice["كرُم/كُرم (عين ضمة)"] += 1
                        else: voice["غير مصنّف-صوتي"] += 1
        if fam_hit: fams += 1
        # إعراب ثلاثي: ≥3 هيئات تختلف في الخاتمة وحده
        last_var = [f for f in forms if len(f) == len(sk)]
        groups = defaultdict(set)
        for f in last_var:
            groups[f[:-1]].add(f[-1])
        for pre, ends in groups.items():
            lic = [e for e in ends if e in ("فتحة", "ضمة", "كسرة")]
            if len(lic) >= 3:
                triples += 1
                if len(triples_ex) < 5:
                    triples_ex.append("".join(x[0] for x in sk[:-1]) + "{" + "/".join(lic) + "}")

    tot = sum(dist.values())
    out = dict(
        شرط_مسجل="غالبًا خاتمة أو أولاهما؛ وسط = كسر معلن",
        عائلات_ذات_أزواج=fams, أزواج=pairs,
        توزيع_الموضع={k: {"عدد": v, "حصة": round(v / tot, 4)} for k, v in dist.most_common()},
        أمثلة={k: v for k, v in ex.items()},
        FOR_أجناس_التغاير=dict(voice),
        إعراب_ثلاثي=dict(عائلات=triples, أمثلة=triples_ex),
    )
    print(f"عائلات لها أزواج دنيا: {fams:,} | الأزواج: {pairs:,}")
    for k, v in dist.most_common():
        print(f"  {k}: {v:,} ({v/tot:.1%})  {ex[k][:3]}")
    print(f"FOR — أجناس التغاير الصوتي: {dict(voice)}")
    print(f"إعراب ثلاثي (خاتمة فقط): {triples} عائلة — {triples_ex[:3]}")
    return out

if __name__ == "__main__":
    R = main()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"الأزواج_الدنيا": R}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {p}")
