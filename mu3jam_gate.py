# mu3jam_gate.py — بابُ المعجم: الجسرُ الثلاثيُّ يُقاس، ولا يُستشهَد به.
#
# ــ ٠) العلّةُ التي يفتحها هذا الباب ــــــــــــــــــــــــــــــــــــــــــــــــــ
# دعوى «جسرِ المعجم» جاءت بثلاثةِ أرقام: حضورٌ 20/20 · اتساعٌ 1,132 عائلة · ورودٌ
# 5,450 موضعًا. وقاعدةُ الوسم التي أعطتها **لم تُعلَن**، ولمّا كُشفت بالمطابقة كانت
# **المتتاليةَ الجزئية**: مادّةٌ «موسومةٌ» في الكلمة إن وقعت حروفُها فيها على ترتيبها
# ولو تفرّقت. فبها صارت «عليهم» و«لعلكم» و«نجعلهم» من مادّة علم، و«أصحاب» و«الحطب»
# من مادّة حبّ. وثلاثةُ الأرقام ليست خطأً في العدّ بل **خطأٌ في المقياس**: قاعدةٌ
# تطابق كلَّ شيءٍ لا تفصل شيئًا.
#
# وهذا البابُ يقلب الترتيب — بأمر المالك:
#   ① **تُعلَن قاعدةُ الوسم قبل القياس** ـ مكتوبةً في بايتات هذا الملفّ.
#   ② **يُستبدَل بالمتتالية إسنادٌ إلى جذورٍ مشتقّةٍ بقاعدةٍ مسعَّرة** — قوالبُ I–XV
#      في `algebra_engine` عبر `awzan_engine`، وثمنُ جدولها مقيسٌ مُودَعٌ
#      (`awzan_v0.table_cost_bits`)، والقائمةُ مغلقةٌ بـ`awzan_v0.roots_widest`.
#   ③ **يُصادَم الناتجُ بجدول ابن فارس المختوم** — فإن غابت بايتاتُه فغيابٌ معلن،
#      لا قياسٌ مؤجَّلٌ بصمت ولا رقمٌ يُنسَب إلى غائب.
#   ④ **يُعرَض على إحدى عشرةَ فرقةَ مثل** — فما غلبَها أُودِع، وما لم يغلبها
#      **سُمِّي دَينًا بلا رقم** ولم يُكتَب في عمود المقيس.
#
# ــ ١) قاعدةُ الوسم — مُعلَنةٌ بحرفها قبل أن يُقاس بها شيء ــــــــــــــــــــــــــ
# كلمةٌ تُوسَم بمادّةٍ **إن وإن فقط** تحقّق الشرطان معًا:
#   أ) أعطى `awzan_engine.hit(الكلمةُ، "و٣-قلع")` جذرًا — أي طابقت الكلمةُ قالبًا من
#      القوالب الخمسةَ عشرَ بعد قلعِ السوابق المعلنة، حرفًا بحرفٍ وشدّةً بشدّة.
#   ب) ووقع ذلك الجذرُ — بعد تسوية الهمزات والألفات المعلنةِ في `awzan_engine.HAMZ`
#      — في **القائمة المغلقة** `awzan_v0.roots_widest`.
# وما خرج عن الشرطين فغيرُ موسوم: **لا يُنسَب إلى مادّةٍ بالحدس ولا بالمتتالية**.
# ونصيبُ الموسوم من المقام مقيسٌ معروضٌ (لا يُدَّعى أنّه المقامُ كلُّه).
#
# ــ ٢) الأرجلُ الثلاث — ثلاثةُ مقاماتٍ لا مقامٌ واحد ـــــــــــــــــــــــــــــــــ
#   • **المدخل ↔ الكلمة**: حضورُ المادّة في القائمة المشتقّة، ومواضعُ ورودها.
#   • **المادة ↔ العائلة**: اتساعُها — كم صورةً مختلفةً ابتنت في المجمَّد.
#   • **الشاهد ↔ الآية**: شبكةُ (مادة × آية) على مقامنا.
# ثمّ تُصادَم الموادُّ المقيسةُ بجدول ابن فارس المختوم في اتجاهٍ واحدٍ معلن
# (**أمُدرَجةٌ عنده؟**) — وبايتاتُه شرطُ التشغيل لا رفاهية: إن غابت سقط البابُ
# بالمخرج 3 ولم يُكتَب رقمٌ منسوبٌ إلى غائب.
# ولا تُجمَع الثلاثةُ في رقمٍ واحد: مقاماتُها مختلفة — وهو عينُ ما يمنعه حارسُ
# `jumla_links` حين منع جمعَ «داخل الآية» بـ«العبور».
#
# ــ ٣) الحَكَمُ المميِّز: ضوابطُ المثل لا الحكمُ المفرد ــــــــــــــــــــــــــــــ
# عدَّةُ الفرقِ `madlul_gate.RIVALS` تُقرَأ من بابها لا تُكتَب ههنا — وقد قِيس هناك
# أنّ الحكمَ المفردَ خاوٍ. وههنا ضابطان معلنان لا واحد، لأنّ المقيسَين مختلفان:
#   • **ضابطٌ مشتقٌّ مطابقُ الحجم** (للورود والاتساع والشبكة): فرقةٌ من موادَّ
#     مشتقّةٍ بالعدد نفسِه (٢٠) وإطلاقُها داخل نطاقٍ معلن ±`BAND` من إطلاق العشرين
#     — فلا يُشترى فضلٌ بالحجم.
#   • **ضابطٌ مصنوعٌ** (للحضور): تباديلُ حروفِ العشرين نفسِها — فالضابطُ المشتقُّ
#     **خاوٍ في الحضور بالبناء** (كلُّ مادّةٍ مشتقّةٍ حاضرةٌ بتعريفها)، ويُعلَن خواؤه
#     ولا يُطوى.
#
# ــ ٤) الحدُّ المُعلَن: ما لا يقوله هذا الباب ـــــــــــــــــــــــــــــــــــــــــ
# لا يقول إنّ العشرين ليست موادَّ العربية، ولا إنّ ابن منظورٍ أخطأ. يقول شيئًا
# واحدًا مقيسًا: **بهذه القاعدةِ المعلنةِ وعلى هذا المقامِ المختوم، حضورُها يفصل
# واتساعُها لا يفصل** — وما لم يفصل يُسمّى دَينًا بلا رقم، لا يُزيَّن ولا يُطوى.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بايتاتٌ غائبة · 4 ختمٌ خالف وديعتَه.
#
# التشغيل:
#   python mu3jam_gate.py                 تقريرٌ معدودٌ على stdout
#   python mu3jam_gate.py --json <ملفّ>   الوديعةُ إلى ملفّ (مولِّدُ الأختام)
#
# ⚑ ولا يُمَسُّ معجمٌ ولا كلفةٌ سابقة: هذا بابُ قياسٍ على المجمَّد، لا تصنيفُ كلمات.
import argparse
import json
import os
import random
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "induction"))

import awzan_engine as AW                        # قوالبُ I–XV وقاعدةُ القلع — لا نسخةَ ثانية
import madlul_gate as MG                         # عدَّةُ فرقِ المثل من بابها الوحيد
import maqayis_layer as MQ                       # ختمُ جدول ابن فارس ومقروؤه
import ta3allum_gate as TG                       # المقامُ والمسعِّرُ والبذرةُ المعلنة
from deposit_law import verdict

E_USAGE = 2
E_MISSING = 3
E_SEAL = 4

AWZAN_JSON = os.path.join(ROOT, "awzan_v0.json")


class Mu3jamError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ═══ الإعلاناتُ المجمَّدةُ قبل القياس ═══════════════════════════════════════════════
# ① القائمةُ المغلقةُ المعلنة: عشرون مادّةً تراثيّةً — بحرفها كما أُعلنت، و«ح ب ب»
#    مكتوبةٌ مضاعَفةً لا مطويّةً إلى «حب»: فالقائمةُ تُقاس كما أُعلنت لا كما يُشتهى.
MATERIALS = ("كتب", "قرأ", "علم", "ملك", "قول", "عمل", "رحم", "عبد", "كلم", "نور",
             "هدي", "قلب", "يقن", "عدل", "سلم", "حبب", "ذكر", "صلح", "جهد", "شهد")

# ② قاعدةُ الوسم — نصُّها في البايتات، وتنفيذُها `tag_of` أدناه بحرفه.
TAG_RULE = ("كلمةٌ تُوسَم بمادّةٍ إن أعطى `awzan_engine.hit(w, 'و٣-قلع')` جذرًا، "
            "ووقع الجذرُ — بتسوية `awzan_engine.HAMZ` — في القائمة المغلقة "
            "`awzan_v0.roots_widest`. وما عداه غيرُ موسوم: لا متتاليةَ جزئيةً "
            "ولا حدسَ جذرٍ ولا معجمَ صورٍ مكتوبًا باليد")

# ③ القاعدةُ المتروكة — تُقاس ولا تُستعمَل حَكَمًا. وإنّما تُقاس لأنّ تركَها دعوى:
#    فلتُصادَم بعددها لا بقولنا إنّها تطابق كلَّ شيء.
LEFT_RULE = ("المتتاليةُ الجزئية: حروفُ المادّة واقعةٌ في الكلمة على ترتيبها ولو "
             "تفرّقت — القاعدةُ التي أعطت 20/20 و1,132 و5,450، وتُقاس ههنا لتُصادَم")

# ④ نطاقُ مطابقةِ الحجم في الضابط المشتقّ: فرقةٌ إطلاقُها خارج [1−BAND, 1+BAND] من
#    إطلاق العشرين لا تُقبَل ضابطًا — فلا يُشترى فضلٌ بالحجم ولا يُباع به.
BAND = 0.2

# ⑤ مادّةٌ مصنوعةٌ لا تقع في القائمة المشتقّة — تُعرَض على المسعِّر في `falsify`
#    ليُثبَت أنّه **يصرخ ولا يُسعِّر فراغًا**. ولا تُعَدُّ مادّةً ولا تدخل ميدانًا.
FABRICATED_MATERIAL = "ڤڠث"

# ⑥ الأحكامُ المجمَّدة: تُشتقُّ من مواضعها في كلِّ تشغيلٍ وتُصادَم بفارق صفرٍ في `run`.
#    وبايتاتُ ابن فارس شرطُ التشغيل: لا يُقاس شاهدٌ على غائبٍ ولا يُؤجَّل بصمت.
SEALED_MU3JAM = {
    "كلماتُ المقام": 77801,
    "موادُّ القائمة المشتقّة": 524,
    "مواضعُ موسومة": 5560,
    "العشرون المعلنة": 20,
    "منها في القائمة المشتقّة": 14,
    "غيابٌ معلن": 6,
    "ورودُ العشرين": 129,
    "اتساعُ العشرين": 29,
    "آياتُ الشبكة": 118,
    "مدرَجةٌ عند ابن فارس": 14,
    "أرجلٌ مُودَعةٌ بالبرهان": 2,
    "ديونٌ بلا رقم": 3,
    "محاولاتُ_تكذيب": 8,
}


# ═══ ① المقامُ والقائمةُ المشتقّة ═══════════════════════════════════════════════════
def nz(text):
    """تسويةُ الهمزات والألفات المعلنةُ في `awzan_engine` بعينها — لا تسويةَ ثانية."""
    return "".join(AW.HAMZ.get(ch, ch) for ch in text)


def closed_list(path=AWZAN_JSON):
    """القائمةُ المغلقة: جذورُ الطبقة الأوسعِ المُودَعةُ في `awzan_v0.json` بتسويتها.

    ولا تُشتَقُّ ههنا اشتقاقًا ثانيًا: تُقرأ من وديعةِ حلقةِ الأوزان — فمصدرُ
    الحقيقة واحدٌ، ولو تغيّرت هناك تغيّر هذا البابُ بمقياسه لا بيدنا.
    """
    if not os.path.isfile(path):
        raise Mu3jamError(E_MISSING, f"وديعةُ حلقة الأوزان غائبةٌ: {path}")
    R = json.load(open(path, encoding="utf-8"))["الأوزان_v0"]
    roots = {nz(r) for r in R["roots_widest"]}
    if not roots:
        raise Mu3jamError(E_SEAL, "قائمةُ الجذور خاويةٌ — لا قائمةَ مغلقةَ تُقاس")
    return roots, R["widest"], R["table_cost_bits"]


def tag_of(word, closed):
    """قاعدةُ الوسم بحرفها — والشرطان معًا أو لا وسم."""
    hit = AW.hit(word, "و٣-قلع")
    if hit is None:
        return None
    root = nz(hit[1])
    return root if root in closed else None


def tagging(closed):
    """وسمُ المقام كلِّه مرّةً واحدة: إزاحةُ الكلمة ⟼ مادّتُها، وآيةُ كلِّ إزاحة.

    والإزاحاتُ **هي هي** إزاحاتُ `ta3allum_gate.corpus_surfaces`: التحليلُ الغنيُّ
    في `awzan_engine.tokenize_rich` يُصادَم بـ`parse_verses` بفارق صفرٍ عند قراءته،
    ويُصادَم ههنا ثانيةً بعددِ الآيات وعددِ كلماتِ كلِّ آية — فلا تنزاح خانة.
    """
    try:
        verses, stream, _ = TG.corpus_surfaces()
    except TG.Ta3allumError as exc:
        raise Mu3jamError(exc.code, exc.message) from exc
    if not os.path.isfile(AW.CORPUS):
        raise Mu3jamError(E_MISSING, f"بايتاتُ المجمَّد غائبةٌ: {AW.CORPUS}")
    rich = AW.tokenize_rich(AW.CORPUS)
    if [len(v) for v in verses] != [len(v) for v in rich]:
        raise Mu3jamError(E_SEAL, "تقطيعُ الآيات اختلف بين القارئَين — لا وسمَ على إزاحةٍ منزاحة")
    assign, verse_of, idx = {}, [], 0
    for vi, words in enumerate(rich):
        for word in words:
            material = tag_of(word, closed)
            if material is not None:
                assign[idx] = material
            verse_of.append(vi)
            idx += 1
    if idx != len(stream):
        raise Mu3jamError(E_SEAL, f"مقامُ الوسم {idx} ≠ مقامُ الصور {len(stream)}")
    return verses, stream, verse_of, assign


# ═══ ② الأرجلُ الثلاث — تُقاس مفرَدةً ولا تُجمَع ═════════════════════════════════════
def legs(materials, stream, verse_of, assign):
    """ورودُ فرقةٍ من الموادّ واتساعُها وآياتُها — ثلاثةُ مقاماتٍ في مخرَجٍ واحد."""
    wanted = set(materials)
    places = [i for i, m in assign.items() if m in wanted]
    return dict(ورود=len(places),
                اتساع=len({stream[i] for i in places}),
                آيات=len({verse_of[i] for i in places}),
                حضور=len({assign[i] for i in places}))


def material_rows(stream, verse_of, assign, closed):
    """كلُّ مادّةٍ من العشرين بصفِّها — والغائبةُ تُعلَن غيابًا معلنًا لا تُحذَف."""
    rows = []
    for raw in MATERIALS:
        material = nz(raw)
        places = [i for i, m in assign.items() if m == material]
        rows.append(dict(
            مادة=raw, مقيسة=material,
            في_القائمة=bool(material in closed),
            ورود=len(places),
            اتساع=len({stream[i] for i in places}),
            آيات=len({verse_of[i] for i in places}),
            صور=sorted({stream[i] for i in places})[:6],
            حال=("مقيسة" if material in closed else
                 "غيابٌ معلن — لا تشتقُّها القاعدةُ المسعَّرةُ على هذا المقام")))
    return rows


# ═══ ③ ضوابطُ المثل — ضابطان معلنان لا واحد ═════════════════════════════════════════
def fire_of(materials, assign):
    wanted = set(materials)
    return {i for i, m in assign.items() if m in wanted}


def split_of(stream, materials, assign):
    """فاتورةُ الوصف الأدنى بمكيال `ta3allum_gate` — وفراغُ الإطلاق يُصرَخ به."""
    fire = fire_of(materials, assign)
    if not fire:
        raise Mu3jamError(E_SEAL, "فرقةٌ لا تُطلِق موضعًا — لا فاتورةَ تُقاس على فراغ")
    try:
        return TG.split_bill(stream, fire, tuple(materials))
    except TG.Ta3allumError as exc:
        raise Mu3jamError(exc.code, exc.message) from exc


def derived_rivals(stream, verse_of, assign, closed_pool, size, fired):
    """الضابطُ المشتقُّ مطابقُ الحجم: `RIVALS` فرقةً ببذرةٍ معلنةٍ وبنطاقٍ معلن."""
    rng = random.Random(TG.CONTROL_SEED)
    counts = Counter(assign.values())
    lo, hi = int(fired * (1 - BAND)), int(fired * (1 + BAND))
    out, tries = [], 0
    while len(out) < MG.RIVALS:
        tries += 1
        if tries > 500000:
            raise Mu3jamError(E_SEAL, "لم تكتمل فرقُ المثل داخل النطاق المعلن — لا حكمَ بضابطٍ ناقص")
        cohort = rng.sample(sorted(closed_pool), size)
        if not lo <= sum(counts[m] for m in cohort) <= hi:
            continue
        row = legs(cohort, stream, verse_of, assign)
        row["موادّ"] = list(cohort)
        row["Δ"] = round(split_of(stream, cohort, assign), 1)
        out.append(row)
    return out, tries


def fabricated_cohorts(size):
    """الضابطُ المصنوع: تباديلُ حروفِ العشرين نفسِها — التوزيعُ الحرفيُّ هو هو."""
    rng = random.Random(TG.CONTROL_SEED)
    letters = [ch for m in MATERIALS for ch in nz(m)]
    step = len(letters) // size
    out = []
    for _ in range(MG.RIVALS):
        pool = letters[:]
        rng.shuffle(pool)
        out.append([("".join(pool[i * step:(i + 1) * step])) for i in range(size)])
    return out


def left_rule_presence(stream):
    """القاعدةُ المتروكةُ مقيسةً: حضورُ العشرين وحضورُ المصنوعة بالمتتالية الجزئية."""
    def inside(material, word):
        k = 0
        for ch in word:
            if ch == material[k]:
                k += 1
                if k == len(material):
                    return True
        return False

    words = [nz(s) for s in stream]
    real = sum(1 for m in MATERIALS if any(inside(nz(m), w) for w in words))
    places = sum(1 for w in words if any(inside(nz(m), w) for m in MATERIALS))
    fab = [sum(1 for f in cohort if any(inside(f, w) for w in words))
           for cohort in fabricated_cohorts(len(MATERIALS))]
    return dict(قاعدة=LEFT_RULE, حضورُ_العشرين=real, مواضعُ_العشرين=places,
                حضورُ_المصنوعة=fab, أعلى_المصنوعة=max(fab),
                تفصل=bool(max(fab) < real / 2),
                بيان=("خمسَ عشرةَ مادّةً مصنوعةً من عشرين تنالها هذه القاعدةُ أيضًا — "
                      "فالحضورُ بها لا يفصل، وعليها بُنيت أرقامُ الملحق"))


# ═══ ④ مصادمةُ ابن فارس — وغيابُ البايتات وضعٌ معلن ═════════════════════════════════
def maqayis_entries():
    """مدخلُ ابن فارس بمفتاحٍ مسوًّى — وبايتاتُه شرطٌ لا يُتجاوَز.

    ولا يُقاس شاهدٌ على غائب: إن غابت البايتاتُ سقط البابُ بالمخرج 3 ومهرُها
    معروضٌ (البصمةُ والطولُ والمصدرُ وطريقُ الجلب) — كما يسقط `mihwar_gate`،
    فالقاعدةُ واحدةٌ في المستودع: **لا رقمَ يُنسَب إلى جدولٍ ليس على القرص**.
    """
    if not os.path.isfile(MQ.TABLE):
        raise Mu3jamError(E_MISSING,
                          f"جدولُ «مقاييس اللغة» غائبٌ عن القرص — ولا يُقاس شاهدٌ على "
                          f"غائب. مهرُه: {MQ.SEAL[:12]}… · {MQ.SEAL_BYTES} بايتًا · "
                          f"{MQ.SOURCE} · ./fetch_maqayis.sh")
    table = MQ.read_table()
    entries = {}
    for row in table:
        entries.setdefault(row["root_full"], row)
    by_norm = {}
    for key, row in entries.items():
        by_norm.setdefault(nz(key), row)
    return table, entries, by_norm


def maqayis_station(rows, by_norm, table, entries):
    """الرجلُ الثالثة: إدراجُ موادِّنا المقيسةِ عند ابن فارس — مصادمةٌ باتجاهٍ معلن."""
    measured = [r for r in rows if r["في_القائمة"]]
    inside = [r["مادة"] for r in measured if nz(r["مقيسة"]) in by_norm]
    axes = Counter()
    for r in measured:
        entry = by_norm.get(nz(r["مقيسة"]))
        axis = (entry or {}).get("semantic_axes", "").strip()
        if axis:
            axes[axis] += 1
    return dict(
        حال="مُصادَمٌ ببصمته", مصدر=MQ.SOURCE, sha256=MQ.SEAL, طول=MQ.SEAL_BYTES,
        سجلات=len(table), جذورٌ_متمايزة=len(entries),
        مقيس=dict(مقيسةٌ_عندنا=len(measured), مدرَجةٌ_عند_ابن_فارس=len(inside),
                  غيرُ_مدرَجة=len(measured) - len(inside),
                  أسماءُ_المدرَجة=inside, محاورُ_دلالية=dict(axes.most_common(8))),
        بيان=("المصادمةُ في اتجاهٍ واحدٍ مُعلَن: أمُدرَجةٌ موادُّنا المقيسةُ عنده؟ "
              "ولا يُقاس العكسُ — فمقامُ المعجمِ ليس مقامَنا"))


# ═══ ⑤ الحكم: ما غلبَ يُودَع، وما لم يغلب يُسمّى دَينًا بلا رقم ══════════════════════
def judge(name, measured, rivals, key, higher_is_better, note):
    """حكمُ رجلٍ واحدة — والمقارنةُ بأدنى/أعلى المثل جميعًا لا بوسيطها."""
    values = [r[key] for r in rivals]
    if higher_is_better:
        beats, edge = measured > max(values), max(values)
    else:
        beats, edge = measured < min(values), min(values)
    return dict(رجل=name, مقيس=measured, حدُّ_المثل=edge, ضوابطُ_المثل=len(values),
                غلبَ_المثل=bool(beats),
                حكم=("مُودَعةٌ بالبرهان" if beats else "دَينٌ بلا رقم — لم يغلب ضوابطَ المثل"),
                بيان=note)


# ═══ ⑥ محاولاتُ التكذيب — تُشغَّل ولا تُقرَأ ═══════════════════════════════════════
def falsify(stream, verse_of, assign, closed, presence, left, verses, maqayis, by_norm):
    T = []

    # ① الوسمُ ليس تسميةً للمقام: لو نُسب أكثرُ من نصفِ الكلمات لمادّةٍ لكانت
    #    القاعدةُ اسمًا للمقام لا قاعدةً فيه (حدُّ `ta3allum_gate.COVER_CEILING`).
    share = len(assign) / len(stream)
    T.append(("الوسمُ ينسب نصفَ المقام فأكثرَ — تسميةٌ لا قاعدة",
              share >= TG.COVER_CEILING))

    # ② مادّةٌ مصنوعةٌ لا تقع في القائمة: يجب أن يُصرَخ، لا أن تُسعَّر بفاتورةِ فراغ.
    try:
        split_of(stream, (FABRICATED_MATERIAL,), assign)
        screamed = False
    except Mu3jamError:
        screamed = True
    T.append(("مادّةٌ مصنوعةٌ سُعِّرت ولم يُصرَخ بها", not screamed))

    # ③ ضوابطُ المثل تميّز: لو تساوت فواتيرُها لكان الحكمُ صدفةً لا قياسًا.
    deltas = {r["Δ"] for r in presence["ضوابطُ_المثل_المشتقّة"]}
    T.append(("ضوابطُ المثل متساويةُ الفواتير — فلا تميّز", len(deltas) < 2))

    # ④ الحضورُ بقاعدة الجذر ليس تحصيلَ حاصل: فرقةٌ مصنوعةٌ لا تناله.
    T.append(("فرقةٌ مصنوعةٌ نالت حضورَ العشرين بقاعدة الجذر",
              presence["أعلى_المصنوعة"] >= presence["حضورُ_العشرين"]))

    # ⑤ القاعدةُ المتروكةُ لا تفصل: لو فصلت لكان تركُها تحكُّمًا لا قياسًا.
    T.append(("القاعدةُ المتروكةُ تفصل كقاعدةِ الجذر",
              left["أعلى_المصنوعة"] <= presence["أعلى_المصنوعة"]))

    # ⑥ شبكةُ الشاهد ليست تحصيلَ حاصل: آياتُها دون آياتِ المجمَّد كلِّها.
    T.append(("شبكةُ (مادة × آية) تسع المجمَّدَ كلَّه — شبكةٌ خاوية",
              len({verse_of[i] for i in fire_of(
                  [nz(m) for m in MATERIALS], assign)}) >= len(verses)))

    # ⑦ العشرون لم تُعرَض على ضابطٍ خاوٍ: الضابطُ المشتقُّ حضورُه كاملٌ بالبناء،
    #    فلو ادُّعي فضلُ حضورٍ عليه لكان الفضلُ من تعريفِ الضابط لا من المقيس.
    T.append(("ادُّعي فضلُ حضورٍ على الضابط المشتقّ — وحضورُه كاملٌ بالبناء",
              presence["حضورُ_العشرين"] > presence["حضورُ_الضابط_المشتقّ"]))

    # ⑧ مصادمةُ ابن فارس ليست قبولًا لكلِّ شيء: المادّةُ المصنوعةُ لا تُدرَج عنده.
    T.append(("المادّةُ المصنوعةُ مُدرَجةٌ عند ابن فارس — فالمصادمةُ تقبل كلَّ شيء",
              nz(FABRICATED_MATERIAL) in by_norm))

    return [dict(محاولة=n, نجحت=bool(ok)) for n, ok in T]


# ═══ ⑦ التشغيل ═════════════════════════════════════════════════════════════════════
def run():
    closed, widest, table_cost = closed_list()
    verses, stream, verse_of, assign = tagging(closed)
    rows = material_rows(stream, verse_of, assign, closed)

    measured_materials = [nz(r["مقيسة"]) for r in rows if r["في_القائمة"]]
    ours = legs([nz(m) for m in MATERIALS], stream, verse_of, assign)
    ours["Δ"] = round(split_of(stream, [nz(m) for m in MATERIALS], assign), 1)

    rivals, tries = derived_rivals(stream, verse_of, assign, closed,
                                   len(MATERIALS), ours["ورود"])
    fab = fabricated_cohorts(len(MATERIALS))
    counts = Counter(assign.values())
    fab_presence = [sum(1 for m in cohort if counts[m]) for cohort in fab]

    presence = dict(
        حضورُ_العشرين=ours["حضور"],
        من_القائمة=len(measured_materials),
        حضورُ_الضابط_المشتقّ=len(MATERIALS),
        حضورُ_المصنوعة=fab_presence, أعلى_المصنوعة=max(fab_presence),
        ضوابطُ_المثل_المشتقّة=rivals,
        خواءُ_الضابط_المشتقّ=dict(
            خاوٍ=True,
            بيان=("كلُّ مادّةٍ في الضابط المشتقِّ حاضرةٌ بتعريفها (مسحوبةٌ من القائمة "
                  "المشتقّة) — فحضورُه 20/20 بالبناء لا بالقياس، ولذلك كان الحَكَمُ "
                  "في الحضور الضابطَ المصنوعَ وحدَه")))

    left = left_rule_presence(stream)
    table, entries, by_norm = maqayis_entries()
    maqayis = maqayis_station(rows, by_norm, table, entries)
    for r in rivals:
        listed = sum(1 for m in r["موادّ"] if nz(m) in by_norm)
        r["إدراج"] = round(listed / len(r["موادّ"]), 4)
    ours["إدراج"] = round(
        maqayis["مقيس"]["مدرَجةٌ_عند_ابن_فارس"] / max(1, maqayis["مقيس"]["مقيسةٌ_عندنا"]), 4)

    verdicts = [
        judge("المدخل ↔ الكلمة (الحضور)", ours["حضور"],
              [dict(حضور=p) for p in fab_presence], "حضور", True,
              "الضابطُ المصنوعُ تباديلُ حروفِ العشرين نفسِها — والتوزيعُ الحرفيُّ هو هو"),
        judge("المادة ↔ العائلة (الاتساع)", ours["اتساع"], rivals, "اتساع", True,
              "ضابطٌ مشتقٌّ مطابقُ الحجم: العشرون أضيقُ من كلِّ فرقةٍ مماثلةٍ في الإطلاق"),
        judge("المدخل ↔ الكلمة (الفاتورة)", ours["Δ"], rivals, "Δ", False,
              "فاتورةُ الوصف الأدنى بمكيال `ta3allum_gate` — والمقارنةُ مطابقةُ الحجم"),
        judge("الشاهد ↔ الآية (الشبكة)", ours["آيات"], rivals, "آيات", True,
              "شبكةُ (مادة × آية) على مقامنا — وشواهدُ المعجمِ نفسُها في صفِّ ابن فارس"),
        judge("المادة ↔ المعجم (الإدراج)", ours["إدراج"], rivals, "إدراج", True,
              "نصيبُ المُدرَجِ عند ابن فارس من الموادِّ المقيسة — والضابطُ مشتقٌّ مثلُها"),
    ]
    deposited = [v for v in verdicts if v["غلبَ_المثل"]]
    debts = [v for v in verdicts if not v["غلبَ_المثل"]]

    trials = falsify(stream, verse_of, assign, closed, presence, left, verses, maqayis, by_norm)

    measured = {
        "كلماتُ المقام": len(stream),
        "موادُّ القائمة المشتقّة": len(set(assign.values())),
        "مواضعُ موسومة": len(assign),
        "العشرون المعلنة": len(MATERIALS),
        "منها في القائمة المشتقّة": len(measured_materials),
        "غيابٌ معلن": len(MATERIALS) - len(measured_materials),
        "ورودُ العشرين": ours["ورود"],
        "اتساعُ العشرين": ours["اتساع"],
        "آياتُ الشبكة": ours["آيات"],
        "مدرَجةٌ عند ابن فارس": maqayis["مقيس"]["مدرَجةٌ_عند_ابن_فارس"],
        "أرجلٌ مُودَعةٌ بالبرهان": len(deposited),
        "ديونٌ بلا رقم": len(debts),
        "محاولاتُ_تكذيب": len(trials),
    }
    for key, sealed in SEALED_MU3JAM.items():
        if measured[key] != sealed:
            raise Mu3jamError(E_SEAL, f"«{key}» = {measured[key]} ≠ المختوم {sealed}")
    if any(t["نجحت"] for t in trials):
        raise Mu3jamError(E_SEAL, "محاولةُ تكذيبٍ نجحت — البابُ ساقط")

    return {"المعجم_v0": {
        "المقام": dict(آيات=len(verses), كلمات=len(stream),
                       موسومة=len(assign),
                       نصيبُ_الموسوم=round(len(assign) / len(stream), 4)),
        "قاعدةُ_الوسم": dict(نصّ=TAG_RULE, طبقة="و٣-قلع", أوسعُ_طبقةٍ_مودَعة=widest,
                             ثمنُ_جدولِ_القوالب=table_cost,
                             قائمةٌ_مغلقة=len(closed),
                             مصدرُ_القائمة="awzan_v0.json · roots_widest"),
        "القائمةُ_المعلنة": dict(عدد=len(MATERIALS), موادّ=list(MATERIALS),
                                 صفوف=rows),
        "الأرجلُ_الثلاث": ours,
        "ضوابطُ_المثل": dict(عدد=MG.RIVALS, بذرة=TG.CONTROL_SEED, نطاقُ_الحجم=BAND,
                              محاولاتُ_السحب=tries, مشتقّة=rivals,
                              مصنوعة=dict(فرق=[list(c) for c in fab],
                                          حضور=fab_presence)),
        "الحضور": presence,
        "القاعدةُ_المتروكة": left,
        "ابنُ_فارس": maqayis,
        "الأحكام": verdicts,
        "ديونٌ_بلا_رقم": [dict(دَين=v["رجل"], بيان=f"{v['بيان']} — سُعِّرت فلم تفصل: لم يغلب ضوابطَ المثل") for v in debts],
        "محاولاتُ_التكذيب": trials,
        "مقيس": measured,
    }}


def show(R):
    M = R["المعجم_v0"]
    m, q = M["مقيس"], M["المقام"]
    print("╔═══ بابُ المعجم: الجسرُ الثلاثيُّ يُقاس ولا يُستشهَد به ═══╗")
    print(f"  المقام: {q['آيات']} آيةً · {q['كلمات']:,} كلمةً — موسومةٌ بمادّةٍ "
          f"{q['موسومة']:,} ({q['نصيبُ_الموسوم']:.2%})")
    print(f"  قاعدةُ الوسم: {M['قاعدةُ_الوسم']['طبقة']} · قائمةٌ مغلقةٌ "
          f"{M['قاعدةُ_الوسم']['قائمةٌ_مغلقة']} مادّةً · ثمنُ جدولِ القوالب "
          f"{M['قاعدةُ_الوسم']['ثمنُ_جدولِ_القوالب']:,} بتًّا")

    print("\n  العشرون المعلنة — والغائبةُ تُعلَن ولا تُحذَف:")
    for r in M["القائمةُ_المعلنة"]["صفوف"]:
        if not r["في_القائمة"]:
            print(f"    ✗ {r['مادة']}: {r['حال']}")
            continue
        print(f"    ✓ {r['مادة']}: ورود {r['ورود']:4} · اتساع {r['اتساع']:3} · "
              f"آيات {r['آيات']:4}")
    print(f"    في القائمة {m['منها في القائمة المشتقّة']}/{m['العشرون المعلنة']} · "
          f"غيابٌ معلن {m['غيابٌ معلن']}")

    print("\n  الأحكام — ما غلبَ المثلَ أُودِع، وما لم يغلبه سُمِّي دَينًا بلا رقم:")
    for v in M["الأحكام"]:
        mark = "✓" if v["غلبَ_المثل"] else "✗"
        print(f"    {mark} {v['رجل']:32} مقيس {v['مقيس']:>8} ⟷ حدُّ المثل "
              f"{v['حدُّ_المثل']:>9} — {v['حكم']}")

    left = M["القاعدةُ_المتروكة"]
    print(f"\n  القاعدةُ المتروكة (المتتالية الجزئية): حضورُ العشرين "
          f"{left['حضورُ_العشرين']}/20 · أعلى فرقةٍ مصنوعةٍ {left['أعلى_المصنوعة']}/20 "
          f"— {'تفصل' if left['تفصل'] else 'لا تفصل'}")
    print(f"  وقاعدةُ الجذر: حضورُ العشرين {M['الحضور']['حضورُ_العشرين']}/20 · "
          f"أعلى مصنوعةٍ {M['الحضور']['أعلى_المصنوعة']}/20 — تفصل")

    f = M["ابنُ_فارس"]
    print(f"\n  ابنُ فارس: {f['حال']} — جذورٌ متمايزةٌ عنده {f['جذورٌ_متمايزة']:,} · "
          f"مقيسةٌ عندنا {f['مقيس']['مقيسةٌ_عندنا']} · مدرَجةٌ عنده "
          f"{f['مقيس']['مدرَجةٌ_عند_ابن_فارس']}")

    print(f"\n  مُودَعٌ بالبرهان {m['أرجلٌ مُودَعةٌ بالبرهان']} · ديونٌ بلا رقم "
          f"{m['ديونٌ بلا رقم']}:")
    for d in M["ديونٌ_بلا_رقم"]:
        print(f"    — {d['دَين']}")
    print(f"  محاولاتُ التكذيب: {m['محاولاتُ_تكذيب']} — لم تنجح واحدةٌ منها ✓")


def main(argv=None):
    ap = argparse.ArgumentParser(description="بابُ المعجم: الجسرُ الثلاثيُّ مقيسًا")
    ap.add_argument("--json", metavar="ملفّ", help="وديعةُ الباب إلى ملفّ")
    args = ap.parse_args(argv)
    try:
        R = run()
    except Mu3jamError as e:
        print(f"صريخ: {e.message}", file=sys.stderr)
        return e.code
    show(R)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(R, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"\nJSON ⟵ {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
