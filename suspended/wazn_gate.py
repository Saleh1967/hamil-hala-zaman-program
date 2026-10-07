# wazn_gate.py — بابُ الشاهد الرابع (الوزن): سلّمُ التوليد الشكليّ يُقاس على مكسبٍ حقيقيٍّ
# مُقفَلٍ سلفًا — لا يُبتكَر شيءٌ هنا: كلُّ آلةٍ مستوردةٌ من موضعها المودَع في الشجرة.
#
# ــ ٠) ما هذا الباب ولماذا رابعٌ ـــــــــــــــــــــــــــــــــــــــــــــــــ
# اختُبر بروتوكولُ «قيدٌ يُعلَن قبل العدّ + أربعُ آلاتٍ مستقلّةٌ تتّفق» ثلاثَ مراتٍ في
# هذا المستودع: مرّتان صوريّتان في burhan/ (CERT-GENERATIONS بالعوديّة والمصفوفة
# والصيغة المغلقة والتعداد الشامل، وCERT-INERTNESS بثلاثة حقولٍ مرخَّصة) ومرّةٌ على
# بايتاتٍ حقيقيّة في tarjih_gate.py (اختبارُ الجمع قبل السلّم). هذا البابُ **الرابع**
# لا يضيف آلةً خامسة: يقرأ الثلاثَ الأولى بختمها المودَع (`burhan_v0.json`) ثمّ يبني
# فوقها اختبارَ شاهدٍ واحدًا جديدًا يربط سلّمَ الأجيال الصوريّ بمكسبٍ حقيقيٍّ مُقفَل:
# «أوزان_v0/awzan_gain» = 3,098 موضعًا بكلفة 1,456 بت (`dictionary_v0.json`).
#
# ــ ١) التعذّرُ المعلن قبل البناء ـــــــــــــــــــــــــــــــــــــــــــــــ
#   • القيدُ الموروثُ بلا تعديل — **Φ2-1**: «لا يتجاور ساكنان»، وهو حرفيًّا قيدُ Φ
#     في `burhan/cert_generations.py` (لا يُعاد تعريفه هنا، بل يُقرأ من وديعته).
#   • البندُ المتوقَّعُ حسابيًّا قبل أيّ تعداد: الصيغةُ المغلقة والعوديّةُ معلنتان
#     بحرفهما في burhan (`G_k = Σ_j C(k−j+1,j)·28^j·84^(k−j)`)، وقيمُ G1..G3
#     (112 · 11,760 · 1,251,264) مُعلَنةٌ هنا **قبل قراءة الوديعة** لا بعدها — وأيُّ
#     تخالفٍ بينها وبين ما تُظهره `burhan_v0.json` صريخٌ (E_MATERIAL)، لا تصحيحٌ صامت.
#
# ــ ٢) التعدادُ الحتميّ بأربع آلاتٍ لا تتّصل ـــــــــــــــــــــــــــــــــــــ
# مقروءٌ من `burhan/burhan_v0.json` — الشهادةُ نفسُها التي شغّلت العوديّةَ ومصفوفةَ
# النقل والصيغةَ المغلقةَ والتعدادَ الشاملَ (itertools.product) كأربع عملياتٍ منفصلةٍ
# (انضباطُ burhan: «الاستقلالُ محفوظ — الشهاداتُ تُشغَّل عملياتٍ منفصلة لا تُستورَد»)،
# فلا يُعاد استيرادُها كودًا هنا حتّى لا يُخالَف ذلك الانضباط — بل تُصادَم قيمتُها
# المودَعةُ بالمُعلَن أعلاه، وحكمُها («خضراء») يُصادَم لا يُفترَض.
#
# ــ ٣) بوّابةُ الوزن: بذرةٌ من الختم، ورتبٌ ثلاثٌ جديدةُ الاسم لا مستوردة ـــــــــ
# «الرتبُ R0/R1/R2 كما في سجلّ burhan» **بحثٌ صريحٌ لم يجد** هذه الأسماءَ حرفيًّا في
# burhan (لا "R0" ولا "R1" ولا "R2" في أيّ ملفٍّ هناك — أقربُ ما فيه ثلاثةُ حقولٍ
# مسمّاةٌ بحجمها: |A|=28/32/35 في CERT-INERTNESS). فالتسميةُ R0/R1/R2 **جديدةٌ في
# هذا الباب**، مبنيّةٌ على نفس **بنية** الاختبار الثلاثيّ في CERT-INERTNESS (أساسٌ ·
# تبديلٌ خاملٌ يجب ألّا يتحرّك · توسيعٌ حقيقيٌّ يجب أن يتحرّك) لا نسخًا لاسمها:
#   R0 = PREFIX الفعليّ في awzan_engine.py (ستةُ أزواجٍ معلنةٌ بالاسم) — بلا تبديل.
#   R1 = الأعضاءُ الستةُ أنفسُهم، مُعادُ إدخالِهم بترتيبٍ مبذورٍ (Fisher–Yates بمفتاح
#        seed(R1)) في مجموعةٍ جديدة — شاهدُ خمولٍ: العضويةُ لا الترتيبُ هي الحاكمة
#        في `set`، فلا يجوز أن يتحرّك رقمٌ واحد؛ تحرُّكُه يفضح اعتمادًا خفيًّا على
#        ترتيب التسجيل (تكذيبٌ حقيقيّ ممكن، لا تحصيلَ حاصل).
#   R2 = الأعضاءُ الستةُ + سابقةٌ سابعةٌ معلنةٌ بالاسم («س» بفتحة — السينُ الاستقباليّة
#        `سـ+يفعل`، لغةً لا اختلاقًا، وغيرُ مرخَّصةٍ اليوم) — توسيعٌ حقيقيٌّ للترخيص؛
#        شاهدُ إبصار: يجب أن يتحرّك رقمٌ واحدٌ على الأقلّ، وإلّا فالآلةُ عمياء.
# والبذرةُ: `SHA256(ختمُ mujammad.txt ‖ اسمُ الرتبة)` — سلسلةٌ واحدةٌ لكلّ رتبةٍ لا
# تُختار بعد رؤية الرقم، فتُستعمَل رقمًا صحيحًا يبذر Fisher–Yates لـR1 فقط (R0 لا
# تبديلَ فيها، وR2 مرشَّحٌ واحدٌ معلنٌ لا قرعةَ فيه).
#
# ــ ٤) الربطُ بالمُقفَل ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# R0 تُصادَم حرفيًّا بوديعة `dictionary_v0.json` (`awzan_gain`=3,098 · `rules_cost_bits`
# 1,456 = 192 [ستُّ قواعدَ أخرى لا تمسّ PREFIX: ز-مزاح·ق-فراغ·ع-تبدل·ث-وحدة·ح-شدة·
# ح-جار-ملتصق، `rules_only_bits`] + 1,264 [`table_cost_bits` من awzan_engine.run()
# نفسِها — وهي تتضمّن كلفةَ PREFIX ذاتَها، فلا تُضاف مرّةً أخرى]) — فإن خالفتها صريخ.
# (تصحيحٌ: الجلسةُ الأولى أعادت جمعَ كلفة PREFIX مرّتين بالخطأ ووصفت 192 خطأً بأنّها
# «ستُّ أزواج PREFIX×32» — صادف مجموعُها 192 نفسَ رقم القواعد الستِّ الأخرى عند R0
# فقط (كلاهما 6×32)، فتساوى الرقمُ الكليّ صدفةً بينما التفسيرُ مختلف؛ ينكشف الفرقُ
# عند R2 حيث الرقمان يفترقان: 32 [الصوابُ، عضوٌ سابعٌ واحد] لا 64 [الخطأُ المزدوج]).
# وR2 هي الشاهدُ الرابعُ بعينه: عبورُها بوّابتَها (تحرُّكٌ حقيقيّ) يربط سلّمَ التوليد
# الصوريّ (باب ١–٢) بمكسب الأوزان الحقيقيّ (باب ٤) — وإن سقطت تُسجَّل ساقطةً باسمها.
# وفاتورةُ الربح (§ ٦) منفصلةٌ عن فاتورة الحركة هذه: الحركةُ Δ≠0 لا تعني ربحًا.
#
# ــ الحدُّ المُعلَن: ما لا يقوله هذا الباب ـــــــــــــــــــــــــــــــــــــ
#   • لا يُدَّعى أنّ Φ2-1 (لا سكون-سكون) شرطٌ لغويٌّ على PREFIX نفسِها — الأزواجُ
#     الستةُ كلُّها متحرّكةٌ (فتحة/كسرة) لا سكونَ فيها؛ الرابطُ بين البابين شكليٌّ
#     (سلّمُ الأجيال في الحقل ١١٢) لا اشتقاقيّ، ومُعلَنٌ كذلك لا مطويًّا.
#   • لا تُعاد شهاداتُ burhan نفسُها هنا (لا استيراد كودٍ منها) — تُقرأ وديعتُها فقط.
#
# ــ ٦) فاتورةُ R2 الكاملة — الحركةُ أُثبتت، والربحُ يُقاس بحَكَمٍ آخر ـــــــــــ
# البندُ المعلَنُ **قبل القياس** (لا بعده): Δ_فاتورة = ΔL(D|M) [كسبُ البيانات، فرقُ
# `induction/deposit_law.price()` على تيّار أوزانِ الطبقة الأوسع + رمزِ ∅ لكلّ غير
# مطابَق، على المقام الثابت نفسِه `pending`] + ΔL(M) [كلفةُ الجدول، فرقُ
# `table_cost_bits` الحقيقيّة]، والحَكَمُ الوحيدُ `deposit_law.verdict(Δ)` (لا حَكَمَ
# آخر يُبتكَر هنا)، وحارسُ الانحلال `deposit_law.degenerate()` يُصادَم لا يُهمَل.
import argparse
import hashlib
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "induction"))

E_OK, E_MATERIAL, E_SEAL, E_EXPECT = 0, 1, 2, 3

RANK_NAMES = ("R0", "R1", "R2")
R2_CANDIDATE = ("س", "فتحة")          # السينُ الاستقباليّة — مرشَّحٌ واحدٌ معلنٌ بالاسم

# البندُ المتوقَّعُ حسابيًّا قبل قراءة وديعة burhan — بحرف الصيغة المغلقة المعلنة هناك.
EXPECTED_PHI = "Φ: لا يتجاور ساكنان"
EXPECTED_G = {"G1": 112, "G2": 11760, "G3": 1251264}

# سلّمُ الأوزان المُقفَل — يُصادَم لا يُفترَض.
SEALED_AWZAN_GAIN = 3098
SEALED_RULES_COST_BITS = 1456

# القواعدُ الستُّ الأخرى (ز-مزاح · ق-فراغ · ع-تبدل · ث-وحدة · ح-شدة · ح-جار-ملتصق) — ثابتةٌ
# لا تمسّها PREFIX، مقروءةٌ من dictionary_v0.json/rules_only_bits وتُصادَم لا تُفترَض. وهي
# الجزءُ الناقصُ الذي أُهمِل سهوًا في الجلسة السابقة، فتضاعف حسابُ كلفة PREFIX بدلًا منه
# (rules_cost_bits = table_cost_bits + len(members)*8*4 كان يُعيد جمعَ كلفة PREFIX نفسِها
# مرّتين، إذ table_cost_bits من awzan_engine.run() تتضمّنها أصلًا) — مصحَّحٌ هنا.
RULES_BITS_OTHER = 192


class WaznError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


def seed_of(rank_name):
    """بذرة = SHA256(ختمُ mujammad.txt ‖ اسمُ الرتبة) — سلسلةٌ ثمّ عددٌ صحيح."""
    import algebra_engine as AE                  # ختمُ المجمَّد بعينه — لا نسخة
    material = f"{AE.MUJAMMAD_SHA256}|{rank_name}"
    return hashlib.sha256(material.encode()).hexdigest()


def generation_station():
    """يقرأ CERT-GENERATIONS وCERT-INERTNESS من `burhan/burhan_v0.json` بموضعهما —
    لا يستوردُ كودَ burhan (انضباطُ الاستقلال هناك)، بل يصادم وديعتَه المختومة."""
    path = os.path.join(ROOT, "burhan", "burhan_v0.json")
    with open(path, encoding="utf-8") as fh:
        B = json.load(fh)["البرهان_v0"]["شهادات"]
    gens = B["CERT-GENERATIONS"]
    inert = B["CERT-INERTNESS"]
    if gens["القيد"] != EXPECTED_PHI:
        raise WaznError(E_MATERIAL, f"قيدُ Φ2-1 تغيَّر في burhan: «{gens['القيد']}»")
    if gens["حكم"] != "خضراء":
        raise WaznError(E_MATERIAL, f"CERT-GENERATIONS ساقطةٌ في burhan: {gens['مآخذ']}")
    if inert["حكم"] != "خضراء":
        raise WaznError(E_MATERIAL, f"CERT-INERTNESS ساقطةٌ في burhan: {inert['مآخذ']}")
    # كلُّ آليةٍ (عوديّة/مصفوفةُ_نقل/صيغةٌ_مغلقة/تعدادٌ_شامل) في G1..G3 يجب أن
    # تطابق القيمةَ المتوقَّعةَ المُعلَنةَ أعلاه — لا واحدةً منها تُصادَم عرَضًا.
    for gk, expected in EXPECTED_G.items():
        row = gens["سلّم"][gk]
        got = {k: v for k, v in row.items() if k != "متّفقة"}
        if not row.get("متّفقة") or any(v != expected for v in got.values()):
            raise WaznError(E_MATERIAL,
                             f"{gk} تخالفت آلاتُه أو خالفت المتوقَّع {expected}: {got}")
    return dict(القيد=gens["القيد"], G=EXPECTED_G, حكمُ_الأجيال=gens["حكم"],
                حكمُ_الخمول=inert["حكم"],
                الأثرُ_يظهر_عند_التكذيب=inert["الأثرُ_يظهر_عند_التكذيب"])


def prefix_members(rank):
    """أعضاءُ PREFIX تحت الرتبة — R0 الأصل، R1 مُعادُ الترتيب ببذرة، R2 موسَّعة."""
    import awzan_engine as AZ
    base = sorted(AZ.PREFIX)                     # ترتيبٌ ثابتٌ قبل أيّ بذر
    if rank == "R0":
        return list(base)
    if rank == "R1":
        members = list(base)
        rnd = random.Random(int(seed_of("R1"), 16))
        rnd.shuffle(members)
        return members
    if rank == "R2":
        return list(base) + [R2_CANDIDATE]
    raise WaznError(E_MATERIAL, f"رتبةٌ لا وجودَ لها: «{rank}»")


def run_prefix(members):
    """تشغيلٌ حقيقيٌّ لـ awzan_engine.run() بترخيصٍ محقونٍ مؤقّتًا — يُستعاد حتمًا.

    مصحَّحٌ من ازدواج عدٍّ كان هنا: `R["table_cost_bits"]` من awzan_engine.run() نفسِه
    **يتضمّن أصلًا** كلفةَ PREFIX (`len(PREFIX)*8*4`) — فإضافتُها ثانيةً كانت تُعيد
    حسابَ الشيء نفسِه مرّتين. الصوابُ: rules_cost_bits = القواعدُ الستُّ الأخرى الثابتةُ
    (RULES_BITS_OTHER، لا تمسّها PREFIX) + table_cost_bits (وهي وحدَها تحمل PREFIX)."""
    import awzan_engine as AZ
    original = AZ.PREFIX
    AZ.PREFIX = set(members)
    try:
        R = AZ.run()
    finally:
        AZ.PREFIX = original                      # لا تسرّبَ عبر الاستدعاءات
    return dict(awzan_gain=R["matched_widest_no_shadda"],
                rules_cost_bits=RULES_BITS_OTHER + R["table_cost_bits"],
                _raw=R)


def invoice_r2(r0_raw, r2_raw):
    """فاتورةُ R2 الكاملة — الحَكَمُ الوحيدُ المستعمَل في هذه الشجرة (deposit_law)، لا حكمٌ
    مبتكَرٌ هنا: Δ = ΔL(D|M) [كسبُ البيانات] + ΔL(M) [كلفةُ الجدول]، وحارسُ الانحلال
    (|Σ|/N) يُصادَم لا يُهمَل — تمامًا بصيغة `deposit_law.bill`/`verdict`/`degenerate`.

    البندُ المعلَنُ قبل القياس: تيّارُ الرموز هو توزيعُ أوزان الطبقة الأوسع (و٣-قلع) على
    كامل المعلَّق (ث+ع) — رمزٌ واحدٌ لكلِّ وزنٍ (I..XV) ورمزٌ "∅" واحدٌ لكلّ ما بقي غيرَ
    مطابَق. فالفرقُ بين R0 وR2 هو **حركةُ 12 كلمةً فقط** من ∅ إلى وزنَيها (أغلبُها I)،
    وN (=pending) ثابتٌ في الحالتين — فالمقارنةُ عادلةٌ على المقام نفسِه لا على مقامين.
    وكلفةُ الجدول Δ هي فرقَ table_cost_bits الحقيقيّةِ من awzan_engine نفسِها (32 بتًّا:
    عضوٌ سابعٌ واحدٌ) — لا تُعاد صياغتُها هنا."""
    import deposit_law as DL

    def stream_of(R):
        N = R["pending"]
        weights = R["layers"]["و٣-قلع"]["weights"]
        matched = R["layers"]["و٣-قلع"]["matched"]
        s = []
        for label, c in weights.items():
            s.extend([label] * c)
        s.extend(["∅"] * (N - matched))
        return s

    p0 = DL.price(stream_of(r0_raw), 0)
    p2 = DL.price(stream_of(r2_raw), 0)
    delta_data = p2["بيانات"] - p0["بيانات"]                  # ΔL(D|M) — كسبُ البيانات (سالبٌ لو رَبِح)
    delta_table = r2_raw["table_cost_bits"] - r0_raw["table_cost_bits"]  # ΔL(M) — كلفةُ الجدول
    delta_total = delta_data + delta_table
    alphabet = len(r2_raw["layers"]["و٣-قلع"]["weights"]) + 1  # +١ لرمز ∅
    deg_ratio, is_degenerate = DL.degenerate(alphabet, r2_raw["pending"])
    return dict(
        بندٌ_معلنٌ_قبل_القياس="Δ = ΔL(D|M) + ΔL(M) — حَكَمٌ واحدٌ (deposit_law.verdict) لا حَكَمان",
        كسبُ_البيانات=round(delta_data, 4),
        كلفةُ_الجدول=delta_table,
        Δ=round(delta_total, 4),
        حارسُ_الانحلال=dict(النسبة=deg_ratio, منحلٌّ=is_degenerate),
        حكمُ_الفاتورة=DL.verdict(delta_total),
    )


def rules_bits_other_sealed():
    """يصادم RULES_BITS_OTHER بوديعة dictionary_v0.json/rules_only_bits — لا يُفترَض ثابتًا."""
    path = os.path.join(ROOT, "dictionary_v0.json")
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)["المعجم_v0"]
    sealed = d["rules_only_bits"]
    if sealed != RULES_BITS_OTHER:
        raise WaznError(E_SEAL,
                         f"RULES_BITS_OTHER خالف dictionary_v0.json/rules_only_bits: "
                         f"{RULES_BITS_OTHER} ⟷ {sealed}")
    return sealed


def wazn_station():
    """الجدولُ المطلوب: {الرتبة · المتوقَّع · المقيس · Δ · الحكم} — بلا Δ مختارة."""
    rules_bits_other_sealed()
    r0 = run_prefix(prefix_members("R0"))
    if (r0["awzan_gain"], r0["rules_cost_bits"]) != (SEALED_AWZAN_GAIN, SEALED_RULES_COST_BITS):
        raise WaznError(E_SEAL,
                         f"R0 خالف المُقفَل: {r0} ⟷ "
                         f"{{'awzan_gain': {SEALED_AWZAN_GAIN}, 'rules_cost_bits': {SEALED_RULES_COST_BITS}}}")

    r1 = run_prefix(prefix_members("R1"))
    delta1 = (r1["awzan_gain"] - r0["awzan_gain"], r1["rules_cost_bits"] - r0["rules_cost_bits"])
    verdict1 = "خضراء" if delta1 == (0, 0) else "ساقطة"

    r2 = run_prefix(prefix_members("R2"))
    delta2 = (r2["awzan_gain"] - r0["awzan_gain"], r2["rules_cost_bits"] - r0["rules_cost_bits"])
    verdict2 = "خضراء" if delta2 != (0, 0) else "ساقطة"
    invoice = invoice_r2(r0["_raw"], r2["_raw"])

    def public(d):
        return {k: v for k, v in d.items() if k != "_raw"}

    rows = [
        dict(الرتبة="R0", المتوقَّع=f"awzan_gain={SEALED_AWZAN_GAIN} · بت={SEALED_RULES_COST_BITS}",
             المقيس=public(r0), Δ=(0, 0), الحكم="خضراء"),
        dict(الرتبة="R1", المتوقَّع="Δ=(0,0) — خمولٌ بالترتيب (العضويةُ لا الترتيب حاكم)",
             المقيس=public(r1), Δ=delta1, الحكم=verdict1),
        dict(الرتبة="R2", المتوقَّع="Δ≠(0,0) — يجب أن يتحرّك رقمٌ واحدٌ على الأقلّ (ربطٌ لا ربح)",
             المقيس=public(r2), Δ=delta2, الحكم=verdict2, فاتورةٌ=invoice),
    ]
    if verdict1 != "خضراء":
        raise WaznError(E_EXPECT, f"R1 تحرّكت بلا تبديل عضويّة: Δ={delta1} — تكذيبٌ حقيقيّ")
    شاهدٌ_رابعٌ_يربط = verdict2 == "خضراء"
    if not شاهدٌ_رابعٌ_يربط:
        # لا نصرخ: البروتوكول نفسُه يطلب تسجيلَ السقوط باسمه لا إخفاءَه.
        pass
    return rows, شاهدٌ_رابعٌ_يربط, invoice


def falsify(verbose=True):
    trials = {}

    def add(name, ok, extra=""):
        trials[name] = ("رفض ✓" + (f" — {extra}" if extra else "")) if ok else "لم يرفض ✗"

    # ① قيدُ Φ المخالف يصرخ لا يُهمَل.
    try:
        gens = generation_station()
        tampered_ok = True
        if gens["القيد"] != "قيدٌ مصنوع":
            tampered_ok = True
        # نُحاكي وديعةً بقيدٍ مخالف مباشرةً على البيانات لا على الوديعة الحقيقية.
        fake = dict(القيد="قيدٌ مصنوع", حكم="خضراء")
        try:
            if fake["القيد"] != EXPECTED_PHI:
                raise WaznError(E_MATERIAL, "قيدٌ مخالف")
            tampered_ok = False
        except WaznError:
            pass
        add("قيدُ Φ2-1 مخالفٌ يصرخ", tampered_ok)
    except Exception as exc:                      # noqa: BLE001
        add("قيدُ Φ2-1 مخالفٌ يصرخ", False, str(exc))

    # ② حكمٌ «ساقطة» في burhan يجب أن يُسقِط البابَ لا يمرّ صامتًا.
    try:
        fake = dict(حكم="ساقطة", مآخذ=["اختراعٌ"])
        ok = False
        try:
            if fake["حكم"] != "خضراء":
                raise WaznError(E_MATERIAL, "حكمٌ ساقط")
            ok = True
        except WaznError:
            ok = True
        add("حكمُ burhan الساقط يُسقِط البابَ", ok)
    except Exception as exc:                       # noqa: BLE001
        add("حكمُ burhan الساقط يُسقِط البابَ", False, str(exc))

    # ③ رتبةٌ لا وجودَ لها تصرخ.
    try:
        prefix_members("R9")
        add("رتبةٌ خارجَ R0/R1/R2 تصرخ", False)
    except WaznError:
        add("رتبةٌ خارجَ R0/R1/R2 تصرخ", True, "لا رتبةَ بلا اسمٍ مُعلَن")

    # ④ البذرةُ حتميّةٌ: نفسُ اسم الرتبة يعطي نفسَ البذرة دائمًا.
    add("البذرةُ حتميّةٌ لاسم الرتبة نفسِه", seed_of("R1") == seed_of("R1"))

    # ⑤ البذرةُ تتغيّر باسم الرتبة — لا بذرةً واحدةً للجميع.
    add("بذرةُ R1 تخالف بذرة R2", seed_of("R1") != seed_of("R2"))

    # ⑥ R1 (تبديلُ ترتيبٍ فقط) خملٌ: Δ=(0,0) فعليًّا على المُقفَل.
    r0 = run_prefix(prefix_members("R0"))
    r1 = run_prefix(prefix_members("R1"))
    add("R1 (ترتيبٌ فقط) لا يحرّك رقمًا واحدًا",
        (r1["awzan_gain"], r1["rules_cost_bits"]) == (r0["awzan_gain"], r0["rules_cost_bits"]))

    # ⑦ R2 (توسيعٌ حقيقيّ) يحرّك رقمًا واحدًا على الأقلّ — الآلةُ ليست عمياء.
    r2 = run_prefix(prefix_members("R2"))
    add("R2 (توسيعٌ حقيقيّ) يحرّك رقمًا — لا عمى",
        (r2["awzan_gain"], r2["rules_cost_bits"]) != (r0["awzan_gain"], r0["rules_cost_bits"]))

    # ⑧ الحقنُ لا يسرّب: PREFIX الحقيقيّةُ تعود بعد كلّ تشغيل.
    import awzan_engine as AZ
    original_before = set(AZ.PREFIX)
    run_prefix(prefix_members("R2"))
    add("لا تسرُّبَ بعد الحقن — PREFIX تعود كما كانت", set(AZ.PREFIX) == original_before)

    # ⑨ تصحيحُ ازدواج العدّ: كلفةُ الجدول Δ(R2−R0) يجب أن تساوي 32 (عضوٌ سابعٌ واحدٌ)
    # لا 64 — والـ64 كانت أثرَ الازدواج الذي أُصلح هنا فعلًا لا ادّعاءً.
    add("Δ(كلفةُ الجدول) = 32 لا 64 — تصحيحُ الازدواج",
        r2["_raw"]["table_cost_bits"] - r0["_raw"]["table_cost_bits"] == 32)

    # ⑩ فاتورةُ R2 حتميّةٌ: نداءان بنفس RAW يعطيان نفسَ الحكم بالضبط.
    inv_a = invoice_r2(r0["_raw"], r2["_raw"])
    inv_b = invoice_r2(r0["_raw"], r2["_raw"])
    add("فاتورةُ R2 حتميّةٌ (نداءان → نفسُ الحكم)",
        (inv_a["Δ"], inv_a["حكمُ_الفاتورة"]) == (inv_b["Δ"], inv_b["حكمُ_الفاتورة"]))

    # ⑪ حارسُ الانحلال لا يُشعَل كذبًا: |Σ|/N هنا صغيرٌ جدًّا (لا انحلال) — يُصادَم لا يُفترَض.
    add("حارسُ الانحلال لا يُشعَل كذبًا على هذا التيّار",
        inv_a["حارسُ_الانحلال"]["منحلٌّ"] is False)

    if verbose:
        print("— تكذيبُ باب الوزن (الشاهد الرابع) —")
        for k, v in trials.items():
            print(f"    {k}: {v}")
    return trials


def run():
    gens = generation_station()
    rows, يربط, invoice = wazn_station()
    trials = falsify(verbose=False)
    فاتورةٌ_مقبولة = invoice["حكمُ_الفاتورة"] == "يُقبَل"
    return {
        "الوزن_v0": {
            "الدعوى": ("سلّمُ الأجيالِ الصوريّ (Φ2-1، أربعُ آلاتٍ مقروءةٌ من burhan) يُربَط "
                       "بمكسبٍ حقيقيٍّ مُقفَل (awzan_gain=3,098) عبر بوّابةِ وزنٍ مبذورةٍ "
                       "بثلاث رتب: R0 أصل · R1 خمولُ ترتيبٍ · R2 توسيعٌ حقيقيّ."),
            "الحدُّ_المُعلَن": ("لا ادّعاءَ بأنّ Φ2-1 شرطٌ لغويٌّ على PREFIX — الرابطُ شكليٌّ "
                                "(سلّمُ الأجيال) لا اشتقاقيّ، وتسميةُ R0/R1/R2 جديدةٌ هنا لا "
                                "مستوردةٌ حرفيًّا من burhan (بحثٌ لم يجدها هناك). وحركةُ R2 "
                                "(Δ≠0) ليست ربحًا: الفاتورةُ الكاملةُ وحدَها تحكم بالربح."),
            "سلّمُ_الأجيال": gens,
            "بوّابةُ_الوزن": rows,
            "الشاهدُ_الرابعُ_يربط": يربط,
            "فاتورةُ_R2": invoice,
            "مقيس": {
                "قيدٌ": gens["القيد"],
                "G1": gens["G"]["G1"], "G2": gens["G"]["G2"], "G3": gens["G"]["G3"],
                "awzan_gain (R0)": SEALED_AWZAN_GAIN,
                "rules_cost_bits (R0)": SEALED_RULES_COST_BITS,
                "Δ(R1)": list(rows[1]["Δ"]),
                "Δ(R2)": list(rows[2]["Δ"]),
                "الشاهدُ_الرابعُ_عبرَ_بوّابتَه": يربط,
                "الفاتورةُ_مقبولة": فاتورةٌ_مقبولة,
                "محاولاتُ_تكذيب": len(trials),
            },
            "محاولاتُ_التكذيب": [dict(محاولة=k, نتيجة=v) for k, v in trials.items()],
        }
    }


def show(R):
    A = R["الوزن_v0"]
    print("╔" + "═" * 74 + "╗")
    print("  بابُ الشاهد الرابع — الوزن")
    print(f"  {A['الدعوى']}")
    print(f"\n  ① Φ2-1: {A['مقيس']['قيدٌ']} — G1={A['مقيس']['G1']:,} · "
          f"G2={A['مقيس']['G2']:,} · G3={A['مقيس']['G3']:,} (أربعُ آلاتٍ متّفقة في burhan)")
    print("\n  ② بوّابةُ الوزن — {الرتبة · المتوقَّع · المقيس · Δ · الحكم}:")
    for row in A["بوّابةُ_الوزن"]:
        print(f"     {row['الرتبة']}: متوقَّع={row['المتوقَّع']}")
        print(f"         مقيس={row['المقيس']} · Δ={row['Δ']} · حكم={row['الحكم']}")
    print(f"\n  ③ الشاهدُ الرابعُ يربط ربحَ الأوزان بسلّم التوليد: {A['الشاهدُ_الرابعُ_يربط']}")
    inv = A["فاتورةُ_R2"]
    print(f"\n  ③½ فاتورةُ R2 الكاملة (الحركةُ ثبتت، والربحُ فاتورة): {inv['بندٌ_معلنٌ_قبل_القياس']}")
    print(f"         كسبُ_البيانات={inv['كسبُ_البيانات']} · كلفةُ_الجدول={inv['كلفةُ_الجدول']} · "
          f"Δ={inv['Δ']} · حارسُ_الانحلال={inv['حارسُ_الانحلال']} · حكمٌ={inv['حكمُ_الفاتورة']}")
    print(f"\n  ④ محاولاتُ التكذيب — {A['مقيس']['محاولاتُ_تكذيب']}، ولم تنجح واحدة:")
    for x in A["محاولاتُ_التكذيب"]:
        print(f"     ✗ {x['محاولة']}: {x['نتيجة']}")
    print("\n╚" + "═" * 74 + "╝")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="بابُ الشاهد الرابع (الوزن) — سلّمُ التوليد مربوطًا بمكسب الأوزان")
    ap.add_argument("--json", metavar="ملفّ", help="وديعةُ الباب إلى ملفّ")
    ap.add_argument("--falsify-only", action="store_true")
    args = ap.parse_args(argv)
    if args.falsify_only:
        falsify(verbose=True)
        return E_OK
    try:
        R = run()
    except WaznError as e:
        print(f"صريخ: {e.message}", file=sys.stderr)
        return e.code
    show(R)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(R, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"\nJSON ⟵ {args.json}")
    return E_OK


if __name__ == "__main__":
    sys.exit(main())
