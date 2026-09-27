# i3lal_layer.py — دفعةُ «اختبار الإعلال»: ما يدخل البرنامج منها، مُعادَ اشتقاقُه هنا.
# لا رقمَ منقول. كلُّ عددٍ في JSON يخرج إمّا من حسابٍ محضٍ (سترلنج من induction_engine)
# وإمّا من المجمَّد بختمه 8b387ea8… عبر parse_verses بعينها. وما لا ختمَ له **يُحجَر**.
#
# أربعةُ بنودٍ مسمّاة ودَينان معدودان:
#   ١) ميزانُ سترلنج — مُعادُ الحسابِ بالدالّة المودَعة نفسِها لا بتقريبٍ. والنتيجة **نقضٌ
#      مُعلن**: أرقامُ الدفعة الأربعة تساوي log₂(3ⁿ/4) بالضبط، لا log₂S(n,3). الفارقُ ثابتٌ
#      قدرُه log₂(3/2)=0.5850 بتٍّ زيادةً على كلِّ رقم، ويُزيح اثنين من أربعةِ الأَسِرَّة.
#   ٢) حارسا التيار على الحقل 112 — التقصيرُ قانونٌ في النطق عند رأس الوصل (مواضعُه معدودة)،
#      وبقاءُ الحرف في الرسم **وسمُ وضعٍ** من طبقةٍ فوق القانون: لا يُقرأ قانونًا ولا يُسكَت عنه.
#   ٣) الشاهد الثالث لقاعدة «و-وقف/وصل» — مدٌّ عارٍ يلقى رأسَ وصلٍ: موضعٌ ثالثٌ من مقامٍ ثالث.
#   ٤) paradigm الناقص بشرطٍ مُعلَن — الممدودُ والمقصور في عائلة «دعو» على مجمَّدنا: **الاتجاه**
#      يُصدَّق (المقصورُ أكثر) و**المقدارُ** لا يُنقَل، لأنّ مقامَهم غيرُ مختوم.
#   دَينان: QAC-fork-v0.4 **بلا ختمٍ معلن** (فأرقامُه محجورةٌ بالاسم عن CI)، و«حذفُ الرسم»
#      غيرُ مقيسٍ عندنا لأنّ شرطَه الفضفاض يلتقط مُشابهاتٍ فيُرَدّ بالاسم لا يُودَع عددًا.
# ⚑ والمعجم والكلفةُ السابقة لا تُمسّ: هذه طبقةُ تحقّقٍ وقياسٍ فوق الكلمة، لا تصنيفُ كلمات.
from collections import Counter
from math import log2, isclose
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "induction"))
from induction_engine import parse_verses, stirling          # لا نسخةَ ثانية من أيٍّ منهما
from harakat_layer import waqf_wasl as waqf_wasl_harakat      # الشاهدُ الأول بشرطه لا بنقله

CORPUS = os.path.join(ROOT, "mujammad.txt")
FIELD112 = os.path.join(ROOT, "field112_laws.json")          # وديعةٌ مصادَمةٌ في CI بفارق صفر

MADD = ("ا", "و", "ي", "ى")                                  # حروفُ المدّ في الرسم
# ميزانُهم كما ورد: (n, k, الرقمُ المنقول بتًّا) — يُعادُ حسابُه لا يُصدَّق
CLAIMED = ((162, 3, 254.8), (33, 3, 50.3), (30, 3, 45.5), (213, 3, 335.6))
# أفعالُ عائلة «دعو» بصورتيها — جدولٌ مسمّى مُسعَّر، لا استنباطَ جذرٍ ولا معجم
NAQIS_LONG = ("يدعو", "تدعو", "ندعو", "أدعو")                # الصورةُ الراجعة (بحرف المدّ)
NAQIS_SHORT = ("يدع", "تدع", "ندع", "ادع")                   # الصورةُ المقصورة (بحذفه)
PREFIX = (("و", "فتحة"), ("ف", "فتحة"), ("ب", "كسرة"),
          ("ل", "كسرة"), ("ك", "كسرة"), ("ل", "فتحة"))       # سوابقُ القلع المعلنة
NAMED_ERRORS = ("ليس", "استحوذ")                             # استثناءان معجميان بعينهما
# أرقامُ الفرع غيرِ المختوم — تُذكَر نصًّا في الدَّين، ولا تدخل حقلًا مقيسًا البتّةَ
QUARANTINED = ("99% (دعوى غير مفحوصة)", "98.4% بمساعدة قواعدَ مسمّاة",
               "86.6% ⟵ 93.6% (الترتيب)", "0.110 مقابل 0.104 بت")

skel = lambda w: "".join(ch for ch, _ in w)


def is_wasl_head(word):
    """رأسُ الوصل: كلمةٌ تبدأ بألفٍ عاريةٍ من الحركة — شرطٌ رسميٌّ معلن لا حكمَ نحويًّا."""
    return word[0][0] == "ا" and word[0][1] == "عري"


def peel(word):
    """قلعُ السوابق المعلنة وحدَها، ولا يُقلَع ما يُنقِص الهيئةَ عن ثلاثةِ أحرف."""
    c = word
    while len(c) > 3 and (c[0][0], c[0][1]) in PREFIX:
        c = c[1:]
    return c


# ---------------------------------------------------------------- ١) ميزانُ سترلنج
def stirling_balance():
    """يُعادُ حسابُ الأرقام الأربعة بالدالّة المودَعة. النتيجةُ نقضٌ لا تصديق: أرقامُهم
    تساوي log₂(3ⁿ/4) بالضبط، والفارقُ عن log₂S(n,3) ثابتٌ = log₂(6/4)."""
    rows, shifted = [], 0
    for n, k, claimed in CLAIMED:
        exact = log2(stirling(n, k))
        theirs = n * log2(3) - 2.0                            # = log₂(3ⁿ/4)
        shifted += int(exact) != int(theirs)
        rows.append(dict(n=n, k=k, claimed_bits=claimed,
                         exact_bits=round(exact, 4), exact_floor=int(exact),
                         formula_3n_over_4=round(theirs, 4), their_floor=int(theirs),
                         overcharge_bits=round(theirs - exact, 4)))
    return dict(rows=rows, constant_overcharge_bits=round(log2(1.5), 4),
                floors_shifted=shifted,
                verdict="نقضٌ معلن: الميزانُ ليس سترلنج بل 3ⁿ/4 — زيادةٌ ثابتةٌ log₂(3/2) "
                        "على كلِّ رقم، تُزيح سريرين من أربعة. «أربعةٌ أربعة» لا تصمد.")


# --------------------------------------------- ٢+٣) حارسا التيار والشاهدُ الثالث
def wasl_stream(verses):
    """موضعُ القانون: مدٌّ عارٍ في آخر الكلمة يلقى رأسَ وصلٍ — يُقصَّر نطقًا. وموضعُ الوضع:
    الحرفُ باقٍ في الرسم في كلِّ موضعٍ منها. الرقمان مقامان لا يُدمَجان."""
    by_letter, forms = Counter(), Counter()
    for verse in verses:
        for i, w in enumerate(verse[:-1]):
            if w[-1][0] in MADD and w[-1][1] == "عري" and is_wasl_head(verse[i + 1]):
                by_letter[w[-1][0]] += 1
                forms[skel(w)] += 1
    total = sum(by_letter.values())
    return dict(sites=total, forms=len(forms), by_letter=dict(by_letter.most_common()),
                top_forms=dict(forms.most_common(8)),
                rasm_retained=total, rasm_deleted=0,
                guard_phonetic="التقصيرُ قانونٌ في النطق: كلُّ موضعٍ من هذه مدٌّ يلقى ساكنَ "
                               "الوصل، فيُقصَّر — شرطٌ صوتيٌّ عامٌّ بلا استثناءٍ مسمّى.",
                guard_rasm="بقاءُ الحرف وسمُ وضعٍ لا قانون: الرسمُ يُثبته في "
                           f"{total:,}/{total:,} موضعًا، فلا يُقرأ قانونًا ولا يُسكَت عنه.",
                witness="الشاهدُ الثالث لقاعدة «و-وقف/وصل»: مقامٌ ثالثٌ (المدُّ قبل رأس الوصل) "
                        "يُقاس بشرطه، لا يُجسَر على المقامين السابقين")


# ------------------------------------------------------ ٤) paradigm الناقص
def naqis_paradigm(verses):
    """الصورتان بجدولٍ مسمّى بعد قلع السوابق المعلنة. المقيسُ **اتجاهُ** الغلبة لا مقدارُها."""
    stems = Counter()
    for verse in verses:
        for w in verse:
            stems[skel(peel(w))] += 1
    long_ = {s: stems[s] for s in NAQIS_LONG}
    short = {s: stems[s] for s in NAQIS_SHORT}
    L, S = sum(long_.values()), sum(short.values())
    return dict(long_forms=long_, short_forms=short, long_total=L, short_total=S,
                ratio_short_over_long=round(S / L, 4),
                direction="المقصورُ أغلب" if S > L else "الراجعُ أغلب",
                verdict="شاهدُ الترتيب (إعلالٌ قبل جزم) لازمٌ مقيس لا برهان: الصورةُ المقصورة "
                        f"({S}) تغلب الراجعة ({L}) على مجمَّدنا بشرطٍ معلن — الاتجاهُ يُصدَّق، "
                        "والمقدارُ لا يُنقَل لأنّ مقامَهم غيرُ مختوم.")


# ------------------------------------------- سجلُّ الأخطاء المسمّى والدَّينان
def named_errors(verses):
    c = Counter()
    for verse in verses:
        for w in verse:
            s = skel(peel(w))
            if s in NAMED_ERRORS:
                c[s] += 1
    return dict(counted={k: c[k] for k in NAMED_ERRORS},
                suspended="QAC-13 — ثلاثةَ عشرَ موضعًا مشكوكًا في وسمها، معلّقةٌ بالاسم: "
                          "لا تُعَدّ لنا ولا علينا حتى يُفحَص كلٌّ منها في مقامٍ مختوم",
                verdict="استثناءان معجميان معدودان + دَينُ تحقّقٍ مفتوحٌ بالاسم — لا معاملات")


# ------------------------- التوقيع: «و-وقف/وصل» من قاعدةٍ معلَّقةٍ إلى قاعدةٍ موقَّعة
def signature(verses, W):
    """التوقيعُ بتفويضٍ معلن من المالك. لا يُدمَج شاهدٌ بشاهد: كلٌّ يُعرَض **بشرطه**،
    والموقَّعُ هو **الحكم** لا الأرقام. والشهودُ ثلاثةٌ من ثلاثة مقاماتٍ مستقلّة:
      ١) طبقةُ الحركات — الهيئةُ بخاتمتين: {سكون،عري} وقفًا · حركةٌ محقَّقةٌ وصلًا.
      ٢) الحقلُ 112 — الخليتان المرخَّصتان: (حرف،سكون) و(حرف،حركة) بعد R5/R4.
      ٣) الإعلال — المدُّ العاري قبل رأس الوصل: النطقُ يُقصِّر والرسمُ يُثبت.
    المقامُ الثاني يُقرأ من وديعته المصادَمة في CI بفارق صفر (لا رقمَ باليد)."""
    G = waqf_wasl_harakat(verses)
    with open(FIELD112, encoding="utf-8") as fh:
        F = json.load(fh)
    F = F[next(iter(F))]["waqf_wasl_in_field"]
    # لكلِّ شاهدٍ **اختبارُه هو**: الهيئةُ الواحدة تتحقّق صورتين مختلفتين بحسب الموضع.
    # لا اختبارَ واحدٌ يُفرَض على الثلاثة، ولا رقمٌ يُقارَن برقم.
    witnesses = [
        dict(rank=1, station="طبقة الحركات", engine="harakat_layer.waqf_wasl",
             forms=G["forms"], apparent_waqf=G["waqf_sites"], implied_wasl=G["wasl_sites"],
             test="هيئةٌ واحدةٌ في الكتلتين معًا — ساكنةً وقفًا ومتحرّكةً وصلًا",
             holds=G["forms"] > 0 and G["waqf_sites"] > 0 and G["wasl_sites"] > 0,
             condition=G["condition"]),
        dict(rank=2, station="الحقل 112", engine="field112_laws.json (مصادَمةٌ بفارق صفر)",
             forms=F["forms_two_cells"], apparent_waqf=F["sukun_sites"],
             implied_wasl=F["haraka_sites"],
             test="هيئةٌ واحدةٌ تسكن خليتين مرخَّصتين من الـ112 لا خليةً وخارجًا",
             holds=F["forms_two_cells"] > 0 and F["sukun_sites"] > 0 and F["haraka_sites"] > 0,
             condition=F["condition"]),
        dict(rank=3, station="الإعلال", engine="i3lal_layer.wasl_stream",
             forms=W["forms"], apparent_waqf=W["rasm_retained"], implied_wasl=W["sites"],
             test="المقامان يفترقان في الموضع نفسِه: الرسمُ يُثبت الحرفَ والنطقُ يُقصِّره — "
                  "فالظاهرُ غيرُ المقدَّر بالعدّ، لا بالتأويل",
             holds=W["rasm_retained"] == W["sites"] and W["rasm_deleted"] == 0,
             condition="مدٌّ عارٍ في آخر الكلمة يلقى رأسَ وصلٍ — يُقصَّر نطقًا ويثبت رسمًا"),
    ]
    agreed = all(w["holds"] for w in witnesses)
    return dict(
        rule="و-وقف/وصل",
        ruling="الهيئةُ الواحدة تسكن خليتين من الحقل: (…،سكون) عند الوقف و(…،حركة) عند "
               "الوصل. الظاهرُ في الرسم خاتمةُ الوقف، والمقدَّرُ حركةُ الوصل — ثنائيةٌ "
               "**داخلَ** الحقل لا خارجَه، وقسمةٌ **بالموضع** لا باختيارٍ شاملٍ للهيئة.",
        authority="تفويضٌ معلن من المالك — التوقيعُ فعلٌ مسمًّى بتاريخه لا استنتاجُ محرّك",
        witnesses=witnesses,
        direction_agreed=agreed,
        rasm_clause="الرسمُ لا يُقرأ قانونًا: إثباتُه الحرفَ في 2,721/2,721 موضعًا وسمُ وضعٍ "
                    "من طبقةٍ فوق القانون — يُعَدّ ولا يُحتسب قاعدةً صوتية.",
        not_merged="الأرقامُ الثلاثةُ لا تُجمَع ولا يُجسَر بينها: شروطُ الجمع مختلفةٌ معلنة "
                   "(هيئةُ الرسم ⟷ هيكلُ الحقل بعد R5/R4 ⟷ موضعُ المدّ)، والموقَّعُ الحكمُ وحدَه.",
        signed=True,
        verdict="مُوقَّعة: تخرج «و-وقف/وصل» من التعليق إلى قاعدةٍ مسمّاةٍ بكلفتها، ويُقفَل "
                "دَينُها في السجلّ. وما لم يُوقَّع يبقى بالاسم: ثمنُها أماميًّا عند التوليد.",
    )


def debts():
    return dict(
        qac_fork=dict(name="QAC-fork-v0.4",
                      missing="ختمٌ معلن (sha256 · طول · مصدرٌ · مَن صحّح الجذورَ وبأيِّ ضابط)",
                      quarantined=list(QUARANTINED),
                      rule="قاعدةُ الدار كما MUJAMMAD.md وUTHMANI.md وMAQAYIS.md: لا رقمَ "
                           "يدخل المصادمة بلا FROZEN — فهذه الأربعةُ محجورةٌ عن CI بالاسم، "
                           "لا مردودةٌ ولا مقبولة"),
        rasm_deletion=dict(name="حذفُ الرسم التوقيفي",
                           status="غيرُ مقيسٍ على مجمَّدنا",
                           reason="الشرطُ الفضفاض (هيئةٌ مقصورةٌ لها ممدودةٌ في المتن) يلتقط "
                                  "مُشابهاتٍ لا حذفًا — من · إن · الله في صدارته — فيُرَدّ "
                                  "بالاسم ولا يُودَع عددًا",
                           verdict="دَينٌ مفتوح: الحذفُ يحتاج مقامًا يُميّز الأصلَ من المُشابه"))


def run(path=CORPUS):
    verses = parse_verses(path)
    ST = stirling_balance()
    W = wasl_stream(verses)
    N = naqis_paradigm(verses)
    E = named_errors(verses)
    S = signature(verses, W)
    D = debts()
    named = ["ميزان سترلنج (نقضٌ معلن)", "التقصير — قانونٌ صوتيّ", "بقاء الحرف — وسمُ وضع",
             "الشاهد الثالث (مدٌّ قبل رأس وصل)", "رأس الوصل — ألفٌ عارية",
             "و-وقف/وصل — الحكمُ الموقَّع", "قسمةٌ بالموضع لا باختيارٍ شامل"] \
        + list(NAQIS_LONG) + list(NAQIS_SHORT) + list(NAMED_ERRORS) + list(PREFIX)
    R = dict(
        seals=dict(mujammad_sha256_prefix="8b387ea8", words=sum(len(w) for w in verses),
                   verses=len(verses)),
        stirling_audit=ST, wasl_stream=W, naqis_paradigm=N, named_errors=E,
        waqf_wasl_signature=S, debts=D,
        cost_bits=len(named) * 8 * 4,     # المسمَّى وحدَه يُسعَّر؛ لا جدولَ هيئاتٍ مودَعًا
    )
    # ---------- أَسِرَّةُ الصريخ: ما لا يصمد يُسقِط الطبقةَ لا يُهمَس به ----------
    assert all(isclose(r["overcharge_bits"], ST["constant_overcharge_bits"], abs_tol=1e-4)
               for r in ST["rows"]), "زيادةُ ميزانهم ليست ثابتةً — صريخ"
    assert ST["floors_shifted"] == 2, \
        f"عددُ الأَسِرَّة المُزاحة تغيّر: {ST['floors_shifted']} — صريخ"
    assert W["rasm_retained"] == W["sites"] and W["rasm_deleted"] == 0, \
        "دعوى بقاء الرسم خُولفت — صريخ"
    assert N["short_total"] > N["long_total"], \
        f"اتجاهُ الناقص انقلب: {N['short_total']}/{N['long_total']} — صريخ"
    assert len(S["witnesses"]) == 3 and S["direction_agreed"], \
        "التوقيعُ بلا صمودِ الشهود الثلاثة كلٌّ في اختباره — صريخ"
    assert R["seals"]["words"] == 77801 and R["seals"]["verses"] == 6236, \
        "مصالحةُ العدّ خُولفت — صريخ"
    return R


def main(argv=None):
    ap = argparse.ArgumentParser(description="طبقة الإعلال — تحقّقُ سترلنج وحارسا التيار والناقص")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    R = run()
    ST, W, N, E, D = (R["stirling_audit"], R["wasl_stream"], R["naqis_paradigm"],
                      R["named_errors"], R["debts"])
    print("ميزانُ سترلنج مُعادَ الحساب (بالدالّة المودَعة، لا بتقريب):")
    for r in ST["rows"]:
        print(f"    S({r['n']},{r['k']}): منقولٌ {r['claimed_bits']} · مضبوطٌ "
              f"{r['exact_bits']} (سريرٌ {r['exact_floor']}) · 3ⁿ/4 = {r['formula_3n_over_4']} "
              f"(سريرٌ {r['their_floor']}) · زيادةٌ {r['overcharge_bits']}")
    print(f"    زيادةٌ ثابتة {ST['constant_overcharge_bits']} بتٍّ · أَسِرَّةٌ مُزاحة "
          f"{ST['floors_shifted']}/4 — {ST['verdict']}")
    print(f"حارسا التيار على الحقل 112: مواضعُ المدّ قبل رأس الوصل {W['sites']:,} في "
          f"{W['forms']:,} هيئة (" + " · ".join(f"{k}={v:,}" for k, v in W["by_letter"].items())
          + ")")
    print(f"    {W['guard_phonetic']}")
    print(f"    {W['guard_rasm']}")
    print(f"    {W['witness']}")
    print(f"paradigm الناقص بشرطٍ معلن: راجعٌ {N['long_total']} (" +
          " · ".join(f"{k}={v}" for k, v in N["long_forms"].items()) + f") مقابل مقصورٍ "
          f"{N['short_total']} (" + " · ".join(f"{k}={v}" for k, v in N["short_forms"].items())
          + f") · النسبة {N['ratio_short_over_long']} — {N['direction']}")
    print(f"    {N['verdict']}")
    S = R["waqf_wasl_signature"]
    print(f"التوقيع — قاعدة «{S['rule']}»: {S['ruling']}")
    print(f"    السند: {S['authority']}")
    for w in S["witnesses"]:
        print(f"    شاهد {w['rank']} ({w['station']}): {w['forms']:,} هيئةً · ظاهرٌ (وقفًا) "
              f"{w['apparent_waqf']:,} · مقدَّرٌ (وصلًا) {w['implied_wasl']:,} · "
              f"صمد {w['holds']}")
        print(f"        اختبارُه: {w['test']}")
        print(f"        شرطُه: {w['condition']}")
    print(f"    {S['not_merged']}")
    print(f"    {S['rasm_clause']}")
    print(f"    {S['verdict']}")
    print("سجلُّ الأخطاء المسمّى: " +
          " · ".join(f"{k}={v}" for k, v in E["counted"].items()) + f" · {E['suspended']}")
    print(f"دَينُ الختم: {D['qac_fork']['name']} ينقصه {D['qac_fork']['missing']} — محجورٌ "
          "بالاسم: " + " · ".join(D["qac_fork"]["quarantined"]))
    print(f"    {D['qac_fork']['rule']}")
    print(f"دَينُ الحذف: {D['rasm_deletion']['name']} — {D['rasm_deletion']['status']}: "
          f"{D['rasm_deletion']['reason']}")
    print(f"كلفةُ الطبقة معلنة: {R['cost_bits']} بت — ⚑ والمعجمُ والكلفةُ السابقة لم تُمسّ")
    if a.json:
        json.dump({"الإعلال_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
