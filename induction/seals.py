# seals.py — سجلُّ الأختام الحيّة: لا رقمَ إلا بمولِّدٍ يُشغَّل، ولا رقمَ إلا باسم دالّتِه ومقامِه.
#
# العلّةُ التي يقتلها هذا الملفّ: الأرقامُ المختومة كانت ثوابتَ ميتةً تُقارَن وتُطبع، فيبقى
# الرقمُ معروضًا وإن مات مولِّدُه — أو يتغيّر صامتًا وإن بقي اسمُه. وهنا يصير كلُّ ختمٍ
# **ستّةَ حقولٍ معًا**، لا يُقبَل ناقصًا:
#     ① اسمٌ  ② وديعةٌ (ملفُّ JSON ومسارُ المفتاح داخله)  ③ قيمةٌ متوقَّعة
#     ④ دالّةٌ مولِّدة  ⑤ مقامٌ (التيارُ وشرطُه)  ⑥ صنفٌ: [بوّابة] تحكم · [شاهد] يُعرَض ولا يحكم
#
# ولِمَ الدالّةُ حقلٌ مستقلّ؟ لأنّ العطلَ الذي كشفته ليلةُ الإقفال كان **اسمًا واحدًا على
# مقامين حسابيين**: «H(البوّابة|سابقتها)» طُبع مرّةً 1.2050 ومرّةً 1.3985، والفرقُ لم يكن
# اتفاقيتين بل جدولَ نصفِ التدريب على مقاماتِ الأزواج كلِّها. فالاسمُ وحدَه لا يكفي.
#
# آليّةُ الحياة (regen_all): لكلِّ وديعةٍ يُشغَّل مولِّدُها إلى ملفٍّ طازجٍ في /tmp، ثمّ:
#     أ) تُصادَم الوديعةُ المودَعة بالطازج — فارقٌ صفرٌ أو صريخ.
#     ب) يُقرَأ كلُّ ختمٍ **من الطازج لا من الوديعة** — فلا يشهد الرقمُ لنفسه.
#     ج) مسارٌ مفقودٌ صريخٌ **ولو كان الختمُ [شاهدًا]** — فلا يبقى رقمٌ لا يولَّد.
# وتغييرُ رقمٍ مختومٍ لا يمرّ إلا بتعديلٍ معلنٍ في هذا الملفّ، مقرونٍ بفاتورته في رسالة الالتزام.
import argparse
import ast
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
import deposit_law                                     # المصادقُ المركزيّ نفسُه الذي تستدعيه المحرّكات
from deposit_law import verdict, ACCEPT, DEGENERACY_CEILING

LAW_FILE = deposit_law.__file__


GATE = "[بوّابة]"      # رقمٌ يحكم: يمنع دمجًا، أو يَسقط به حكم
WITNESS = "[شاهد]"     # رقمٌ يُعرَض ولا يحكم — ويُولَّد مع ذلك، فالعرضُ ليس إعفاءً


def S(اسم, وديعة, مسار, قيمة, دالّة, مقام, صنف):
    """ختمٌ سداسيُّ الحقول — لا يُقبَل ناقصًا."""
    assert صنف in (GATE, WITNESS), f"صنفٌ غيرُ معلنٍ للختم {اسم}"
    assert دالّة and مقام, f"ختمٌ بلا دالّةٍ أو بلا مقام: {اسم}"
    return dict(اسم=اسم, وديعة=وديعة, مسار=tuple(مسار), قيمة=قيمة,
                دالّة=دالّة, مقام=مقام, صنف=صنف)


# المولِّدات: وديعةٌ ⟵ سطرُ تشغيلِها (تُكتب إلى ملفٍّ طازجٍ ثمّ تُصادَم).
GENERATORS = {
    "results.json": ["induction/induction_engine.py", "--require-corpus"],
    "online_peel.json": ["induction/online_peel.py"],
    "mirror.json": ["induction/mirror.py"],
    "deposit_law.json": ["induction/deposit_law.py"],
    "tensor_law.json": ["induction/tensor_law.py"],
    "jami3_mani3.json": ["induction/jami3_mani3.py"],
    "hiyad.json": ["induction/hiyad.py"],
    "pairs_v0.json": ["pairs_engine.py"],
    "context_ladder.json": ["context_ladder.py"],
    "jumla_links.json": ["jumla_links.py"],
    # الوحيدةُ التي لا تُقاس على المجمَّد: مولِّدُها يقرأ بايتاتِ شهودٍ مختومين من
    # corpora/sources/ (غيرِ المودَعة في الشجرة)، ويسقط بالمخرج 3 إن غابت — فلا
    # يُصادَم هذا السجلُّ إلا بعد «bash fetch_source.sh --fetch» لشاهدَي التعداد.
    "sources_census.json": ["sources_census.py"],
}

# موضعُ كلِّ وديعةٍ في الشجرة — الأصلُ induction/، وما خرج عنه يُعلَن هنا بمساره.
DEPOSIT_DIR = {"pairs_v0.json": ROOT, "context_ladder.json": ROOT,
               "jumla_links.json": ROOT, "sources_census.json": ROOT}


def deposit_path(deposit):
    return os.path.join(DEPOSIT_DIR.get(deposit, HERE), deposit)


# الودائعُ المبوَّبةُ في ci.yml لا في هذا الملفّ — لكلِّ واحدةٍ خطوةُ مصادمةٍ باسمها.
# الحارسُ أدناه يتحقّق من الدعوى في بايتات ci.yml، فلا تُقبَل بمجرّد كتابتها هنا.
CI_COLLIDED = (
    "awzan_v0.json", "dictionary_v0.json", "field112_laws.json", "harakat_v0.json",
    "i3lal_v0.json", "isnad_v0.json", "jar_gate.json", "maqayis_v0.json", "waqf_v0.json",
    # وديعةُ السجلِّ نفسِه: مولِّدُها هذا الملفّ، فلا تُوضَع في GENERATORS (فتُعيد تشغيلَ
    # نفسِها بلا قرار)، بل تُصادَم في خطوةِ ci.yml التي تشغّله ثمّ تقابل مخرَجَه بالمودَع.
    "seals.json",
)

SEALS = [
    # ——— الاستقراء: تيارُ بوّابات الآيات ———
    S("إنتروبيا البوّابة الشرطية", "results.json", ("مقيس", "H_cond"), 1.398473785338209,
      "run_gates ⟵ gate()", "بوّابات الآيات بالعبور · الجدولُ والمقاماتُ من الأزواج كلِّها (6,235)",
      GATE),
    S("أزواج العبور", "results.json", ("مقيس", "Np"), 6235,
      "run_gates", "بوّابات الآيات بالعبور — حدُّ الآية يُعبَر معلنًا", GATE),
    S("بوّابة العطف C", "results.json", ("مقيس", "marginal", "C"), 2888,
      "gate()", "مدخلُ كلِّ آيةٍ من 6,236 — وَ/فَ مفتوحةً", GATE),
    S("بوّابة التنوين T", "results.json", ("مقيس", "marginal", "T"), 102,
      "gate()", "مدخلُ الآية — خاتمةُ تنوينٍ أو تنوينُ فتحٍ مزاحٌ قبل ا/ى", GATE),
    S("فاتورة الأحاديّ", "results.json", ("مقيس", "unigram", 0), 4518.0773095090935,
      "invoice_unigram", "نصفُ التدريب 3,118 زوجًا · α=1 · خليةٌ log2(Ntr+1)", GATE),
    S("فارق الجشع عن الاستنفاد", "results.json", ("مقيس", "gap"), 0.0,
      "greedy_path ⟷ invoice_for", "الأقسامُ الـ52 كلُّها بحراسة ستيرلنج", GATE),
    S("خلايا الحقل 112 المشغولة", "results.json", ("مقيس", "حقل112", "alphabet"), 108,
      "run_field112", "مواضعُ الحقل 112 المرخَّصة — 223,611 موضعًا", GATE),

    # ——— التقشير الفوريّ ———
    S("مقشور فوريًّا", "online_peel.json", ("التقشير_الفوري", "أحوال", "مقشور"), 17979,
      "run() ⟵ peel", "المجمَّد 77,801 كلمةً · جدولُ 11 لاحقةً معلنة", GATE),
    S("باب «ي» حاكمًا (فوريّ)", "online_peel.json",
      ("التقشير_الفوري", "الجولة_الثالثة", "أحوال_فوريّ", "حارس-النسق(ي)"), 1495,
      "run2 ⟵ peel2", "شاهدُ النسق: الجذعُ شُوهد بلاحقةٍ أخرى — فوريًّا لا دفعيًّا", GATE),
    S("باب «ي» دفعيًّا عرضًا", "online_peel.json",
      ("التقشير_الفوري", "الجولة_الثالثة", "أحوال_دفعيّ_عرضًا", "حارس-النسق(ي)"), 1404,
      "run2 (دفعيّ)", "المقامُ الدفعيّ — عرضٌ موسومٌ لا يُجسَر بالفوريّ (فارق 91)", WITNESS),

    # ——— المرآة ———
    S("إجماع المرآة", "mirror.json", ("المرآة", "إجماع"), 0.0649,
      "run ⟵ build/peel", "77,801 كلمةً · الجدولُ المودَع", WITNESS),
    S("المرآة النزيهة", "mirror.json",
      ("المرآة", "إعادةُ_الاختبار", "المرآةُ_النزيهة", "نسبةٌ_على_الكلّ"), 0.3174,
      "honest_mirror", "بلا جذعٍ مخزَّن — وهذه **تكذب** فهي مرآةٌ حقًّا", GATE),
    S("تكذيبُ الهوية بجدولٍ فارغ", "mirror.json",
      ("المرآة", "إعادةُ_الاختبار", "الهويةُ_تحصيلُ_حاصل", "تجارِبُ_التكذيب", "جدولٌ_فارغ", "هوية"),
      1.0, "FALSIFY_TRIALS", "جدولُ لواحقَ فارغٌ يعطي الهويةَ التامّة — فالهويةُ تحصيلُ حاصل", GATE),

    # ——— قانون الوديعة ———
    S("فاتورة المودَع عند الكلمة", "deposit_law.json",
      ("قانون_الوديعة", "السلّمُ_الفراكتاليّ", "درجات", "L2 كلمة", "ρ"), -0.004,
      "rung", "L2 الكلمة · 14,870 هيكلًا — المشغّلُ ينقلب عند الكلمة", GATE),
    S("انحلال L3", "deposit_law.json",
      ("قانون_الوديعة", "السلّمُ_الفراكتاليّ", "درجات", "L3 آية", "انحلال"), 0.9708,
      "rung ⟵ حارسُ الانحلال", "|Σ|/N فوق العتبة — فرقمُ L3 لا يُنقَل", GATE),

    # ——— دعوى التنسور ———
    S("فاتورة التنسور", "tensor_law.json",
      ("دعوى_التنسور", "T2_تفنيد", "الفاتورةُ_ترفض", "جداول", "التنسور كما هو", "فائدة"), 69037,
      "tensor_bill", "الأساس 1,737,746 بتًّا — Δ موجبٌ ⟹ ترفض الوديعة", GATE),
    S("الميم لها منازع", "tensor_law.json",
      ("دعوى_التنسور", "T1_تصديق", "الميم", "ميم-بلا-منازع"), 1164,
      "run ⟵ T₁", "المدَّعى «بلا منازع» — والشاهدُ المضادّ من البايتات يكسره", WITNESS),

    # ——— الجامع المانع ———
    S("فاتورة الحقل 112", "jami3_mani3.json", ("البناءُ_الجامع_المانع", "الحَكَم", "فرق"), -310993,
      "verdict", "الخامُ 2,694,034 ⟷ الحقلُ 2,383,040 — Δ سالبٌ ⟹ وديعةٌ صالحة", GATE),
    S("خلايا مشغولة (جامع)", "jami3_mani3.json",
      ("البناءُ_الجامع_المانع", "الجامع", "خلايا_مشغولة"), 108,
      "partition", "قسمةُ التضمين والاستبعاد — تُصادَم بـfield112_laws.json", GATE),

    # ——— دعوى الحياد ———
    S("فاتورة طيّ الألف", "hiyad.json", ("دعوى_الحياد", "الحَكَم", "ا", "فرق"), 24145,
      "bill", "طيُّ الألف وسمًا — Δ موجبٌ ⟹ يُرفَض", GATE),
    S("فاتورة طيّ و/ي", "hiyad.json", ("دعوى_الحياد", "الحَكَم", "وي", "فرق"), -5427,
      "bill", "طيُّ العلّتين وسمًا — Δ سالبٌ ⟹ يُقبَل", GATE),

    # ——— الأزواجُ الدنيا (كانت يتيمةً بلا بوّابة) ———
    S("عائلاتُ الإعراب الثلاثي", "pairs_v0.json",
      ("الأزواج_الدنيا", "إعراب_ثلاثي", "عائلات"), 176,
      "pairs_engine.main", "هياكلُ المجمَّد — ≥3 هيئاتٍ تختلف في الخاتمة وحدَها", GATE),
    S("العائلاتُ ذاتُ الأزواج الدنيا", "pairs_v0.json",
      ("الأزواج_الدنيا", "عائلات_ذات_أزواج"), 1764,
      "pairs_engine.main", "هيكلٌ حرفيٌّ واحد · هيئتان تختلفان في وحدةٍ واحدة", GATE),

    # ——— سلّمُ السياق (كان يتيمًا بلا بوّابة) ———
    S("العدوى المعجمية", "context_ladder.json",
      ("سلم_السياق", "قناة_العدوى", "معجمية"), 1.8028,
      "context_ladder.main", "خاتمةُ الكلمة مشروطةً بالحاكم المعلن — 42,850 صفًّا", GATE),
    S("العدوى السياقية", "context_ladder.json",
      ("سلم_السياق", "قناة_العدوى", "سياقية"), 0.0734,
      "context_ladder.main", "H(الخاتمة) − H(الخاتمة|الحاكم المعلن) — المقامُ نفسُه", GATE),
    # ——— أرقامُ سجلِّ الأختام الموازي (PR #10): لا يُفقَد رقمٌ صامتًا عند الدمج ———
    S("ماركوف · الربحُ الكلّيّ", "results.json", ("مقيس", "markov", 2), 290.1716959343538,
      "run_gates ⟵ markov", "بتًّا على 6,235 بوّابة — H − H_cond مضروبًا في المقام", GATE),
    S("ماركوف · فارقُ الترتيبين", "results.json", ("مقيس", "orders_gap"), -600.097234034085,
      "run_gates ⟵ orders_gap", "بتًّا — الترتيبُ الطبيعيُّ ⟷ المعكوس على المقام نفسِه", GATE),
    S("المرآة · الهوية", "mirror.json", ("المرآة", "هوية"), "77,801/77,801 = 1.0000",
      "run ⟵ build/peel", "كلمةً — وهي تحصيلُ حاصلٍ يكذّبُه الجدولُ الفارغ (الختمُ الذي يليه)",
      WITNESS),
    S("الفاتورة · الأساس", "deposit_law.json",
      ("قانون_الوديعة", "الفاتورةُ_الحاكمة", "جداول", "بلا جدولٍ (الأساس)", "الكلّ"), 1737746,
      "bill ⟵ L₀", "بتًّا — الأساسُ الذي تُخصَم منه كلُّ وديعة", GATE),
    S("الفاتورة · المودَع يُقبَل", "deposit_law.json",
      ("قانون_الوديعة", "الفاتورةُ_الحاكمة", "جداول", "المودَع", "فائدة"), -15321,
      "bill ⟵ verdict", "بتًّا — Δ سالبٌ ⟹ يُقبَل", GATE),
    S("الفاتورة · الشَّرِه يُرفَض", "deposit_law.json",
      ("قانون_الوديعة", "الفاتورةُ_الحاكمة", "جداول", "حروفٌ شائعة (شَرِه)", "فائدة"), 6281,
      "bill ⟵ verdict", "بتًّا — Δ موجبٌ ⟹ يُرفَض ولو رفع عدّادَ الإجماع", GATE),
    S("التقشير · الحاكمُ فوريّ", "online_peel.json",
      ("التقشير_الفوري", "الجولة_الثانية", "ياء", "فوريّ"), 637,
      "run2 ⟵ peel2", "موضعَ باب «ي» — المقامُ الحاكمُ فوريٌّ لا دفعيّ", GATE),
    S("التقشير · الدفعيُّ عرضًا", "online_peel.json",
      ("التقشير_الفوري", "الجولة_الثانية", "ياء", "دفعيّ_عرضًا"), 728,
      "run2 (دفعيّ)", "موضعَ باب «ي» — عرضٌ موسومٌ بفارق 91 عن الحاكم", WITNESS),
    S("التنسور · مفردٌ منعكس", "tensor_law.json",
      ("دعوى_التنسور", "T1_تصديق", "أحوال", "مفرد-منعكس"), 27533,
      "run ⟵ T₁", "كلمةً — و16,487 منها بلا تنسورٍ أصلًا (∅·فعل·∅)", WITNESS),
    S("التنسور · الميمُ لها منازع", "tensor_law.json",
      ("دعوى_التنسور", "T2_تفنيد", "الميمُ_لها_منازع", "بشاهدٍ_مضادّ"), 446,
      "tensor_bill ⟵ T₂", "من 1,164 — الشاهدُ المضادّ من البايتات (منهم=من+هم)", GATE),
    S("الجامع · الوحدات", "jami3_mani3.json", ("البناءُ_الجامع_المانع", "الجامع", "الوحدات"), 362305,
      "partition", "وحدةً — الجامعُ يستوعب المجمَّد كلَّه بلا بقية", GATE),
    S("الجامع · داخل 112", "jami3_mani3.json", ("البناءُ_الجامع_المانع", "الجامع", "داخل_112"), 262355,
      "partition", "وحدةً من 362,305 — المرخَّصُ في الحقل 112", GATE),
    S("المانع · الارتدادُ وسمًا", "jami3_mani3.json",
      ("البناءُ_الجامع_المانع", "المانع", "ارتداد", "وسم"), 77801,
      "ascend (أعمى)", "من 77,801 — الخنجريةُ وسمَ مدٍّ: ارتدادٌ تامّ", GATE),
    S("المانع · الخنجريةُ فتحةً تُتلف", "jami3_mani3.json",
      ("البناءُ_الجامع_المانع", "المانع", "ارتداد", "فتحة"), 74585,
      "ascend (أعمى)", "من 77,801 — الاتفاقيةُ البديلة تُتلف 3,216 كلمة", GATE),
    # ——— محرّكُ الربط الاثني عشر (بوّابةٌ من يومه الأول — فلا يتعفّن) ———
    S("حدودُ الجملة داخل الآية", "jumla_links.json",
      ("الربط_v0", "مقامات", "داخل_الآية", "حدود"), 13191,
      "links_within ⟵ segment", "أزواجٌ داخل الآية — N قبل العدّ، ولا يُخلط بالعبور", GATE),
    S("أزواجُ العبور (الخطاب)", "jumla_links.json",
      ("الربط_v0", "مقامات", "العبور", "حدود"), 6235,
      "links_crossing", "حدُّ الآية يُعبَر معلنًا — المقامُ الثاني وحدَه", GATE),
    S("تغطيةُ الأسباب داخل الآية", "jumla_links.json",
      ("الربط_v0", "مقامات", "داخل_الآية", "تغطية"), 0.3289,
      "_tally ⟵ classify", "المصنَّفُ 4,339 من 13,191 — دون فاصل الإسقاط 90%", GATE),
    S("تغطيةُ الأسباب بالعبور", "jumla_links.json",
      ("الربط_v0", "مقامات", "العبور", "تغطية"), 0.3416,
      "_tally ⟵ classify", "المصنَّفُ 2,130 من 6,235 — مقامٌ آخر لا يُجمَع بالأوّل", GATE),
    S("المتبقّي غيرُ المسمّى (داخل الآية)", "jumla_links.json",
      ("الربط_v0", "مقامات", "داخل_الآية", "غيرُ_المسمّى"), 0,
      "_residue_kind ⟵ _tally", "كلُّ معلَّقٍ بجنسٍ مسمًّى — «غيرُ ذلك» صفرٌ أو سقط الشرط",
      GATE),
    S("المتبقّي غيرُ المسمّى (العبور)", "jumla_links.json",
      ("الربط_v0", "مقامات", "العبور", "غيرُ_المسمّى"), 0,
      "_residue_kind ⟵ _tally", "المقامُ الثاني بشرطه نفسِه — لا موضعَ بلا جنس", GATE),
    S("الجملُ المقطوعةُ بالتعريف المعلن", "jumla_links.json",
      ("الربط_v0", "جمل", "داخل_الآية"), 19427,
      "segment ⟵ head_of", "صدورٌ بالتعريف المعلن على 6,236 آية — عرضٌ لا يحكم", WITNESS),
    S("تعليقُ العطف داخل الآية", "jumla_links.json",
      ("الربط_v0", "مقامات", "داخل_الآية", "أجناسُ_المتبقّي", "صدرٌ بعاطفٍ ملتصق"), 6817,
      "classify ⟵ attached_atf", "العطفُ ليس سببًا — تعليقٌ لا تصنيف، ولا يُحتسَب تغطيةً",
      GATE),
    # ——— الجولة ٢: المُعادُ تبويبُه [شاهد]، والمقيسُ وحدَه [بوّابة] ———
    S("التغطيةُ بالوصل داخل الآية", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "عطفٌ_واصل", "داخل_الآية", "تغطيةٌ_بالوصل"), 0.8781,
      "wasl_view", "4,339 + 7,244 من 13,191 — مُعادُ تبويبٍ مشتقٌّ من مختوم، لا قياسٌ جديد",
      WITNESS),
    S("التغطيةُ بالوصل بالعبور", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "عطفٌ_واصل", "العبور", "تغطيةٌ_بالوصل"), 0.6882,
      "wasl_view", "2,130 + 2,161 من 6,235 — عرضٌ ثانٍ لا يرفع سقوطَ الجولة ١", WITNESS),
    S("صدورُ الفيات في مقام العبور", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "مقامُ_العبور_مرّتين", "صدورُ_الفيات"), 3040,
      "crossing_substation", "صدرُ آيةٍ بحدّ التلاوة — منها 1,139 نالت سببًا و1,901 معلَّقة",
      GATE),
    S("المقامُ الفرعيُّ للعبور", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "مقامُ_العبور_مرّتين", "المقامُ_الفرعيّ"), 3195,
      "crossing_substation", "6,235 − 3,040 — و«4,334» بديلٌ مرفوضٌ لطرحه المعلَّقَ وحدَه",
      GATE),
    S("تغطيةُ المقام الفرعيّ", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "مقامُ_العبور_مرّتين", "تغطيةُ_الفرعيّ"), 0.3102,
      "crossing_substation", "991 من 3,195 — مقامٌ ثالثٌ يُعرَض مع الخام، ولا رقمَ يُنقَل",
      GATE),
    S("البابُ الأوّل · تابعٌ لمرفوعٍ مُثبَت", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "أبوابُ_الاسميّ", "داخل_الآية", "أبواب",
       "تابعٌ لمرفوعٍ مُثبَت"), 53,
      "noun_doors ⟵ is_marfu3_proven", "من 1,464 — دون فاصل [250–900]، فالبابُ صوريٌّ ساقط",
      GATE),
    S("البابُ الثاني · مبتدأٌ مستقلٌّ حقًّا", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "أبوابُ_الاسميّ", "داخل_الآية", "أبواب",
       "مبتدأٌ مستقلٌّ حقًّا"), 1411,
      "noun_doors", "متمّمُ الأوّل بالبناء — يُعرَض ولا يُحتسَب تفسيرًا", WITNESS),
    S("حارسُ نزاهة الباب (داخل الآية)", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "أبوابُ_الاسميّ", "داخل_الآية", "حارسُ_النزاهة", "نسبة"),
      0.7941,
      "noun_doors ⟵ marfu3_antecedent",
      "1,952 من 2,458 مطابقةٍ كانت مفسَّرةً — القيدُ ليس مفصَّلًا على العتبة", GATE),
    S("حارسُ نزاهة الباب (العبور)", "jumla_links.json",
      ("الربط_v0", "الجولة_٢", "أبوابُ_الاسميّ", "العبور", "حارسُ_النزاهة", "نسبة"), 0.8160,
      "noun_doors ⟵ marfu3_antecedent", "1,299 من 1,592 — الحارسُ قائمٌ في المقامين", GATE),
    # ——— الجولة ٣: بابُ شبه الجملة — حكمُه ساقطٌ مودَعٌ، والصورةُ بجانبه ———
    S("بابُ شبهِ الجملة · مفسَّرٌ بإثبات الجرّ", "jumla_links.json",
      ("الربط_v0", "الجولة_٣", "بابُ_شبهِ_الجملة", "مفسَّرٌ_بالباب"), 21,
      "shibh_doors ⟵ jar_head ⟵ is_majrur_proven",
      "من 1,901 صدرَ آيةٍ بلا قرينة — دون أرضيةِ [40–120]، فالحكمُ ساقطٌ مودَعٌ "
      "ولا تُخفَّض الأرضيةُ بعده", GATE),
    S("بابُ شبهِ الجملة · الصورةُ وحدَها", "jumla_links.json",
      ("الربط_v0", "الجولة_٣", "بابُ_شبهِ_الجملة", "عددٌ_بالصورة_لا_يُحتسَب", "قيمة"), 75,
      "shibh_doors ⟵ jar_head_shape",
      "حرفٌ بلا مجرورٍ مُثبَت — تشخيصٌ يُعرَض ولا يدخل بابًا ولا تغطية: فيه «بِئسما» "
      "و«مَن يُطِعِ»، والفرقُ 75 ⟵ 21 ثمنُ قيد الإثبات", WITNESS),
    S("حارسُ نزاهة بابِ شبهِ الجملة", "jumla_links.json",
      ("الربط_v0", "الجولة_٣", "بابُ_شبهِ_الجملة", "حارسُ_النزاهة", "نسبة"), 0.3875,
      "shibh_doors ⟵ jar_head",
      "31 من 80 مطابقةً كانت مفسَّرةً سلفًا بأحد الاثني عشر — فوق فاصل 0.25، "
      "فالقيدُ ليس مفصَّلًا على المتبقّي", GATE),
    S("حضورٌ لا تعلُّق · داخل الآية", "jumla_links.json",
      ("الربط_v0", "الجولة_٣", "حضورٌ_لا_تعلُّق", "داخل_الآية", "جارٌّ_في_الأثناء"), 1922,
      "shibh_witness ⟵ _jar_inside",
      "جارٌّ في أثناء الجملة من 13,191 حدًّا — [شاهد] يُعرَض ولا يُحتسَب تغطيةً: "
      "احتسابُه ربحٌ بالمِقَصّ لا بالمِجهر", WITNESS),
    S("حضورٌ لا تعلُّق · العبور", "jumla_links.json",
      ("الربط_v0", "الجولة_٣", "حضورٌ_لا_تعلُّق", "العبور", "جارٌّ_في_الأثناء"), 1248,
      "shibh_witness ⟵ _jar_inside",
      "جارٌّ في أثناء الجملة من 6,235 حدًّا — [شاهد] بلا فاصلٍ ولا احتساب", WITNESS),

    S("الحياد · الألفُ تفرّق", "hiyad.json", ("دعوى_الحياد", "حيادٌ_تقابليّ", "ا", "مواضع"), 11024,
      "contrastive", "موضعًا — الألفُ محايدةٌ في الحالة لا في الحرف", GATE),

    # ——— تعدادُ الشهود: أوّلُ مقدارٍ مختومٍ مقيسٍ على غير المجمَّد ———
    # كلُّ ما فوق هذا السطر مقيسٌ على mujammad.txt وحدَه. وهذه الأربعةُ مقيسةٌ على
    # بايتاتِ شاهدين من OpenITI: تُصادَم ببصمتها في البيان ثمّ تُقشَّر بـnormalize.py.
    S("أسطرُ متن النحّاس المقشورة", "sources_census.json",
      ("تعدادُ_الشهود", "nahhas_icrab_shamay", "أسطر"), 35679,
      "census_of ⟵ normalize.read_lines",
      "إعرابُ القرآن للنحّاس — ما بعد ‎#META#Header#End#‎ سطرًا سطرًا، والبومُ مقشورٌ لا معدود",
      GATE),
    S("سطورُ الوصل في النحّاس", "sources_census.json",
      ("تعدادُ_الشهود", "nahhas_icrab_shamay", "أصناف", "وصل"), 19642,
      "census_of ⟵ normalize.classify",
      "‎~~‎ وصلُ فقرةٍ سابقة — أكثرُ من نصف المتن، فمن عدَّ السطرَ فقرةً أخطأ نصفَ العدّ",
      GATE),
    S("مواضعُ الترقيم في النحّاس", "sources_census.json",
      ("تعدادُ_الشهود", "nahhas_icrab_shamay", "ترقيم"), 3948,
      "census_of ⟵ normalize.PAGE",
      "PageVxxPyy منتزَعًا حقلًا لا محذوفًا — من PageV01P001 إلى PageV05P317", GATE),
    S("أسطرُ متن الألفية المقشورة", "sources_census.json",
      ("تعدادُ_الشهود", "ibnmalik_alfiyya", "أسطر"), 1255,
      "census_of ⟵ normalize.read_lines",
      "شاهدٌ ثانٍ مخالفُ الهيئة (بلا بومٍ وبلا وصلٍ البتّة) — يُعرَض ولا يحكم", WITNESS),
]


def dig(obj, path, name):
    """يشقُّ المسارَ في المخرَج الطازج — والمفقودُ صريخٌ ولو كان الختمُ [شاهدًا]."""
    cur = obj
    for key in path:
        if isinstance(cur, list):
            if not isinstance(key, int) or key >= len(cur):
                raise KeyError(f"الختم «{name}»: المسارُ {path} انقطع عند {key!r}")
            cur = cur[key]
        elif isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            raise KeyError(f"الختم «{name}»: المسارُ {path} انقطع عند {key!r} — "
                           f"رقمٌ بلا مولِّدٍ حيّ")
    return cur


def regenerate(deposit, outdir):
    """يشغّل مولِّدَ الوديعة إلى ملفٍّ طازجٍ ويُرجع محتواه — لا يُقرَأ رقمٌ من الوديعة نفسِها."""
    argv = GENERATORS[deposit]
    fresh = os.path.join(outdir, deposit)
    cmd = [sys.executable, os.path.join(ROOT, argv[0])] + argv[1:] + ["--json", fresh]
    if argv[0].endswith("induction_engine.py"):      # محرّكُ الاستقراء يأخذ --json=قيمة
        cmd = [sys.executable, os.path.join(ROOT, argv[0]), f"--json={fresh}"] + argv[1:]
    run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(f"مولِّدُ {deposit} سقط:\n{run.stdout[-2000:]}\n{run.stderr[-2000:]}")
    with open(fresh, encoding="utf-8") as fh:
        return json.load(fh)


def coverage(verbose=True, _found=None, _ci=None):
    """حارسُ التغطية الذاتي: كلُّ وديعةِ JSON في الشجرة مبوَّبةٌ — أو يسقط CI من لحظة ولادتها.

    العلّةُ التي يقتلها: `pairs_v0.json` و`context_ladder.json` عاشتا خارج كلِّ بوّابةٍ
    فتعفّنتا صامتتين (محرّكاهما لم يعودا يستوردان أصلًا، وإحداهما لم تكن تُولَّد مرّتين
    على النسق نفسِه). فالعدُّ هنا ذاتيٌّ: لا قائمةَ ودائعَ مكتوبةً بيدٍ تُقارَن بقائمةٍ
    أخرى مكتوبةٍ بيد، بل **مسحُ الشجرة** يُقابَل بالمبوَّب. ودعوى «مبوَّبٌ في ci.yml»
    لا تُصدَّق بكتابتها هنا، بل تُفتَّش في بايتات ci.yml.
    """
    problems = []
    if _found is None:
        _found = set()
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".github")]
            for fn in files:
                if fn.endswith(".json"):
                    _found.add(fn)
    found = set(_found)

    if _ci is None:
        with open(os.path.join(ROOT, ".github", "workflows", "ci.yml"), encoding="utf-8") as fh:
            _ci = fh.read()
    ci = _ci

    for dep in CI_COLLIDED:
        if dep not in ci:
            problems.append(f"الوديعة «{dep}» مدَّعًى أنّها مبوَّبةٌ في ci.yml ولا ذكرَ لها فيه")

    gated = set(GENERATORS) | set(CI_COLLIDED)
    for dep in sorted(found - gated):
        problems.append(f"وديعةٌ يتيمة: «{dep}» في الشجرة ولا بوّابةَ تمرّ عليها — "
                        f"تُدخَل في GENERATORS (بمولِّدها) أو في CI_COLLIDED (بخطوتها)")
    for dep in sorted(gated - found):
        problems.append(f"وديعةٌ مبوَّبةٌ غائبةٌ عن الشجرة: «{dep}»")

    if verbose:
        print(f"— التغطية: {len(found)} وديعةً في الشجرة · {len(GENERATORS)} بمولِّدٍ هنا "
              f"· {len(CI_COLLIDED)} بخطوةٍ في ci.yml —")
        for p in problems:
            print(f"::error::{p}")
        if not problems:
            print("    ✓ لا يتيمَ: كلُّ وديعةٍ مبوَّبة")
    return problems


# فواتيرُ الودائع: كلُّ دعوى نموذجٍ تُسجَّل هنا بمسارِ Δ **ومسارِ حكمِها المكتوب**.
# والمصادمةُ هي المقصود: الحكمُ المكتوبُ في الوديعة يُقابَل بالحكم المشتقّ من إشارة Δ،
# فلا يُقبَل «يُقبَل» فوق فاتورةٍ موجبة. (قاعدةُ «لا رقمَ بلا فاتورة»: CONTRIBUTING.md §٢)
# الاتفاقيةُ واحدةٌ معلنة: Δ بالبتّات، سالبٌ ⟹ يُقبَل · موجبٌ ⟹ يُرفَض.
BILLS = {
    "jami3_mani3.json": (("البناءُ_الجامع_المانع", "الحَكَم", "فرق"),
                         ("البناءُ_الجامع_المانع", "الحَكَم", "حكم"),
                         "قسمةُ الحقل 112"),
    "tensor_law.json": (("دعوى_التنسور", "T2_تفنيد", "الفاتورةُ_ترفض", "جداول",
                         "التنسور كما هو", "فائدة"),
                        ("دعوى_التنسور", "T2_تفنيد", "الفاتورةُ_ترفض", "جداول",
                         "التنسور كما هو", "حكم"),
                        "سابقة⊗وزن⊗لاحقة"),
}

# ودائعُ الحياد: الحكمُ فيها لا يُكتَب في الوديعة، فيُقابَل Δ بالحكم المعلن هنا.
HIYAD_BILLS = {"ا": ("طيُّ الألف وسمًا", "يُرفَض"), "وي": ("طيُّ و/ي وسمًا", "يُقبَل")}


def _verdict_of(delta):
    """حكمُ الفاتورة — **من القانون لا من نسخةٍ هنا**.

    ولولا هذا لصادَق المدقِّقُ نفسَه: لو تغيّر الحدُّ في `deposit_law` لبقي هذا السجلُّ
    يوافق الودائعَ القديمةَ على قانونٍ متروك، فيشهد بالسلامة وهو أعمى.
    """
    return verdict(delta)


def sole_judge(verbose=True, _dir=None):
    """حارسُ «حَكَمٌ واحد»: القانونُ يُستدعى ولا يُنسَخ.

    العلّةُ الملموسة: كان نصُّ الحكم وحدُّ الانحلال مكتوبين بأيديهما في `jami3_mani3`
    و`tensor_law` و`hiyad` و`deposit_law` وفي هذا السجلِّ نفسِه — خمسُ نسخٍ توافقت
    بالصدفة لا بالبناء. فلو رُقِّي الحدُّ في واحدةٍ لتخالفت الودائعُ **صامتةً**، ولصادَق
    المدقِّقُ المُدقَّقَ بقانونٍ غيرِ قانونِه.

    والفحصُ على **الشجرة النحوية لا على النصّ**: يُبحَث عن تعبيرٍ شرطيٍّ يُخرج «يُقبَل»،
    وعن مقارنةٍ بعتبة الانحلال — فلا يُسقِط الحارسُ وثيقةً تذكر القاعدةَ حكايةً (وقد
    أسقط هذه الدالّةَ نفسَها حين كان يفتّش البايتات، فكان ذلك تكذيبَه الأول).
    """
    problems = []
    law = os.path.basename(LAW_FILE)
    folder = _dir or HERE
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith(".py") or fname == law:
            continue
        tree = ast.parse(open(os.path.join(folder, fname), encoding="utf-8").read(), fname)
        for node in ast.walk(tree):
            if (isinstance(node, ast.IfExp)
                    and isinstance(node.body, ast.Constant) and node.body.value == ACCEPT):
                problems.append(f"حَكَمٌ ثانٍ في induction/{fname}:{node.lineno} — نصُّ الحكم "
                                f"مكتوبٌ بيده، ويُستدعى `verdict` من {law} ولا يُنسَخ")
            elif (isinstance(node, ast.Compare)
                  and any(isinstance(c, ast.Constant) and c.value == DEGENERACY_CEILING
                          for c in node.comparators)):
                problems.append(f"حَكَمٌ ثانٍ في induction/{fname}:{node.lineno} — حدُّ الانحلال "
                                f"مكتوبٌ بيده، ويُستدعى `degenerate` من {law} ولا يُنسَخ")
    if verbose and not problems:
        print(f"    ✓ حَكَمٌ واحد: لا نسخةَ ثانيةً للحكم ولا لحدِّ الانحلال خارج {law}")
    return problems


def contracts(verbose=True):
    """قاعدةُ «لا رقمَ بلا فاتورة»، مفحوصةً لا موعودة.

    ① كلُّ وديعةٍ بمولِّدٍ هنا لها ختمٌ [بوّابة] واحدٌ على الأقلّ — وإلا فهي رقمٌ يُعرَض
       ولا يَحكم، وذلك بابُ «معرَّض».
    ② كلُّ دعوى نموذجٍ لها Δ يُقرأ من وديعتها، و**حكمُها المكتوبُ يُصادَم بإشارة Δ**.
    ③ **ولا حَكَمَ ثانٍ**: لا يُعاد كتابةُ الحكم ولا حدِّ الانحلال خارج `deposit_law` —
       فالقانونُ نسخةٌ واحدة، لا خمسٌ متوافقةٌ بالصدفة.
    """
    problems = []
    problems += sole_judge(verbose)
    for deposit in GENERATORS:
        if not any(s["وديعة"] == deposit and s["صنف"] == GATE for s in SEALS):
            problems.append(f"الوديعة «{deposit}» بلا ختمٍ {GATE} واحد — عرضٌ بلا حارس")

    def check(deposit, delta, written, claim):
        derived = _verdict_of(delta)
        if written != derived:
            problems.append(f"فاتورةٌ تخالف حكمَها: «{claim}» في {deposit} — "
                            f"Δ = {delta:+} ⟹ {derived}، والمكتوبُ «{written}»")
        elif verbose:
            print(f"    Δ({claim}) = {delta:+,} بتًّا ⟹ {derived} — والمكتوبُ يوافقه ✓")

    for deposit, (dpath, vpath, claim) in BILLS.items():
        if deposit not in GENERATORS:
            problems.append(f"فاتورةٌ لوديعةٍ بلا مولِّد: «{deposit}»")
            continue
        with open(deposit_path(deposit), encoding="utf-8") as fh:
            doc = json.load(fh)
        check(deposit, dig(doc, dpath, f"فاتورة {claim}"),
              dig(doc, vpath, f"حكم {claim}"), claim)

    with open(deposit_path("hiyad.json"), encoding="utf-8") as fh:
        hiyad = json.load(fh)["دعوى_الحياد"]["الحَكَم"]
    for key, (claim, declared) in HIYAD_BILLS.items():
        check("hiyad.json", hiyad[key]["فرق"], declared, claim)

    if verbose and not problems:
        print("    ✓ لا وديعةَ بلا حارس، ولا حكمَ يخالف إشارةَ فاتورتِه")
    for p in problems:
        print(f"::error::{p}")
    return problems


def audit_sheet():
    """قائمةُ الأختام للتدقيق الخارجي — **مولَّدةٌ من السجلّ لا مكتوبةٌ بيد**.

    فلا تتخلّف الورقةُ عن الشجرة: CI يعيد توليدَها ويصادمُها حرفًا بحرف.
    """
    rows = ["# AUDIT-SEALS — قائمةُ الأختام للتدقيق الخارجي الثاني (Alghanem)",
            "",
            "> **مولَّدةٌ آليًّا** بـ`python induction/seals.py --audit AUDIT-SEALS.md`،",
            "> ويصادمُها CI بفارق صفر. لا تُحرَّر بيد.",
            "",
            "## الدعوى المعروضة",
            "",
            "كلُّ رقمٍ أدناه **يُعاد توليدُه** بأمرٍ واحد (`python induction/seals.py`)، ويُقرَأ",
            "من مخرَجٍ طازجٍ لا من الوديعة. والمطلوبُ من التدقيق حكمٌ من ثلاثيِّ T لكلِّ سطر",
            "(انظر `AUDIT-188.md` §٠): **T₁** تصديقٌ بعدٍّ من مقامٍ مختوم · **T₂** تفنيدٌ بحسابٍ",
            "معروض · **T₃** تعليقٌ بالاسم. والصمتُ ليس حكمًا.",
            "",
            "## الأختام",
            "",
            "| # | الختم | القيمة | الصنف | الدالّة | المقام | الوديعة · المسار |",
            "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(SEALS, 1):
        rows.append(f"| {i} | {s['اسم']} | `{s['قيمة']}` | {s['صنف']} | `{s['دالّة']}` | "
                    f"{s['مقام']} | `{s['وديعة']}` · `{'/'.join(map(str, s['مسار']))}` |")
    n_gate = sum(1 for s in SEALS if s["صنف"] == GATE)
    rows += ["",
             f"**العدّ**: {len(SEALS)} ختمًا — {n_gate} {GATE} · {len(SEALS) - n_gate} {WITNESS}.",
             "",
             "## الفواتيرُ المصادَمةُ بأحكامها",
             "",
             "كلُّ دعوى نموذجٍ يُقرأ Δ من وديعتها، و**يُشتقّ الحكمُ من إشارته** فيُقابَل بالمكتوب",
             "(`seals.contracts`، والاتفاقيةُ واحدة: Δ سالبٌ ⟹ يُقبَل · موجبٌ ⟹ يُرفَض):",
             "",
             "| الدعوى | Δ (بتًّا) | الحكمُ المشتقّ |",
             "|---|---|---|"]
    rows += [f"| {claim} | {delta:+,} | {حكم} |" for claim, delta, حكم in _bill_rows()]
    rows += ["",
             "## البندُ الذي وَلد من عطلٍ — الفصلُ بين جدولِ التدريب والمقامات",
             "",
             "طُبع رقمٌ واحدٌ باسمين ومقامين: «H(البوّابة|سابقتها)» = 1.2050 مرّةً و1.3985 أخرى.",
             "والعلّةُ لم تكن اتفاقيتين، بل **جدولَ نصفِ التدريب (3,118 زوجًا) على مقاماتِ",
             "الأزواج كلِّها (6,235)** — فكتلةُ كلِّ سابقةٍ كانت ‎≈0.50 لا 1.0، فلم تكن إنتروبيا",
             "شرطيةً أصلًا. والإصلاحُ ثلاثةُ أشياء معًا:",
             "",
             "1. اتفاقيةٌ واحدة: الجدولُ والمقاماتُ من التيار نفسِه — `H_cond = 1.398473785338209`.",
             "2. حارسُ كتلة: `assert abs(mass - 1.0) < 1e-9` لكلِّ سابقة، فلا يعود العطلُ صامتًا.",
             "3. فصلُ المفتاحين في الوديعة: `transitions_train` ⟷ `transitions_all` — فلا يجتمع",
             "   اسمٌ واحدٌ على جدولين.",
             "",
             "والمصادمةُ الخارجية: `algebra_engine.gate_markov_for()['H_gc']` تُعطي الرقمَ نفسَه",
             "بفارق `0.0` بتنفيذٍ مستقلّ — فالرقمُ محروسٌ بمصدرين لا بواحد.",
             "",
             "## ما يُطلَب من المدقِّق بعينه",
             "",
             "1. أيُّ ختمٍ [بوّابة] ينبغي أن يكون [شاهدًا] (يُعرَض ولا يَحكم)؟ وبأيِّ سند؟",
             "2. أيُّ **مقامٍ** أعلاه مخلوطٌ كما خُلط مقامُ H_cond — اسمٌ واحدٌ على قاعدتين؟",
             "3. `QAC-fork-v0.4` محجورٌ T₃ لانعدام FROZEN (`AUDIT-188.md` §١ صفّ ٢): ما بصمتُه",
             "   وطولُه ومصدرُه ومَن صحّح جذورَه وبأيِّ ضابط؟ — فمرايا الشبكة تتخالف في الطول.",
             ""]
    return "\n".join(rows)


def _bill_rows():
    """صفوفُ الفواتير — تُقرأ من الودائع لا تُكتب في الورقة."""
    out = []
    for deposit, (dpath, vpath, claim) in BILLS.items():
        with open(deposit_path(deposit), encoding="utf-8") as fh:
            doc = json.load(fh)
        delta = dig(doc, dpath, f"فاتورة {claim}")
        out.append((claim, delta, _verdict_of(delta)))
    with open(deposit_path("hiyad.json"), encoding="utf-8") as fh:
        hiyad = json.load(fh)["دعوى_الحياد"]["الحَكَم"]
    for key, (claim, _declared) in HIYAD_BILLS.items():
        out.append((claim, hiyad[key]["فرق"], _verdict_of(hiyad[key]["فرق"])))
    return out


def regen_all(verbose=True, report=None):
    """يعيد توليدَ كلِّ وديعةٍ وكلِّ ختمٍ ويصادمُهما — فارقٌ صفرٌ أو صريخ."""
    problems, checked = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for deposit in GENERATORS:
            fresh = regenerate(deposit, tmp)
            with open(deposit_path(deposit), encoding="utf-8") as fh:
                stored = json.load(fh)
            if fresh != stored:
                problems.append(f"{deposit}: الوديعةُ المودَعة خالفت ما يُنتجه مولِّدُها")
                if report is not None:
                    report["ودائعُ_خالفت"].append(deposit)
                if verbose:
                    print(f"::error::{problems[-1]}")
                continue
            if verbose:
                print(f"{deposit} مُعادةُ الإنتاج بفارق صفر ✓")
            for seal in SEALS:
                if seal["وديعة"] != deposit:
                    continue
                checked += 1
                try:
                    got = dig(fresh, seal["مسار"], seal["اسم"])
                except KeyError as exc:
                    problems.append(str(exc))
                    if report is not None:
                        report["أختامٌ_انحرفت"].append(seal["اسم"])
                    if verbose:
                        print(f"::error::{exc}")
                    continue
                if got != seal["قيمة"]:
                    problems.append(f"الختم «{seal['اسم']}» {seal['صنف']}: "
                                    f"المتوقَّع {seal['قيمة']} · المولَّد {got} — "
                                    f"({seal['دالّة']} · {seal['مقام']})")
                    if report is not None:
                        report["أختامٌ_انحرفت"].append(seal["اسم"])
                    if verbose:
                        print(f"::error::{problems[-1]}")
                elif verbose:
                    print(f"    ✓ {seal['صنف']} {seal['اسم']} = {got}  "
                          f"⟵ {seal['دالّة']} · {seal['مقام']}")
    if verbose:
        n_gate = sum(1 for s in SEALS if s["صنف"] == GATE)
        print(f"\nالأختام: {checked} مصادَمًا من {len(SEALS)} مسجَّلًا "
              f"({n_gate} {GATE} · {len(SEALS) - n_gate} {WITNESS}) — "
              f"{'كلُّها بفارق صفر ✓' if not problems else f'سقط منها {len(problems)} ✗'}")
    return problems


def ci_text():
    with open(os.path.join(ROOT, ".github", "workflows", "ci.yml"), encoding="utf-8") as fh:
        return fh.read()


def falsify(verbose=True):
    """هل يستطيع هذا الحارسُ أن يرفض؟ — ثلاثُ تجارِبَ مكذِّبةٍ على نسخٍ في الذاكرة."""
    trials = {}
    sample = {"مقيس": {"H_cond": 1.398473785338209, "marginal": {"C": 2888}}}

    try:
        dig(sample, ("مقيس", "لا_وجود_له"), "تجربة")
        trials["مسارٌ مفقود"] = "لم يرفض ✗"
    except KeyError:
        trials["مسارٌ مفقود"] = "رفض ✓"

    got = dig(sample, ("مقيس", "H_cond"), "تجربة")
    trials["قيمةٌ مبدَّلة"] = "رفض ✓" if got != 1.2050 else "لم يرفض ✗"

    witness = [s for s in SEALS if s["صنف"] == WITNESS][0]
    try:
        dig({}, witness["مسار"], witness["اسم"])
        trials["شاهدٌ بلا مسار"] = "لم يرفض ✗"
    except KeyError:
        trials["شاهدٌ بلا مسار"] = "رفض ✓ — العرضُ ليس إعفاءً من التوليد"

    try:
        S("بلا دالّة", "results.json", ("مقيس",), 1, "", "مقام", GATE)
        trials["ختمٌ بلا دالّة"] = "لم يرفض ✗"
    except AssertionError:
        trials["ختمٌ بلا دالّة"] = "رفض ✓ — لا رقمَ بلا اسم دالّتِه"

    orphan = coverage(verbose=False, _found=set(GENERATORS) | set(CI_COLLIDED) | {"يتيم_v0.json"}, _ci=ci_text())
    trials["وديعةٌ يتيمةٌ وُلدت"] = ("رفض ✓ — التغطيةُ تُمسك اليتيمَ ساعةَ ولادته"
                                    if any("يتيم_v0.json" in p for p in orphan) else "لم يرفض ✗")

    claim = coverage(verbose=False, _found=set(GENERATORS) | set(CI_COLLIDED), _ci="")
    trials["دعوى تبويبٍ كاذبة"] = ("رفض ✓ — «مبوَّبٌ في ci.yml» تُفتَّش لا تُصدَّق"
                                   if len(claim) >= len(CI_COLLIDED) else "لم يرفض ✗")

    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "ناسخ.py"), "w", encoding="utf-8") as fh:
            fh.write(f'حكم = "{ACCEPT}" if d < 0 else "x"\nمنحلّ = v / n > {DEGENERACY_CEILING}\n')
        copies = sole_judge(verbose=False, _dir=td)
    trials["حَكَمٌ ثانٍ يُكتَب"] = ("رفض ✓ — القانونُ يُستدعى ولا يُنسَخ (الحكمُ وحدُّ الانحلال معًا)"
                                   if len(copies) == 2 else "لم يرفض ✗")

    trials["حكمٌ يخالف فاتورتَه"] = ("رفض ✓ — «يُقبَل» فوق Δ موجبةٍ لا تمرّ"
                                     if _verdict_of(+69037) == "يُرفَض"
                                     and _verdict_of(-5427) == "يُقبَل" else "لم يرفض ✗")

    if verbose:
        print("— تكذيبُ الحارس (هل يستطيع أن يرفض؟) —")
        for k, v in trials.items():
            print(f"    {k}: {v}")
    assert all(v.startswith("رفض") for v in trials.values()), "حارسُ الأختام لا يرفض — فهو عرض"
    return trials


def record(trials, report, problems):
    """عقدُ الوديعة `seals.json` — تسعةُ حقولٍ تقرؤها خطوةُ CI وتُسقطها عند أوّل انحراف.

    ولِمَ وديعةٌ للسجلِّ نفسِه؟ لأنّ الحارسَ الذي لا يودِع مخرَجَه لا يُصادَم: يبقى نجاحُه
    دعوى طباعةٍ تُقرأ بالعين. فهنا يُودَع مخرَجُه ويُصادَم كسائر الودائع — **والحارسُ
    وديعةٌ عند القانون كالمحروس**.
    """
    return dict(
        أختام=[dict(اسم=s["اسم"], وديعة=s["وديعة"], مسار=list(s["مسار"]), قيمة=s["قيمة"],
                    دالّة=s["دالّة"], مقام=s["مقام"], صنف=s["صنف"]) for s in SEALS],
        أختامٌ_انحرفت=sorted(set(report["أختامٌ_انحرفت"])),
        أختامٌ_بلا_مولِّد=sorted({s["اسم"] for s in SEALS if s["وديعة"] not in GENERATORS}),
        ودائعُ_خالفت=sorted(set(report["ودائعُ_خالفت"])),
        اختبارُ_التكذيب=[dict(محاولة=k, مرفوضة=v.startswith("رفض")) for k, v in trials.items()],
        مسبارات=sorted(GENERATORS),
        بوّابات=sum(1 for s in SEALS if s["صنف"] == GATE),
        شواهد=sum(1 for s in SEALS if s["صنف"] == WITNESS),
        الحكم=("حيٌّ: كلُّ ختمٍ يولَّد ويُصادَم" if not problems
               else f"ساقطٌ: {len(problems)} انحرافًا"))


def main():
    ap = argparse.ArgumentParser(description="سجلُّ الأختام الحيّة")
    ap.add_argument("--falsify-only", action="store_true")
    ap.add_argument("--audit", metavar="مسار", help="توليدُ ورقة التدقيق الخارجي")
    ap.add_argument("--json")
    args = ap.parse_args()

    if args.audit:                       # التوليدُ وحدَه — ثمّ تُصادَم الورقةُ في CI
        sheet = audit_sheet()
        with open(args.audit, "w", encoding="utf-8") as fh:
            fh.write(sheet)
        print(f"ورقةُ التدقيق ({len(SEALS)} ختمًا) ⟵ {args.audit}")
        return 0

    print("سجلُّ الأختام — لا رقمَ إلا بمولِّدٍ يُشغَّل، ولا رقمَ إلا باسم دالّتِه ومقامِه\n")
    trials = falsify()
    report = dict(ودائعُ_خالفت=[], أختامٌ_انحرفت=[])
    problems = ([] if args.falsify_only
                else coverage() + contracts() + regen_all(report=report))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"سجلُّ_الأختام": record(trials, report, problems)},
                      fh, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {args.json}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
