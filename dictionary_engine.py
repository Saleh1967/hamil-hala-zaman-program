# dictionary_engine.py — المعجم v0: أول حلقة {ث/ع} بقواعد مبنيٍّ معلنة، من الصفر.
# الانضباط: كل موضعٍ إما مصنَّفٌ بقاعدةٍ مسمّاة أو ⚑ — لا افتراضيَّ صامت.
# القواعد المعلنة (وراثة باسمها من برنامج hamil):
#   ح-شدة: أوّل زوج الشدة سكونٌ مبنيٌّ (R5-أول)
#   ح-جار: ب/ل/ك الملتصقة بكسرة مبنيٌّ اتصالٌ لا إعراب
#   ع-تبدل: سند خاتمة الهيكل يتبدّل على المجمَّد (سندان فأكثر)
#   ث-وحدة: سندٌ واحد وعلامةٌ محقَّقة
#   ز-مزاح: تنوين فتح على ما قبل الخاتمة وخاتمةٌ عارية ا/ى
#   ق-فراغ: خاتمةٌ عاريةٌ بلا تنوينٍ مزاح
#   و٣-قلع: مطابقة قوالب I–XV بعد قلع السوابق المعلنة (awzan_engine — القوالب من T بعينها)
from collections import Counter, defaultdict
from math import log2
import json, os, sys

_INDUCTION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "induction")
assert os.path.isfile(os.path.join(_INDUCTION, "induction_engine.py")), \
    "محرّك الاستقراء غائبٌ عن induction/ — لا استيراد صامت"
sys.path.insert(0, _INDUCTION)
from induction_engine import parse_verses, GATES5  # عائلة الجذر الواحد

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")

def skel_of(word):
    return "".join(ch for ch, _ in word)

def classify_word(word, sup):
    """الأولوية المعلنة: ز ثم ق ثم ع(تبدّل) ثم ث(وحدة) — كلها قواعد مسمّاة."""
    if len(word) >= 2 and word[-2][1] == "تنوين فتح" and word[-1][0] in ("ا", "ى") and word[-1][1] == "عري":
        return "ز", "ز-مزاح"
    if word[-1][1] == "عري":
        return "ق", "ق-فراغ"
    return ("ع", "ع-تبدل") if len(sup[skel_of(word)]) >= 2 else ("ث", "ث-وحدة")

def mabni_loci(word):
    """مواضع المبني المعلنة السطحية — تغطيةٌ محسوبة لا ادّعاءُ تصنيفٍ كامل."""
    loc = []
    for i, (ch, st) in enumerate(word):
        if ch in "بل" and i + 1 < len(word) and word[i + 1][1] in ("ضمة", "سكون") and st == "كسرة":
            loc.append("ح-جار-ملتصق")  # بِ/لِ + ساكن: جارٌّ ملتصق مبنيّ
    return loc

def has_shadda(word, raw):
    return "ح-شدة" if "ّ" in raw else None

def awzan_cover(path, verses, sup):
    """تغطية الأوزان (و٣-قلع) على المعلَّق ث+ع — تُحسب هنا بالمحرّك نفسه، لا برقمٍ منقول."""
    import awzan_engine as AZ
    rich = AZ.tokenize_rich(path, verses)
    matched = shadda_ovl = 0
    for va, vb in zip(verses, rich):
        for wa, wb in zip(va, vb):
            if classify_word(wa, sup)[0] not in ("ث", "ع"):
                continue
            if AZ.hit(wb, "و٣-قلع") is not None:
                matched += 1
                shadda_ovl += any(d for _, _, d in wb)
    return matched, shadda_ovl, sum(len(t) for t in AZ.T.values()) * 8 + len(AZ.PREFIX) * 8 * 4


def run(path=CORPUS):
    verses = parse_verses(path)
    # العبور الأول: سندو الخواتم لكل هيكل (مقيس على الهياكل لا الكلمات)
    sup = defaultdict(Counter)
    toks = []
    for words in verses:
        ws = []
        for w in words:
            sup[skel_of(w)][w[-1][1]] += 1
            ws.append(w)
        toks.append(ws)
    assert len(sup) == 14870, "بصمة الهياكل خُالفت — صريخ"
    cnt, q_split, rule_cov = Counter(), Counter(), Counter()
    mabni_words = 0
    Nw = 0
    for ws in toks:
        for w in ws:
            Nw += 1
            k, rule = classify_word(w, sup)
            cnt[k] += 1
            rule_cov[rule] += 1
            if k == "ق":
                q_split[w[-1][0]] += 1
            if mabni_loci(w):
                mabni_words += 1
    z_chk = cnt["ز"]
    assert Nw == 77801 and z_chk == 3153, f"مصالحة hamil خُالفت: Nw={Nw} ز={z_chk} — صريخ"
    # تغطية القواعد المعلنة: الشدة في النص الخام (لا توسيع R5 هنا — هذا v0 السطحي)
    raw_words = 0; shadda_words = 0
    blob = open(path, encoding="utf-8").read()
    for ln in blob.splitlines():
        if not ln.strip():
            continue
        for w in ln.split(" "):
            if w.strip():
                raw_words += 1
                if "ّ" in w:
                    shadda_words += 1
    n_var = sum(1 for c in sup.values() if len(c) >= 2)
    sup_states = Counter()
    for c in sup.values():
        if len(c) >= 2:
            for st in c:
                sup_states[st] += 1
    awzan_words, awzan_shadda, awzan_bits = awzan_cover(path, verses, sup)
    awzan_gain = awzan_words - awzan_shadda          # الجديدُ وحده: ما لم تغطّه ح-شدة
    return dict(Nw=Nw, cnt=dict(cnt), z=z_chk, q_split=dict(q_split),
                skeletons=len(sup), n_var=n_var, sup_states=dict(sup_states),
                coverage=dict(raw_words=raw_words, shadda_words=shadda_words,
                              jar_mabni_words=mabni_words,
                              awzan_words=awzan_words, awzan_gain=awzan_gain,
                              scream=raw_words - shadda_words - awzan_gain),  # ⚑ المتبقّي بلا قاعدة
                rules_cost_bits=len(["ز-مزاح", "ق-فراغ", "ع-تبدل", "ث-وحدة",
                                     "ح-شدة", "ح-جار-ملتصق"]) * 8 * 4 + awzan_bits)

def main():
    R = run()
    out = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    H = -sum(v / R["Nw"] * log2(v / R["Nw"]) for v in R["cnt"].values())
    print(f"المعجم v0 — كلمات {R['Nw']:,} · هياكل {R['skeletons']:,} (متبدّلة {R['n_var']:,}) | "
          f"ث={R['cnt']['ث']:,} · ع={R['cnt']['ع']:,} · ز={R['cnt']['ز']:,} · ق={R['cnt']['ق']:,} | H(صنف)={H:.4f}")
    print(f"حسم «ق» بخواتمه: " + " · ".join(f"{k}={v:,}" for k, v in sorted(R["q_split"].items(), key=lambda kv: -kv[1])))
    print(f"تغطية المبني السطحية: شدّة {R['coverage']['shadda_words']:,} كلمة · جار ملتصق {R['coverage']['jar_mabni_words']:,} · "
          f"أوزان {R['coverage']['awzan_words']:,} (جديدها {R['coverage']['awzan_gain']:,}) · "
          f"⚑ المتبقّي {R['coverage']['scream']:,} (لا قاعدة سطحية له — دَين المعجم الكامل)")
    print(f"كلفة القواعد الست + جدول الأوزان معلنة: {R['rules_cost_bits']} بت — تُخصم من أي ربحٍ يُبنى عليها")
    if out:
        json.dump({"المعجم_v0": R}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {out}")

if __name__ == "__main__":
    main()
