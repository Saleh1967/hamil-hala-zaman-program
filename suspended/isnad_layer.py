# isnad_layer.py — دفعةُ «الإسناد»: ثلاثةُ مقاماتٍ تُقاس، ودَينٌ واحدٌ يُعلَن بالاسم.
# لا رقمَ منقول: كلُّ عددٍ يخرج من المجمَّد بختمه 8b387ea8… عبر parse_verses بعينها.
#
# ثلاثةُ مقاماتٍ **لا تُجمَع ولا يُجسَر بينها** — لكلٍّ شرطُه كما في شهود «و-وقف/وصل»:
#   ١) صفُّ «أنيت» الثمانيّ — الحروفُ الأربعة في أوّل الكلمة × حالتَي فتحة/ضمة. عدٌّ رسميٌّ
#      محضٌ: **لا دعوى معجمية** (لا يُقال «هذا فعلٌ مضارع»)، والمقيسُ شَغْلُ الخلايا الثماني.
#   ٢) صفُّ التاء الرباعيّ — التاءُ في آخر الكلمة بحالاتها الأربع. و**وسمُ وضعٍ لا قانون**:
#      العددُ سطحيٌّ يخلط تاءَ الإسناد بتاء الأصل (بيت) وبتاء الجمع المعرَبة (الصالحات)،
#      فيُعَدّ ولا يُسمّى إسنادًا — كما فُصل التقصيرُ الصوتيُّ عن بقاء الرسم.
#   ٣) الشرطُ المصحَّح — أوّلُ الكلمة من «أنيت» مضمومًا ثمّ ساكن، **على القسم الخالي من
#      اللواحق السطحية وحدَه**: فالموضعُ −2 ليس العينَ متى لحقت لاحقة (يؤمنون: واوُ الجماعة).
#      واللواحقُ تُستعمل **إخراجًا لا قلعًا**: لا يُدَّعى جذعٌ ولا يُشترى «حدُّ لاحقةٍ» بدَين.
#
# والدعويان **مقامان لا يُجمَعان في رقم**: «الضمّةُ تكشف الرباعيَّ أو المجهول» (مقامُ الحرف
# الأول) و«الكسرُ معلومٌ والفتحُ مجهول» (مقامُ العين) — كلٌّ يُعرَض بشرطه.
#
# الدَّينُ المعلن: **التاءُ المشتركة** — «تَكتُبُ» تصلح للمخاطَب وللغائبة، وغموضُها لا يُحَلّ
#   تحت الكلمة بالبناء: **T₃ محالةٌ إلى الجولة الثانية** (H(بوّابة|صنف) فوق حدٍّ موقوف).
# وما يستند إلى `c35956ef` أو «الجدول الموقَّع» أو مقام النبهاني: **T₃ بالاسم** — لا ختمَ
#   لأيٍّ منها في هذا المستودع، فلا يدخل عددًا (قاعدةُ AUDIT-188.md نفسُها).
# ⚑ والمعجم والكلفةُ السابقة لا تُمسّ: هذه طبقةُ عدٍّ رسميٍّ فوق الكلمة، لا تصنيفُ كلمات.
from collections import Counter
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "induction"))
from induction_engine import parse_verses                  # المجمَّد بختمه — لا نسخةَ ثانية

CORPUS = os.path.join(ROOT, "mujammad.txt")

ANYT = ("أ", "ن", "ي", "ت")          # حروفُ الصفّ الأربعة — الهمزةُ المرسومة «أ» وحدَها
ROW_STATES = ("فتحة", "ضمة")         # حالتا الصفّ: 4×2 = ثماني خلايا من الـ112
TA_STATES = ("ضمة", "فتحة", "كسرة", "سكون")                # صفُّ التاء الرباعيّ
SUFFIX = ("ون", "وا", "ين", "ان", "ن")                     # لواحقُ **إخراج** سطحيةٌ مسمّاة
NOUNISH_END = ("ة", "ى")             # معيارُ العيب: رسميٌّ لا معجميّ — يُعرَض بالعدّ

skel = lambda w: "".join(ch for ch, _ in w)


def has_suffix(word):
    """لاحقةٌ سطحيةٌ من القائمة المسمّاة. تُستعمل **إخراجًا** لا قلعًا: لا جذعَ يُدَّعى."""
    s = skel(word)
    return any(s.endswith(x) for x in SUFFIX)


# ------------------------------------------------- ١) صفُّ «أنيت» الثمانيّ
def anyt_row(verses):
    """عدٌّ رسميٌّ محضٌ على أوّل الكلمة: أربعةُ حروفٍ × حالتين. **لا دعوى معجمية**: لا يُقال
    عن موضعٍ إنّه فعلٌ مضارع، ولا عن حرفٍ إنّه حرفُ مضارعة — المقيسُ شَغْلُ الخلايا."""
    cells = Counter()
    for verse in verses:
        for w in verse:
            key = (w[0][0], w[0][1])
            if key[0] in ANYT and key[1] in ROW_STATES:
                cells[key] += 1
    rows = [dict(letter=l, state=s, count=cells[(l, s)], occupied=cells[(l, s)] > 0)
            for l in ANYT for s in ROW_STATES]
    return dict(
        cells=rows, cells_named=len(rows), cells_occupied=sum(r["occupied"] for r in rows),
        total=sum(r["count"] for r in rows),
        scope="أوّلُ الكلمة في المجمَّد — عدٌّ رسميٌّ بلا تصنيفٍ نحويّ",
        hamza_clause="الهمزةُ المرسومة «أ» وحدَها في الصفّ؛ و«ا» العاريةُ في أوّل الكلمة "
                     "(10,791 موضعًا) رأسُ وصلٍ لا همزةَ صفٍّ — تُستثنى بالرسم لا بالتأويل.",
        no_bridge="أسماءُ الخلايا من الحقل 112 (28×4)، والعدُّ على التفكيك الخام لا على "
                  "تفكيك الحقل بعد R5/R4 — مفرداتٌ مشتركةٌ لا جسرٌ بين مقامين.",
        verdict="ثماني خلايا مسمّاةٍ من الـ112، مشغولةٌ كلُّها بالعدّ — الصفُّ محقَّقٌ رسمًا، "
                "وما وراءه (أهو إسنادٌ أم أصلُ كلمة) لا تقوله هذه الطبقة.")


# ------------------------------------------------- ٢) صفُّ التاء الرباعيّ
def ta_row(verses):
    """التاءُ في آخر الكلمة بحالاتها الأربع. العددُ **سطحيٌّ معلنُ الخلط**: يقع فيه تاءُ
    الأصل (بيت) وتاءُ الجمع المعرَبة (الصالحات) مع ما قد يكون تاءَ إسناد — فيُعَدّ ولا
    يُسمّى إسنادًا. **وسمُ وضعٍ لا قانون**، على قاعدة «التقصيرُ قانونٌ وبقاءُ الرسم وضعٌ»."""
    states, forms = Counter(), {s: Counter() for s in TA_STATES}
    for verse in verses:
        for w in verse:
            if w[-1][0] == "ت" and w[-1][1] in TA_STATES:
                states[w[-1][1]] += 1
                forms[w[-1][1]][skel(w)] += 1
    rows = [dict(state=s, count=states[s], occupied=states[s] > 0,
                 top_forms=dict(forms[s].most_common(5))) for s in TA_STATES]
    return dict(
        cells=rows, cells_named=len(rows), cells_occupied=sum(r["occupied"] for r in rows),
        total=sum(r["count"] for r in rows),
        surface_clause="العددُ سطحيٌّ بالرسم: يخلط تاءَ الإسناد بتاء الأصل وبتاء الجمع "
                       "المعرَبة. فلا يُقرأ عددَ أشخاصٍ ولا يُنسَب إلى إسنادٍ — يُعَدّ وحسب.",
        status="وسمُ وضعٍ لا قانون",
        verdict="أربعُ خلايا من صفِّ التاء مشغولةٌ بالعدّ. وفصلُ تاء الإسناد عن تاء الأصل "
                "يحتاج معجمًا نحويًّا — دَينٌ قائمٌ بالاسم، لا يُقضى بعدٍّ سطحيّ.")


# ------------------------------------------------- ٣) الشرطُ المصحَّح
def corrected_condition(verses):
    """أوّلُ الكلمة من «أنيت» مضمومًا ثمّ ساكن. ثمّ **إخراجان معلنان** قبل قراءة العين:
       (أ) ما لحقته لاحقةٌ سطحيةٌ مسمّاة — لأنّ الموضع −2 عندها ليس العين؛
       (ب) ما خاتمتُه «ة» أو «ى» — عيبُ فُعْلة/فُعْلى، **ويُعرَض بالعدّ لا بالمثال**.
    والمصالحةُ محروسةٌ: المطابقُ = ذو اللاحقة + الخالي، والخالي = المُخرَج بالعيب + المقروء."""
    matched = [w for verse in verses for w in verse
               if len(w) >= 4 and w[0][0] in ANYT and w[0][1] == "ضمة" and w[1][1] == "سكون"]
    suffixed = [w for w in matched if has_suffix(w)]
    bare = [w for w in matched if not has_suffix(w)]
    nounish = [w for w in bare if skel(w)[-1] in NOUNISH_END]
    read = [w for w in bare if skel(w)[-1] not in NOUNISH_END]
    ayn = Counter(w[-2][1] for w in read)
    kasra, fatha = ayn["كسرة"], ayn["فتحة"]
    return dict(
        matched=len(matched), suffixed_excluded=len(suffixed), bare=len(bare),
        nounish_excluded=len(nounish), read=len(read),
        nounish_top=dict(Counter(skel(w) for w in nounish).most_common(8)),
        ayn_states=dict(ayn.most_common()),
        kasra=kasra, fatha=fatha,
        kasra_over_fatha=round(kasra / fatha, 4) if fatha else None,
        by_letter=dict(Counter(w[0][0] for w in read).most_common()),
        top_forms=dict(Counter(skel(w) for w in read).most_common(10)),
        suffix_clause="اللواحقُ الخمسُ المسمّاة تُستعمل **إخراجًا لا قلعًا**: لا جذعَ "
                      "يُدَّعى ولا «حدُّ لاحقةٍ» يُشترى بدَين — ثمنُه نصفُ العيّنة، يُدفَع معلنًا.",
        defect_clause="العيبُ المعلن **بالعدّ**: خاتمةُ «ة/ى» — فُعْلة/فُعْلى في صدارتها "
                      "(أخرى · نطفة · أسوة). ولا يلتقط الشرطُ «نُور» و«تُراب» أصلًا: ما "
                      "بعد أوّلهما مدٌّ **عارٍ** لا ساكن — فالعيبُ الأوّلُ يُعاد وصفُه لا يُكرَّر.",
        overcut_clause="والإخراجُ الثاني **يقطع زائدًا بالاعتراف**: يُخرِج معه مقصورًا قد "
                       "يكون مجهولًا (تتلى · يجزى · يؤتى) — قطعٌ سطحيٌّ معدودٌ لا مُنتقى، "
                       "ثمنُه معلنٌ وأثرُه في الفتحة وحدَها.",
        two_stations="الدعويان مقامان لا يُجمَعان في رقم: ضمّةُ الحرف الأوّل مقامٌ "
                     "(رباعيٌّ أو مجهول)، وحالُ العين مقامٌ آخر (كسرٌ معلومٌ · فتحٌ مجهول) — "
                     "وهذه الطبقةُ تعرض الثاني بشرطه ولا تُصدِّق الأوّلَ بغير عدٍّ يخصُّه.",
        verdict=f"على المقروء ({len(read)} موضعًا) تغلب الكسرةُ ({kasra}) الفتحةَ ({fatha}) "
                "عند العين. **الاتجاهُ وحدَه يُقرَأ**، ولا يُسمّى معلومًا ولا مجهولًا: "
                "التسميةُ حكمٌ صرفيٌّ يحتاج معجمًا، والعدُّ هنا رسميٌّ محض.")


def debts():
    return dict(
        shared_ta=dict(name="التاءُ المشتركة",
                       statement="«تَكتُبُ» تصلح للمخاطَب وللغائبة — غموضٌ لا يُحَلّ تحت "
                                 "الكلمة بالبناء، فقرينتُه فوقها",
                       ruling="T₃ — محالةٌ بالاسم إلى الجولة الثانية من المرحلة ٢ "
                              "(H(بوّابة|صنف) أماميًّا فوق حدٍّ موقوف)"),
        unsealed=dict(name="مقاماتٌ بلا ختم",
                      items=["ختم `c35956ef` (الإعرابُ بعاملٍ في لفظٍ آخر) — لا أثرَ له في "
                             "الشجرة", "«الجدولُ الموقَّع» بأدوار التاء — الموقَّعُ الوحيد في "
                             "السجلّ «و-وقف/وصل»، وليس فيه إسنادٌ ولا ضمائر",
                             "مقامُ النبهاني (ج٣) — غيرُ مودَعٍ ببصمةٍ وطولٍ ومصدر"],
                      ruling="T₃ بالاسم على قاعدة AUDIT-188.md: تُنقَل نصًّا موسومًا ولا "
                             "تُحوَّل عددًا حتى يُودَع ختمُ مقامِها"))


def run(path=CORPUS):
    verses = parse_verses(path)
    A, T, C, D = anyt_row(verses), ta_row(verses), corrected_condition(verses), debts()
    named = ["صفُّ أنيت الثمانيّ", "التاءُ الرباعيّة — وسمُ وضع", "الشرطُ المصحَّح",
             "الإخراجُ باللاحقة لا القلع", "عيبُ فُعْلة/فُعْلى بالعدّ",
             "القطعُ الزائد معترَفًا به", "مقاما الدعويين لا يُجمَعان",
             "التاءُ المشتركة — دَينٌ محال"] \
        + list(ANYT) + list(ROW_STATES) + list(TA_STATES) + list(SUFFIX) + list(NOUNISH_END)
    R = dict(
        seals=dict(mujammad_sha256_prefix="8b387ea8", words=sum(len(w) for w in verses),
                   verses=len(verses)),
        anyt_row=A, ta_row=T, corrected_condition=C, debts=D,
        cost_bits=len(named) * 8 * 4,
    )
    # ---------- أَسِرَّةُ الصريخ ----------
    assert A["cells_named"] == 8 and A["cells_occupied"] == 8, \
        f"صفُّ «أنيت» ليس ثمانيًا مشغولًا: {A['cells_occupied']}/{A['cells_named']} — صريخ"
    assert T["cells_named"] == 4 and T["cells_occupied"] == 4, \
        f"صفُّ التاء ليس رباعيًّا مشغولًا: {T['cells_occupied']}/{T['cells_named']} — صريخ"
    assert C["matched"] == C["suffixed_excluded"] + C["bare"], "مصالحةُ اللاحقة خُولفت — صريخ"
    assert C["bare"] == C["nounish_excluded"] + C["read"], "مصالحةُ العيب خُولفت — صريخ"
    assert C["kasra"] > C["fatha"], \
        f"اتجاهُ العين انقلب: {C['kasra']}/{C['fatha']} — صريخ"
    assert R["seals"]["words"] == 77801 and R["seals"]["verses"] == 6236, \
        "مصالحةُ العدّ خُولفت — صريخ"
    return R


def main(argv=None):
    ap = argparse.ArgumentParser(description="طبقة الإسناد — ثلاثةُ مقاماتٍ ودَينٌ معلن")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    R = run()
    A, T, C, D = R["anyt_row"], R["ta_row"], R["corrected_condition"], R["debts"]
    print(f"١) صفُّ «أنيت» الثمانيّ ({A['scope']}) — {A['total']:,} موضعًا:")
    for r in A["cells"]:
        print(f"    ({r['letter']}، {r['state']}): {r['count']:,}")
    print(f"    {A['hamza_clause']}")
    print(f"    {A['no_bridge']}")
    print(f"    {A['verdict']}")
    print(f"٢) صفُّ التاء الرباعيّ — {T['total']:,} موضعًا · {T['status']}:")
    for r in T["cells"]:
        print(f"    (ت، {r['state']}): {r['count']:,} — " +
              " · ".join(f"{k}={v}" for k, v in r["top_forms"].items()))
    print(f"    {T['surface_clause']}")
    print(f"    {T['verdict']}")
    print(f"٣) الشرطُ المصحَّح: مطابقٌ {C['matched']:,} = ذو لاحقةٍ {C['suffixed_excluded']:,} "
          f"+ خالٍ {C['bare']:,}؛ والخالي = عيبُ «ة/ى» {C['nounish_excluded']:,} + مقروءٌ "
          f"{C['read']:,}")
    print("    حالُ العين على المقروء: " +
          " · ".join(f"{k}={v}" for k, v in C["ayn_states"].items()) +
          f" · كسرة/فتحة = {C['kasra_over_fatha']}")
    print("    بالحرف: " + " · ".join(f"{k}={v}" for k, v in C["by_letter"].items()))
    print("    مُخرَجُ العيب: " + " · ".join(f"{k}={v}" for k, v in C["nounish_top"].items()))
    print(f"    {C['suffix_clause']}")
    print(f"    {C['defect_clause']}")
    print(f"    {C['overcut_clause']}")
    print(f"    {C['two_stations']}")
    print(f"    {C['verdict']}")
    print(f"الدَّينُ المعلن — {D['shared_ta']['name']}: {D['shared_ta']['statement']} · "
          f"{D['shared_ta']['ruling']}")
    print(f"{D['unsealed']['name']}: " + " · ".join(D["unsealed"]["items"]))
    print(f"    {D['unsealed']['ruling']}")
    print(f"كلفةُ الطبقة معلنة: {R['cost_bits']} بت — ⚑ والمعجمُ والكلفةُ السابقة لم تُمسّ")
    if a.json:
        json.dump({"الإسناد_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
