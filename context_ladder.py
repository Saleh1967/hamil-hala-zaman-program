# context_ladder.py — سلّم السياق end-to-end: استقراءٌ على استقراء، FOR التصريف المُعدٍ.
# الفراكتال ببنيّتين: داخل الكلمة (الهيئة) · بين الكلمات (الحاكم يُعدي خاتمة تابعه).
# ON = تيار الكلمات المُلخَّصة (طبقة الجذر الموروثة) · FOR = قناة العدوى: كم من إنتروبيا
# الخاتمة سياقيةٌ معلَّة بالحاكم وكم معجميةٌ أصيلة · ماركوف على التيار المركّب بمراتب 0–2.
import sys, os, json
from math import log2
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from induction_engine import parse_verses, gate, GATES5
from dictionary_engine import classify_word, skel_of

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
LIC = ("فتحة", "ضمة", "كسرة", "سكون")

def H(c):
    n = sum(c.values())
    return -sum(v / n * log2(v / n) for v in c.values() if v)

def Hcond(rows):
    by = defaultdict(Counter)
    for x, y in rows: by[x][y] += 1
    n = len(rows)
    return sum(sum(c.values()) / n * H(c) for c in by.values())

def main():
    verses = parse_verses(CORPUS)
    sup = defaultdict(Counter)
    for v in verses:
        for w in v:
            sup[skel_of(w)][w[-1][1]] += 1

    # ـــــ ١) قناة الوصل بين الكلمتين: حالة أولى ⟵ خاتمة سابقة (عدوى الاتصال)
    junction = Counter()
    for v in verses:
        for i in range(1, len(v)):
            a = v[i - 1][-1][1]; b = v[i][0][1]
            if a in LIC and b in LIC:
                junction[(a, b)] += 1
    Nj = sum(junction.values())
    H_junc = Hcond([(a, b) for (a, b), n in junction.items() for _ in range(n)])

    # ـــــ ٢) قناة العدوى التصريفية: خاتمة الكلمة ⟵ صنف الحاكم (بوّابة الكلمة السابقة)
    rows = []
    for v in verses:
        for i in range(1, len(v)):
            end = v[i][-1][1]
            if end not in LIC: continue
            rows.append((gate(v[i - 1]), end))
    H_end = H(Counter(e for _, e in rows))
    H_end_g = Hcond(rows)
    JARR_G = {"J"}; INNA_SKEL = {"ان", "أن", "انّ", "إن"}
    rows2 = []
    for v in verses:
        for i in range(1, len(v)):
            end = v[i][-1][1]
            if end not in LIC: continue
            psk = skel_of(v[i - 1])
            ctx = "إنّ" if psk in INNA_SKEL else ("جار" if psk in {"من","عن","على","الى","في"} else gate(v[i-1]))
            rows2.append((ctx, end))
    H_end_g2 = Hcond(rows2)
    inf = Counter(e for c, e in rows2 if c in ("جار", "إنّ"))
    inf_ctx = Counter(c for c, _ in rows2 if c in ("جار", "إنّ"))

    # ـــــ ٣) استقراء على استقراء: التيار المركّب (فئة الشكل × الخاتمة) عبر الكلمات
    # ON = مخرجات الجذر: صنفا الشكل (مطابق وزن/غير) من المعجم + الخاتمة
    comp = []
    for v in verses:
        for w in v:
            end = w[-1][1]
            ec = end if end in LIC else ("عري" if end == "عري" else "تنوين")
            fc = "مطابق" if classify_word(w, sup)[0] in ("ث", "ع") else "بناء"
            comp.append((fc, ec))
    pairs = list(zip(comp, comp[1:]))
    Hc0 = H(Counter(b for _, b in pairs))
    Hc1 = Hcond(pairs)
    Hc2 = Hcond([((pairs[i][0], pairs[i - 1][0][1] if i else "#"), pairs[i][1])
                 for i in range(1, len(pairs))])

    R = dict(
        قناة_الوصل=dict(أزواج=Nj, H=round(H_junc, 4),
                         تبعا_لكلمة=f"{H_junc:.3f} بت/وصلة"),
        قناة_العدوى=dict(صفوف=len(rows), H_الخاتمة=round(H_end, 4),
                          H_بالحاكم_بوابة=round(H_end_g, 4),
                          ربح_البوابة=round(H_end - H_end_g, 4),
                          H_بالحاكم_المعلن=round(H_end_g2, 4),
                          ربح_المعلن=round(H_end - H_end_g2, 4),
                          سياقية=round(H_end - H_end_g2, 4),
                          معجمية=round(H_end_g2, 4),
                          بعد_جار_إنّ=dict(inf), سياقات_جار_إنّ=dict(inf_ctx)),
        التيار_المركب=dict(حالات=len(set(comp)), H0=round(Hc0, 4), H1=round(Hc1, 4),
                            H2=round(Hc2, 4), ربح_الماركوف=round(Hc0 - Hc1, 4)),
    )
    print(f"١) الوصل: {Nj:,} وصلة · H(أولى|خاتمة سابقة) = {H_junc:.4f}")
    print(f"٢) العدوى: H(الخاتمة) = {H_end:.4f} · بالحاكم-بوابة {H_end_g:.4f} (ربح {H_end-H_end_g:.4f})"
          f" · بالمعلن {H_end_g2:.4f} (ربح {H_end-H_end_g2:.4f})")
    print(f"   العدوى بعد جار/إنّ: {dict(inf)} من {dict(inf_ctx)}")
    print(f"٣) التيار المركّب ({len(set(comp))} حالة): H0 {Hc0:.4f} · H1 {Hc1:.4f} · H2 {Hc2:.4f}"
          f" — ماركوف يربح {Hc0-Hc1:.4f} بت")
    return R

if __name__ == "__main__":
    R = main()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"سلم_السياق": R}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {p}")
