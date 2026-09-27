# mirror.py — المرآة: قانون الإغلاق peel ∘ build = الهوية، مقيسًا على كل اللغة.
# البروتوكول المعلن (خمس خطوات، وبالعكس خطواتُ خمس):
#   البناءُ الحر يولّد · التقشيرُ يستعيد · الخلافُ يُسمّى · التسميةُ تُودَع · الإيداعُ يرفع الإجماع.
# الوجهان عملةٌ واحدة: build يحمل حمولةً (ما لا يُشتق) · peel يسترد المشتقَّ ·
#   والمرآة تثبتها عملةً واحدة: إن استردّ peelُّ ما بناه build استردادًا تامًّا فهو وجهٌ واحد،
#   وإن اختلفا فالخلافُ موضعُ إيداعٍ معلن.
# الإجماع = 1 − الحمولة/الخام — ولا يُرفع بتوسيع جداول بل بإيداعاتٍ تُنزّل الحمولة.
#
# ── حدُّ المرآة (يُقرأ قبل أيّ رقمٍ منها) ─────────────────────────────────────────
#   الهويةُ بالبناء **لا تصحّح البناء**: «الله ⟵ الل + ه» يجتاز المرآة كأيّ بناءٍ سليم،
#   فالانعكاسُ يثبت **القابليةَ** لا **الصواب**. فالمرآةُ نصفُ البرهان، ونصفُه الآخرُ
#   بوّاباتٌ صفرية. ولذلك يُشترط: لا إجماعَ نهائيًّا قبل أن تُعيد البواباتُ للمرآة ما تبنيه.
#
# ── التسجيلُ المسبق للمصادمة (قبل التشغيل) ────────────────────────────────────────
#   المُسلَّمُ ادّعى: هوية 77,801/77,801 = 1.0000 · خام 661,456 · مشتق 42,932 ·
#   إجماع 0.0649 · حمولة 0.9351 · خلافاتٌ مسمّاة {} — وتُصادَم كلُّها بـassert أدناه.
import sys, os, json, re
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from induction_engine import parse_verses

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
LIC = ("فتحة", "ضمة", "كسرة", "سكون")
SUF = ("هما", "كما", "هن", "هم", "كن", "كم", "نا", "ها", "ه", "ك", "ي")
GUARD_TA = "ة"
TEMPLATES = ["فعل", "فعلل", "فاعل", "أفعل", "تفعلل", "تفاعل", "انفعل", "افتعل", "افعلل", "استفعل"]

# أحكامُ المرآة مجمَّدةٌ بنصّها — الحسابُ الحيُّ لا يُنقَل وحدَه (سنّةُ SEALED_VERDICTS).
SEALED_MIRROR = dict(كلمات=77801, هوية=77801, خام=661456, مشتق=42932)


def rx(t):
    lg = {}; out = ""; idx = 0
    for ch in t:
        if ch in "فعل":
            lg.setdefault(ch, []).append(idx + 1); out += "(.)"; idx += 1
        else:
            out += ch
    return re.compile("^" + out + "$"), lg


RXS = [(t, *rx(t)) for t in TEMPLATES]


def build(w):
    """بناء حر: يقرر ما يُشتق ويحمل الباقي. يعيد الهيكلَ بحمولته."""
    sk = "".join(c for c, _ in w); st = [x for _, x in w]
    derived = 0
    # R4: اللاحق مشتق من الجدول
    stem, suf = sk, None
    if not sk.endswith(GUARD_TA):
        for s in SUF:
            if sk.endswith(s) and len(sk) - len(s) >= 2:
                stem, suf = sk[:-len(s)], s; derived += len(s); break
    # R5: ثوابت القالب مشتقة من معرّفه (ما ليس من الجذر)
    form = None; root = None
    for t, r, lg in RXS:
        m = r.match(stem)
        if m and all(len(set(m.group(g) for g in gs)) == 1 for gs in lg.values()):
            form = t
            root = tuple(m.group(g) for g in lg["ف"]) + tuple(m.group(g) for g in lg["ع"]) \
                + tuple(m.group(g) for g in lg["ل"])
            fixed = len(stem) - len(set(root))
            derived += fixed; break
    # R4-صوتي: نون التنوين مشتقة من الحركة
    tw = sum(1 for x in st if x.startswith("تنوين"))
    derived += tw
    return dict(sk=sk, stem=stem, st=st, suf=suf, form=form, root=root,
                raw=len(sk) + len(st), derived=derived, tanwin=tw)


def peel(b):
    """تقشير: يسترد السطح من البناء. اللصقُ على **الجذع المخزَّن** لا على الأصل —
    وهذا موضعُ الخلل الذي كادت المرآةُ الأولى تكذب به: لصقٌ على الأصل أظهر
    18,546 «خلافًا» وهميًّا، فالمرآةُ تكشف عيبَ نفسِها قبل أن تكشف عيبَ اللغة."""
    sk = b["stem"]
    if b["suf"]:
        sk = sk + b["suf"]
    return sk




# ── الأسماءُ المقفاة: شاهدُ القلع الزائف، يُعَدّ ولا يُغيّر حكمًا ─────────────────
# المُسلَّمُ وضع لها كاشفًا مشروطًا بـ`form is None` — وقد **مات الكاشفُ صامتًا**:
# قالبُ «فعل» ثلاثةُ محارفَ حرّة، فهو يطابق كلَّ جذعٍ ثلاثيّ («الل» منه)، فلا يخلو
# `form` أبدًا في هذه المواضع، فخرجت القائمةُ فارغةً وقُرئت «لا قلعَ زائف». والعدُّ
# يقول غيرَ ذلك. فيُعزَل الكاشفُ عن القالب ويُعَدّ بالاسم — **عرضًا لا حكمًا**:
# البناءُ لا يتغيّر، والهويةُ لا تنقلب، والحمولةُ لا تُمَسّ؛ إنما يُسمّى ما تمرّره المرآة.
SEALED_NAMES = ("الله", "مالك", "الرحمن")


def main():
    verses = parse_verses(CORPUS)
    raw_t = der_t = 0; ident = 0; words = 0
    dis = Counter(); dis_ex = {}
    payloads = Counter(); state_units = 0
    forms = Counter(); form_zero = Counter(); fake = Counter()
    for v in verses:
        for w in v:
            words += 1
            b = build(w)
            raw_t += b["raw"]; der_t += b["derived"]; state_units += len(b["st"])
            rec = peel(b)
            if rec == b["sk"]:
                ident += 1
            else:
                dis["خلاف-الهوية"] += 1; dis_ex.setdefault("خلاف-الهوية", b["sk"])
            payloads[min(b["raw"] - b["derived"], 12)] += 1
            forms[b["form"]] += 1
            if b["form"] and len(b["stem"]) - len(set(b["root"])) == 0:
                form_zero[b["form"]] += 1
            if b["suf"] and b["sk"] in SEALED_NAMES:
                fake[f"{b['sk']}⟵{b['stem']}+{b['suf']}"] += 1
    cons = der_t / raw_t

    # ── المصادمةُ بفارق صفر: كلُّ رقمٍ في المُسلَّم يُصادَم، ولا يُنقَل حتى يمرّ ──
    assert words == SEALED_MIRROR["كلمات"], f"الكلمات {words}"
    assert ident == SEALED_MIRROR["هوية"], f"الهوية {ident}"
    assert raw_t == SEALED_MIRROR["خام"], f"الخام {raw_t}"
    assert der_t == SEALED_MIRROR["مشتق"], f"المشتق {der_t}"
    assert round(cons, 4) == 0.0649 and round(1 - cons, 4) == 0.9351, "الإجماع/الحمولة"
    assert not dis, f"خلافُ هويةٍ غيرُ متوقَّع: {dis_ex}"

    borne = raw_t - der_t
    R = dict(
        بروتوكول="بناء-حر-يولّد · تقشير-يستعيد · خلاف-يُسمّى · تسمية-تُودَع · إيداع-يرفع-الإجماع",
        قانون_الإغلاق="peel ∘ build = الهوية",
        هوية=f"{ident:,}/{words:,} = {ident/words:.4f}",
        خام=raw_t, مشتق=der_t, محمول=borne,
        إجماع=round(cons, 4), حمولة=round(1 - cons, 4),
        حمولة_بتوزيعها=dict(sorted(payloads.items())[:8]),
        خلافات_مسمّاة={k: {"عدد": n, "مثال": dis_ex.get(k, "")} for k, n in dis.most_common()},
        حاملُ_الحمولة=dict(الهيئة=state_units, من_الخام=round(state_units / raw_t, 4),
                           الرسم=raw_t - state_units),
        قلعٌ_زائفٌ_معدود=dict(عدد=sum(fake.values()), مواضع=dict(fake.most_common()),
                              ملاحظة=("كاشفُ المُسلَّم مات صامتًا لاشتراطه form is None، وقالبُ «فعل» "
                                      "يطابق كلَّ ثلاثيّ فلا يخلو form — فخرجت القائمةُ فارغةً. "
                                      "وهذا عدٌّ لا حكم: البناءُ والهويةُ والحمولةُ لم تُمَسّ.")),
        تغطيةُ_القوالب=dict(موزَّعة={(k or "بلا-قالب"): n for k, n in forms.most_common()},
                            بلا_قالب=forms[None],
                            تغطيةٌ_لا_تشتقّ=dict(form_zero.most_common()),
                            ملاحظة=("«فعل» ثلاثةُ محارفَ حرّة: تغطيتُه اسميةٌ، ومنها ما لا يشتقّ "
                                    "حرفًا واحدًا (fixed=0). فالتغطيةُ ليست اشتقاقًا.")),
        حدُّ_المرآة=("الهويةُ بالبناء لا تصحّح البناء: «الله ⟵ الل + ه» يجتاز المرآة كأيّ بناءٍ "
                     "سليم. فالانعكاسُ يثبت القابليةَ لا الصواب — والصحّةُ تُثبَت بالبوّابات الصفرية "
                     "لا بالمرآة. ولا إجماعَ نهائيًّا قبل أن تُعيد البواباتُ للمرآة ما تبنيه."),
        إيداعات_مرشحة=[
            "R3 نداء الاجتماع (ترخيص مشترك) — يشتدّ على حمولة الهيئة وهي نصفُ الخام",
            "حارس الأسماء المقفاة — معدودٌ بالاسم أعلاه، وكاشفُه بوّابةٌ لا مرآة",
            "باب المشارك والمصدر في R5 — يفكّ تغطيةَ القالب الحرفية",
        ])

    print(f"قانون الإغلاق: peel∘build = الهوية — متحققة في {ident/words:.4f} ({ident:,}/{words:,})")
    print(f"الخام {raw_t:,} · المشتق {der_t:,} · المحمول {borne:,} · الإجماع {cons:.4f} · الحمولة {1-cons:.4f}")
    print(f"حاملُ الحمولة الأكبر: الهيئةُ {state_units:,} = {state_units/raw_t:.4f} من الخام · الرسمُ {raw_t-state_units:,}")
    print("الخلافاتُ المسمّاة:", dict(dis) or "{} — الهويةُ تامّة")
    print(f"قلعٌ زائفٌ معدود: {sum(fake.values())} — {dict(fake)}")
    print(f"  (كاشفُ المُسلَّم كان ميتًا: «فعل» يطابق كلَّ ثلاثيّ فلا يخلو form — فقُرئت القائمةُ الفارغة «لا قلع»)")
    print(f"تغطيةُ القوالب: بلا قالب {forms[None]:,} · «فعل» {forms['فعل']:,} منها {form_zero['فعل']:,} لا تشتقّ حرفًا")
    print("حدُّ المرآة:", R["حدُّ_المرآة"])
    return R


if __name__ == "__main__":
    R = main()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"المرآة": R}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {p}")
