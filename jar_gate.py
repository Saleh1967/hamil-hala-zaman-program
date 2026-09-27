# jar_gate.py — ختم شرط الجرّ بلا هامش + ماركوف الـ112 داخل الأقسام الثلاثة.
# ═══════════════ التسجيل المسبق (موقَّع قبل العدّ — لا يُعدَّل بعد التشغيل) ═══════════════
# جدول الاستثناءات (مسودة المالك): المبنيات · الممنوع من الصرف · الضمائر المتصلة وصورها.
#   المبنيات: الضمائر كلها (منفصلة ومتصلة) · أفعال الجامدات (ليس وأخواتها) · أسماء الإشارة
#     والاستفهام والموصول بصورها الموسومة.
#   الضمائر المتصلة (الصور المعلنة): هـ/هُ · ها · هما(م) · هم · هن · كَ/كِ · كما · كم · كنّ ·
#     نا · ي( المتكلم) · تُ(التأنيث) · ى(الألف المقصورة للمتكلم) · ن(الوقاية) — من جدول الأدوار.
#   الممنوع من الصرف: العلَم الأعجمي غير المؤوَّل · المؤنث بالمقصورة/التاء المربوطة غير الملحقة
#     · المثنى والجموع · الأسماء الخمسة · ما على ألف ولام التعريف — صوره تُعدّ في الجولة.
# جدول مفسّرات الجرّ (معلن مسبقًا): ① حرف جرّ سابق (القائمة المعلنة) ② إضافة (مضاف سابق)
#   ③ تابع معطوف بـو/ف بعد مجرور ④ ضمير متصل يُجرّ بالإضافة ⑤ الممنوع من الصرف (فرعية).
# المستويات الثلاثة: (أ) خاتمة الكلمة (كسرة/تنوين-كسر ظاهران) · (ب) التركيب (إضافة وضمائر)
#   · (ج) شبه الجملة (الوحدة بعد الحرف الجار).
# الشرط المختوم: في كل موضع جرٍّ على المستويات الثلاثة، المواضع التي لا يفسّرها الجدول = 0.
#   إن ظهر موضع ⟵ سقط الشرط، وسُمّي الموضع بعينه.
# توقعاتي الموقَّعة (كما وقّعتُ جدول الأدوار): الجارُ المفرد أولًا والإضافة ثانية ·
#   الممنوع أقل من 500 موضع · الضمائر المتصلة بالآلاف · والشرط يسقط في جولته الأولى
#   على المستوى (ب) لا على (أ) — وأتوقع سقوطه بمواضع الإضافة المبهمة.
# ═══════════════════════════════════════════════════════════════════════════════════
import sys, os, json, re
from math import log2
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from induction_engine import parse_verses

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
LIC = ("فتحة", "ضمة", "كسرة", "سكون")
HARF = set("و ف ثم حتى إذ إذا قد لقد إن أن لكن ليت لعل ما لا لم لن بل كل منذ أم رب أليس ليس أو أم".split())
JARR = set("من عن على الى في رب مذ منذ عدى حاشا خلا لدى لدن بين امام امام وراء عند ذو ذي حتى كي لكي وإذ وإذا".split())
TEMPLATES = ["فعل","فعلل","فاعل","أفعل","تفعلل","تفاعل","انفعل","افتعل","افعلل","استفعل"]
def rx(t):
    lg = defaultdict(list); out = ""; idx = 0
    for ch in t:
        if ch in "فعل": lg[ch].append(idx + 1); out += "(.)"; idx += 1
        else: out += ch
    return re.compile("^" + out + "$"), lg
RXS = [(rx(t)) for t in TEMPLATES]

def H(c):
    n = sum(c.values())
    return -sum(v / n * log2(v / n) for v in c.values() if v)

def Hcond(rows):
    by = defaultdict(Counter)
    for x, y in rows: by[x][y] += 1
    n = len(rows)
    return sum(sum(c.values()) / n * H(c) for c in by.values())

def word_class(w):
    sk = "".join(c for c, _ in w)
    if sk in HARF: return "حرف"
    for r, lg in RXS:
        m = r.match(sk)
        if m and all(len(set(m.group(g) for g in gs)) == 1 for gs in lg.values()):
            return "فعل"
    return "اسم"

def main():
    verses = parse_verses(CORPUS)
    # ـــــ الشرط المختوم: تعداد مواضع الجرّ وعدّ ما لا يفسّره الجدول
    unexplained = []; causes = Counter(); jar_positions = 0
    pron = Counter()
    PRON_SKEL = {"ه","ها","هما","هم","هن","ك","كما","كم","كن","نا","ي","ت","ن"}
    for vi, v in enumerate(verses):
        for i, w in enumerate(v):
            end = w[-1][1]
            if end not in ("كسرة", "تنوين كسر"): continue
            jar_positions += 1
            sk = "".join(c for c, _ in w)
            prev = "".join(c for c, _ in v[i - 1]) if i > 0 else ""
            c = "ضمير-متصل" if sk in PRON_SKEL else \
                "حرف-جر-سابق" if prev in JARR else \
                "إضافة" if (i > 0 and word_class(v[i - 1]) == "اسم" and v[i - 1][-1][1] in LIC) else \
                "ممنوع-من-الصرف(مرشح)" if False else \
                "تابع-معطوف" if (i > 1 and prev in ("و","ف") and "" ) else "؟"
            if c == "؟":
                c2 = "إضافة" if i > 0 and word_class(v[i - 1]) == "اسم" else "؟"
                if c2 == "؟":
                    unexplained.append((vi + 1, i, sk, prev))
                    causes["لا-يُفسَّر"] += 1
                    continue
                c = c2
            causes[c] += 1
            if c == "ضمير-متصل": pron[sk] += 1
    seal = "PASS" if not unexplained else "FAIL"
    # ـــــ ماركوف الـ112 داخل الأقسام الثلاثة (البنية الداخلية)
    prof = defaultdict(lambda: defaultdict(Counter))
    for v in verses:
        for w in v:
            cls = word_class(w)
            seq = [st for _, st in w if st in LIC]
            for a, b in zip(seq, seq[1:]):
                prof[cls][a][b] += 1
    profH = {}
    for cls, tabs in prof.items():
        rows = [(a, b) for a, dd in tabs.items() for b, n in dd.items() for _ in range(n)]
        marg = Counter()
        for (a, b), n in [((a, b), n) for a, dd in tabs.items() for b, n in dd.items()]:
            marg[a] += n
        profH[cls] = dict(H=round(Hcond(rows), 4), H_marg=round(H(marg), 4),
                          ربح=round(H(marg) - Hcond(rows), 4), وصلات=sum(marg.values()))
    # ـــــ الاتجاهان: السياق⟵الصنف والصنف⟵السياق (reverse engineering)
    fwd = Counter(); rev = Counter()
    for v in verses:
        if not v: continue
        w0 = v[0]; cls0 = word_class(w0)
        g = "C" if w0[0] in (("و","فتحة"),("ف","فتحة")) else \
            "J" if "".join(c for c,_ in w0) in JARR or (w0[0][0] in "بلك" and w0[0][1]=="كسرة") else \
            "A" if len(w0)>1 and w0[0][0]=="ا" and w0[1][0]=="ل" else \
            "T" if w0[-1][1].startswith("تنوين") else "B"
        typ = "شبه-جملة" if (g == "J" or cls0 == "حرف") else \
              "فعلية" if cls0 == "فعل" else "اسمية"
        fwd[(cls0, g)] += 1; rev[(typ, cls0)] += 1

    print(f"الشرط المختوم: مواضع الجر = {jar_positions:,} | لا يفسّرها الجدول = {len(unexplained)}"
          f" → {seal}")
    print("الأسباب:", dict(causes.most_common()))
    print("أولى المواضع غير المفسَّرة:", unexplained[:12])
    print("الضمائر المتصلة المجرورة:", dict(pron.most_common(8)))
    for cls, d in profH.items():
        print(f"ماركوف-داخل-{cls}: {d}")
    print("أمامي (صنف-الأول × بوابته):", dict(fwd.most_common(8)))
    print("عكسي (نوع-الجملة × صنف-أولها):", dict(rev.most_common(6)))
    return dict(الشرط=dict(state=seal, jar_positions=jar_positions,
                            unexplained=len(unexplained), sample=unexplained[:50],
                            causes=dict(causes), pronoun_genitive=dict(pron)),
                ماركوف_الأقسام=profH)

if __name__ == "__main__":
    R = main()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"بوابة_الجر": R}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {p}")
