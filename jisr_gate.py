# jisr_gate.py — بابُ الجسر: «أيُقام بين البتِّ والأبجدية جسرٌ يُطوى ويُفَكّ؟»
#
# ــ ٠) الدعوى، والفخُّ الذي تحتها ــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# المطلوبُ برهانُه ثلاثةٌ لا واحد:
#   ① **التعيين**  — لكلِّ محرفٍ في الأبجدية كلمةُ بتٍّ واحدةٌ معيَّنة، لا اثنتان.
#   ② **التمييز**  — ٠ و١ ليسا اسمين لشيءٍ واحد: تبديلُهما يُفسِد، لا يُبقي.
#   ③ **الطيُّ والفكّ** — النصُّ يُطوى بتّاتٍ ثمّ يُفَكُّ فيعود هو هو بايتًا بايتًا.
#
# وتحت الثالثِ **فخٌّ يُبطِل العملَ كلَّه إن لم يُنصَب له**: الطيُّ ثمّ الفكُّ يُعطي
# المطابقةَ التامّةَ لأيِّ تقابلٍ كان — حتّى لجدولٍ مختلَقٍ لا معنى له. فالمطابقةُ
# ١٫٠٠٠٠ **تحصيلُ حاصلٍ لا برهان**، وهي بعينها هويّةُ `induction/mirror.py` التي
# سقطت في هذا المختبر لمّا تبيّن أنّ جداولَ لواحقَ مختلقةً وفارغةً تُعطيها كلَّها.
#
# فلا يُقبَل من هذا البابِ رقمُ مطابقةٍ البتّة حتى يُقاس **ما يَرُدُّه المقياس**:
# جداولُ مصنوعةٌ تُعرَض عليه فتسقط، وتبديلٌ في البتّات يُعرَض فيُفسِد. وعددُ
# الساقطِ هو وحدَه برهانُ أنّ المطابقةَ ليست خاوية.
#
# ــ ١) وما لا يَثبُت به التمييزُ وإن أوهم ــــــــــــــــــــــــــــــــــــــــــــ
# يُظَنُّ أنّ عدَّ الأصفار والآحاد يميِّز. وهو **خاوٍ** ويُقاس ههنا ليُعلَن خواؤه:
# نصيبُ الصفر يقارب النصفَ بالبناء (الجدولُ المشتقُّ بالتردُّد يُسوّي الفرعين)،
# فالقربُ من النصف لا يَنفي تمييزًا ولا يُثبته. والمميِّزُ هو **الفكُّ** لا العدّ.
#
# ــ ٢) والمقامُ مختومٌ قبل أن يُعَدّ ــــــــــــــــــــــــــــــــــــــــــــــــــ
# الأبجديةُ **لا تُعلَن بيد**: تُشتقُّ محارفَ من بايتاتِ مصدرٍ مختوم. ومصدران لا
# واحد — شرطُ العموم الموروثُ من `deposit_law.price_two_sources`: «مصدرٌ واحدٌ لا
# يُثبِت عموميّةَ مكيالٍ البتّة». وختمُ كلِّ مصدرٍ **يُقرَأ من كود مُنشِئه** لا
# يُنسَخ ههنا، فلا تتخلّف نسخةٌ ثانيةٌ عن أصلها.
#
# ــ ٣) والكيلُ ليس هنا ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# ثمنُ التعيين يُقاس بـ`deposit_law.price` — تُستدعى ولا تُنسَخ. وبابٌ يكيل بمكياله
# يعيد العطلَ الذي قُتل في `sole_judge`.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بايتاتٌ غائبة · 4 ختمٌ خالف · 5 الجسرُ سقط.
#
# التشغيل:
#   python jisr_gate.py                      # عرضٌ على الشاشة
#   python jisr_gate.py --json jisr_v0.json  # إيداع
#   python jisr_gate.py --doc JISR.md        # توليدُ الوثيقة

import argparse
import hashlib
import heapq
import json
import math
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "induction"))
import deposit_law as DL                                        # noqa: E402

E_USAGE = 2
E_MISSING = 3
E_SEAL = 4
E_BRIDGE = 5


class JisrError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


# ── التسجيلُ المسبق: يُكتَب قبل أن يُقاس، ويُودَع نصًّا فلا يُبدَّل بعد الرؤية ──────
PRE_REGISTERED = (
    "① الأبجديةُ تُشتقُّ من بايتاتٍ مختومةٍ ولا تُعلَن بيد.",
    "② التعيينُ يُشتقُّ بالتردُّد المقيس على المصدر نفسِه — لا يُختار بالهوى.",
    "③ الفاكُّ لا يرى النصَّ الأصليَّ البتّة: يأخذ البتّاتِ والجدولَ وحدَهما.",
    "④ المطابقةُ ١٫٠٠٠٠ لا تُقبَل برهانًا حتى يسقطَ مصنوعٌ بالمقياس نفسِه.",
    "⑤ نصيبُ الصفر يُقاس ويُعلَن **خاويًا** — لا يُتَّخذ حجّةً على تمييز.",
    "⑥ مصدران لا واحد؛ والواحدُ لا يُثبِت عمومًا.",
    "⑦ المصنوعُ يُعرَض على المقياس نفسِه بلا تليينٍ له ولا تشديد.",
)

# ── المصادر: ختمُ كلٍّ مقروءٌ من كود مُنشِئه، لا منسوخٌ ههنا ───────────────────────
def sealed_sources():
    """المصدران المختومان — وختمُ كلٍّ يُقرَأ من موضعه الأصليِّ لا يُكتَب ههنا."""
    import algebra_engine as AE
    import shakhsiyya_extract as SE
    return (
        dict(اسم="المجمَّد", مسار=AE.MUJAMMAD_PATH, ختم=AE.MUJAMMAD_SHA256,
             سند="algebra_engine.MUJAMMAD_SHA256"),
        dict(اسم="متنُ الشخصية ج٣", مسار=os.path.join(HERE, SE.MATN),
             ختم=SE.MATN_SHA256, سند="shakhsiyya_extract.MATN_SHA256"),
    )


def read_sealed(src):
    """بايتاتُ المصدر مُصادَمةً بختمها قبل أن يُعَدَّ منها محرفٌ واحد."""
    if not os.path.exists(src["مسار"]):
        raise JisrError(E_MISSING, f"بايتاتُ «{src['اسم']}» غائبة: {src['مسار']}")
    raw = open(src["مسار"], "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    if got != src["ختم"]:
        raise JisrError(E_SEAL,
                        f"«{src['اسم']}» خالف ختمَه: {got[:16]}… ⟷ {src['ختم'][:16]}…")
    return raw.decode("utf-8")


# ── ① التعيين: جدولٌ مشتقٌّ بالتردُّد، لا مُعلَنٌ بيد ──────────────────────────────
def assign(counts):
    """تعيينُ كلمةِ بتٍّ لكلِّ محرفٍ باندماجِ أقلِّ تردُّدين — والفرعان ٠ و١.

    والترتيبُ مثبَّتٌ بمفتاحٍ ثانٍ (الرمزُ نفسُه ثمّ مسلسلٌ صاعد) فلا يتأرجح
    الجدولُ بين تشغيلتين — وإلّا صار الختمُ غيرَ قابلٍ للمصادمة.
    """
    if not counts:
        raise JisrError(E_BRIDGE, "أبجديةٌ فارغة — لا تعيينَ على فراغ")
    if len(counts) == 1:
        return {next(iter(counts)): "0"}
    heap = [(n, i, [s]) for i, (s, n) in enumerate(sorted(counts.items()))]
    heapq.heapify(heap)
    code = {s: "" for s in counts}
    serial = len(counts)
    while len(heap) > 1:
        n1, _, g1 = heapq.heappop(heap)
        n2, _, g2 = heapq.heappop(heap)
        for s in g1:
            code[s] = "0" + code[s]
        for s in g2:
            code[s] = "1" + code[s]
        heapq.heappush(heap, (n1 + n2, serial, g1 + g2))
        serial += 1
    return code


def is_injective(code):
    """التعيينُ متباينٌ: لا كلمتَي بتٍّ متساويتين لمحرفين."""
    return len(set(code.values())) == len(code)


def is_prefix_free(code):
    """لا كلمةَ بتٍّ بادئةُ أخرى — وهذا شرطُ الفكِّ بلا فاصلٍ خارجيّ."""
    words = sorted(code.values())
    return all(not b.startswith(a) for a, b in zip(words, words[1:]))


# ── ② الطيُّ والفكّ ───────────────────────────────────────────────────────────────
def fold(text, code):
    """الطيّ: نصٌّ ⟶ بتّات. ومحرفٌ خارجَ التعيين **يصرخ** ولا يُسقَط صامتًا."""
    out = []
    for ch in text:
        w = code.get(ch)
        if w is None:
            raise JisrError(E_BRIDGE, f"محرفٌ خارجَ التعيين: U+{ord(ch):04X}")
        out.append(w)
    return "".join(out)


def unfold(bits, code):
    """الفكّ: بتّاتٌ ⟶ نصّ. ولا يرى النصَّ الأصليَّ البتّة — جدولٌ وبتّاتٌ فقط.

    والبتّاتُ المبتورةُ (بقيّةٌ لا تُكمِل كلمةً) **تصرخ** ولا تُكمَّل بالحشو:
    الحشوُ ههنا اختلاقُ محرفٍ لم يُطوَ.
    """
    inv = {}
    for s, w in code.items():
        if w in inv:
            raise JisrError(E_BRIDGE, f"تعيينٌ غيرُ متباين: «{w}» لمحرفين")
        inv[w] = s
    out, cur = [], ""
    for b in bits:
        if b not in "01":
            raise JisrError(E_BRIDGE, f"رمزٌ ليس بتًّا في التيّار: {b!r}")
        cur += b
        s = inv.get(cur)
        if s is not None:
            out.append(s)
            cur = ""
    if cur:
        raise JisrError(E_BRIDGE, f"بتّاتٌ مبتورة: بقيّةٌ بطول {len(cur)} لا تُكمِل كلمة")
    return "".join(out)


def round_trip(text, code):
    """الطيُّ ثمّ الفكُّ — ويُرَدُّ الحكمُ مع سببِ السقوط إن سقط."""
    try:
        bits = fold(text, code)
        back = unfold(bits, code)
    except JisrError as exc:
        return dict(قام=False, سبب=exc.message, بتّات=None)
    return dict(قام=(back == text), سبب=None if back == text else "الفكُّ خالف الأصل",
                بتّات=len(bits))


# ── ③ محطّةُ المصدر: الأبجديةُ والتعيينُ وثمنُه ────────────────────────────────────
def source_station(src):
    """مقامُ مصدرٍ واحدٍ مشتقًّا من بايتاته المختومة — بلا رقمٍ مُعلَنٍ بيد."""
    text = read_sealed(src)
    counts = Counter(text)
    code = assign(counts)
    rt = round_trip(text, code)
    if not rt["قام"]:
        raise JisrError(E_BRIDGE, f"الجسرُ سقط على «{src['اسم']}»: {rt['سبب']}")
    bits = fold(text, code)
    width = max(1, math.ceil(math.log2(len(counts)))) if len(counts) > 1 else 1
    fixed = len(text) * width
    zeros = bits.count("0")
    priced = DL.price(text, 0)
    return dict(
        اسم=src["اسم"], سندُ_الختم=src["سند"], ختم=src["ختم"],
        محارف=len(text), أبجدية=len(counts),
        تعيينٌ_متباين=is_injective(code), تعيينٌ_بادئيّ=is_prefix_free(code),
        بتّاتُ_الطيّ=len(bits), ثابتُ_العرض=fixed, عرضُ_الثابت=width,
        مكسبُ_التعيين=fixed - len(bits),
        نصيبُ_المكسب=round(1 - len(bits) / fixed, 4),
        بتٌّ_للمحرف=round(len(bits) / len(text), 4),
        حدُّ_المكيال=round(priced["بيانات"] / len(text), 4),
        نصيبُ_الصفر=round(zeros / len(bits), 4),
        طيٌّ_وفكٌّ_متطابقان=True,
    ), text, code, bits


# ── ④ محطّةُ التمييز: ٠ و١ ليسا اسمين لشيءٍ واحد ──────────────────────────────────
POLARITY = str.maketrans("01", "10")
FLIP_SAMPLE = 256
FLIP_SEED = 0
TAMYIZ_WINDOW = 4000


# ── ضابطُ التمييز: قناةٌ فيها بتٌّ لا أثرَ له — تُعرَض على المقياس نفسِه ───────────
def blind_fold(text, code):
    """طيٌّ يَحشو بعد كلِّ كلمةٍ بتًّا — والبتُّ المحشوُّ **لا يحمل خبرًا**."""
    return "".join(code[ch] + "0" for ch in text)


def blind_unfold(bits, code):
    """فكٌّ يَقفِز البتَّ المحشوَّ ولا يقرؤه — فقلبُه لا يُبدِّل شيئًا."""
    inv = {w: s for s, w in code.items()}
    out, cur, i = [], "", 0
    while i < len(bits):
        cur += bits[i]; i += 1
        s = inv.get(cur)
        if s is not None:
            out.append(s); cur = ""
            if i >= len(bits):
                raise JisrError(E_BRIDGE, "حشوٌ مبتور")
            i += 1
    if cur:
        raise JisrError(E_BRIDGE, "بتّاتٌ مبتورة")
    return "".join(out)


def mutate_tally(origin, bits, decode):
    """المصادماتُ الثلاثُ على تيّارٍ وفاكٍّ أيًّا كانا — تُعاد حرفيًّا للضابط."""
    def outcome(stream):
        try:
            back = decode(stream)
        except JisrError:
            return "صرخ"
        return "لم يتبدّل" if back == origin else "تبدَّل"

    swapped = outcome(bits.translate(POLARITY))
    flip, drop = Counter(), Counter()
    rng = random.Random(FLIP_SEED)
    for _ in range(FLIP_SAMPLE):
        i = rng.randrange(len(bits))
        flip[outcome(bits[:i] + ("1" if bits[i] == "0" else "0") + bits[i + 1:])] += 1
    rng2 = random.Random(FLIP_SEED)
    for _ in range(FLIP_SAMPLE):
        i = rng2.randrange(len(bits))
        drop[outcome(bits[:i] + bits[i + 1:])] += 1
    blind = flip["لم يتبدّل"] + drop["لم يتبدّل"] + (1 if swapped == "لم يتبدّل" else 0)
    return dict(قلبُ_القطبين=swapped, قلبُ_بتٍّ_واحد=dict(flip),
                حذفُ_بتٍّ_واحد=dict(drop), بتٌّ_بلا_أثر=blind)


def tamyiz_station(text, code, bits):
    """التمييزُ مقيسٌ، **وقوّةُ قياسِه مقيسةٌ معه** — وهذا موضعُ الصدق فيه.

    يُبدَّل البتُّ ثلاثَ مصادمات (قلبُ القطبين · قلبُ بتٍّ · حذفُ بتٍّ) فيُنظَر
    أيُفسِد أم لا يُبالى به. والحقُّ أنّ «لم يتبدّل» **مُحالٌ بالبناء** متى كان
    التعيينُ متباينًا بادئيًّا: الطيُّ دالّةٌ، فلا تيّارانِ مختلفان يُعطيان نصًّا
    واحدًا. فالمصادماتُ وحدَها **لازمُ بناءٍ لا برهانُ تمييز**، ولو سُكت عن هذا
    لكانت دعوى «٢٥٦/٢٥٦ تبدَّل» من جنس هويّة `mirror.py` الخاوية.

    فيُعرَض عليها **ضابطٌ**: قناةٌ تَحشو بتًّا بعد كلِّ كلمةٍ وتقفزه في الفكّ —
    فيها بتٌّ لا خبرَ فيه بالبناء. فإن لم تُسجِّل المصادماتُ على الضابط «بتًّا بلا
    أثر» فهي **عمياء**، ولا يُقبَل منها حكمٌ على المودَع.

    ومقامُ المصادمتين الأخيرتين مُعلَنٌ لا مطويّ: نافذةُ `TAMYIZ_WINDOW` محرفًا من
    صدر النصّ — ضرورةُ زمنٍ تُعلَن ولا تُدَّعى عمومًا.
    """
    win = text[:TAMYIZ_WINDOW]
    sealed = mutate_tally(win, fold(win, code), lambda s: unfold(s, code))
    swapped_full = "لم يتبدّل" if False else None
    try:
        swapped_full = ("لم يتبدّل" if unfold(bits.translate(POLARITY), code) == text
                        else "تبدَّل")
    except JisrError:
        swapped_full = "صرخ"
    control = mutate_tally(win, blind_fold(win, code), lambda s: blind_unfold(s, code))
    powerful = control["بتٌّ_بلا_أثر"] > 0
    return dict(
        المودَع=sealed, الضابط=control,
        قلبُ_القطبين_على_التيّار_كلِّه=swapped_full, مقامُ_التيّار=len(bits),
        عيّنة=FLIP_SAMPLE, بذرة=FLIP_SEED,
        نافذة=TAMYIZ_WINDOW,
        بتٌّ_بلا_أثر=sealed["بتٌّ_بلا_أثر"],
        بتٌّ_بلا_أثرٍ_في_الضابط=control["بتٌّ_بلا_أثر"],
        المقياسُ_ذو_قوّة=powerful,
        مميَّز=(sealed["بتٌّ_بلا_أثر"] == 0 and powerful),
        حدّ=("البتُّ ذو أثرٍ في المودَع، والمقياسُ أثبتَ قوّتَه إذ سجَّل على الضابط "
             f"{control['بتٌّ_بلا_أثر']} بتًّا بلا أثر" if powerful else
             "المقياسُ أعمى: لم يُسجِّل على الضابطِ بتًّا بلا أثر، فلا حكمَ له"),
    )


# ── ⑤ محطّةُ الخواء المسمّى: ما لا يميِّز وإن أوهم ─────────────────────────────────
def hollow_station(stations):
    """نصيبُ الصفر يُقاس ويُعلَن خاويًا — ولا يُفرَد حجّةً على تمييزٍ ولا على نفيه."""
    shares = [s["نصيبُ_الصفر"] for s in stations]
    return dict(
        نصيبُ_الصفر=shares,
        أقصى_بعدٍ_عن_النصف=round(max(abs(x - 0.5) for x in shares), 4),
        خاوٍ=True,
        حدّ=("القربُ من النصف لازمُ التعيين المشتقِّ بالتردُّد لا شاهدُ تمييز — "
             "والمميِّزُ الفكُّ وحدَه. يُعرَض هذا الرقمُ ولا يَحكم"),
    )


# ── ⑥ محطّةُ قوّة المقياس: المصنوعُ يُعرَض فيسقط ───────────────────────────────────
def forged_tables(code, counts, rng):
    """جداولُ مصنوعةٌ تُعرَض على المقياس نفسِه — ويجب أن يَرُدَّها كلَّها.

    وهذه هي **مقتلُ دعوى ١٫٠٠٠٠**: إن مرّ مصنوعٌ فالمطابقةُ خاويةٌ كهوية
    `mirror.py`، ولا تُقبَل من هذا الباب كلمةٌ واحدة.
    """
    keys = sorted(code)
    longest = max(code.values(), key=len)
    forged = []

    # ① غيرُ متباين: محرفان بكلمةِ بتٍّ واحدة — فالفكُّ لا يعرف أيَّهما
    t1 = dict(code); t1[keys[1]] = code[keys[0]]
    forged.append(("تعيينٌ غيرُ متباين", t1))

    # ② غيرُ بادئيّ: كلمةٌ صارت بادئةَ أطولِ كلمة — فالفكُّ يقطع قبل أوانه
    t2 = dict(code); t2[keys[0]] = longest[:-1]
    forged.append(("تعيينٌ غيرُ بادئيّ", t2))

    # ③ ناقصٌ: محرفٌ من الأبجدية بلا تعيين
    t3 = dict(code); t3.pop(keys[2])
    forged.append(("تعيينٌ ناقصٌ محرفًا", t3))

    # ④ عشوائيٌّ بأطوالٍ عشوائيّةٍ ببذرةٍ معلنة — تقابلٌ بلا بنية
    t4, seen = {}, set()
    for s in keys:
        while True:
            w = "".join(rng.choice("01") for _ in range(rng.randint(1, 9)))
            if w not in seen:
                seen.add(w); t4[s] = w; break
    forged.append(("تعيينٌ عشوائيٌّ ببذرة", t4))

    # ⑤ ثابتُ العرض على عرضٍ أضيقَ من الأبجدية — فمحرفان يلتقيان
    narrow = max(1, math.ceil(math.log2(len(counts))) - 1)
    t5 = {s: format(i % (2 ** narrow), f"0{narrow}b") for i, s in enumerate(keys)}
    forged.append(("ثابتُ عرضٍ أضيقُ من الأبجدية", t5))

    # ⑥ كلمةٌ واحدةٌ للجميع — أقصى الانهيار
    t6 = {s: "0" for s in keys}
    forged.append(("كلمةٌ واحدةٌ للأبجدية كلِّها", t6))
    return forged


def power_station(text, code, counts):
    """قوّةُ المقياس: كم مصنوعًا رَدَّ؟ — وردُّه كلَّها شرطُ قبولِ رقم المطابقة."""
    rng = random.Random(FLIP_SEED)
    rows = []
    for name, table in forged_tables(code, counts, rng):
        rt = round_trip(text, table)
        rows.append(dict(مصنوع=name, قام=rt["قام"], سبب=rt["سبب"]))
    passed = [r["مصنوع"] for r in rows if r["قام"]]
    return dict(
        مصنوعاتٌ_عُرضت=len(rows), مصنوعاتٌ_رُدَّت=len(rows) - len(passed),
        مصنوعاتٌ_مرّت=len(passed), أسماءُ_ما_مرّ=passed,
        صفوف=rows,
        المطابقةُ_خاوية=bool(passed),
        حدّ=("المطابقةُ ذاتُ مضمون: المقياسُ ردَّ المصنوعَ كلَّه بالمكيال نفسِه"
             if not passed else
             "المطابقةُ خاويةٌ كهوية mirror.py — مصنوعٌ مرَّ بها، فلا تُقبَل"),
    )


# ── ⑥½ ضوابطُ المثل: برهانُ أنّ **الطيَّ والفكَّ مجّانيّان** وأنّ التعيينَ ليس كذلك ──
RIVALS = 11


def rivals_station(text, code, counts):
    """أضدادٌ **تُطوى وتُفَكُّ كلُّها** ولا تكسب — فالمطابقةُ مجّانيّةٌ والتعيينُ ثمين.

    يُؤخَذ جدولُ التعيين نفسُه، وتُخلَط نسبةُ الكلماتِ إلى المحارف خلطًا عشوائيًّا
    ببذرةٍ معلنة. فالضدُّ **متباينٌ بادئيٌّ** كالأصل سواءً بسواء — ومن ثَمَّ يُطوى
    ويُفَكُّ مطابقةً تامّةً هو أيضًا. وهذا بعينه **برهانُ خواء رقم المطابقة**:
    إحدى عشرةَ فرقةً عشوائيّةً تناله كلُّها.

    والفارقُ كلُّه في **الثمن**: الضدُّ يُنفق بتّاتٍ أكثر لأنّه عيَّن الطويلَ
    للكثير. فإن لم يغلب الأصلُ أدنى أضدادِه فالتعيينُ تسميةٌ حرّةٌ لا قاعدة.
    """
    words = [code[s] for s in sorted(code)]
    rng = random.Random(FLIP_SEED)
    base = sum(counts[s] * len(code[s]) for s in code)
    rows = []
    for k in range(RIVALS):
        shuffled = list(words)
        rng.shuffle(shuffled)
        rival = {s: w for s, w in zip(sorted(code), shuffled)}
        cost = sum(counts[s] * len(rival[s]) for s in rival)
        rt = round_trip(text, rival)
        rows.append(dict(ضدّ=k + 1, بتّات=cost, طُوي_وفُكّ=rt["قام"],
                         متباينٌ_بادئيّ=is_injective(rival) and is_prefix_free(rival)))
    folded = sum(1 for r in rows if r["طُوي_وفُكّ"])
    worst = min(r["بتّات"] for r in rows)
    return dict(
        أضدادٌ=RIVALS, بذرة=FLIP_SEED,
        أضدادٌ_طُويت_وفُكَّت=folded,
        بتّاتُ_المودَع=base, أدنى_ضدٍّ=worst, أقصى_ضدٍّ=max(r["بتّات"] for r in rows),
        غلبَ_أدنى_ضدٍّ=base < worst, فرقٌ_عن_أدنى_ضدٍّ=worst - base,
        صفوف=rows,
        حدّ=(f"الأضدادُ {folded}/{RIVALS} طُويت وفُكَّت مطابقةً تامّةً — "
             f"فرقمُ المطابقة **مجّانيٌّ بالبرهان**. والمودَعُ يغلبها بالثمن وحدَه: "
             f"{worst - base:,} بتًّا دون أدناها"),
    )


# ── ⑦ محاولاتُ تكذيبِ الباب نفسِه ─────────────────────────────────────────────────
def falsify():
    """محاولاتٌ تُشغَّل ولا تُقرَأ — ونجاحُ واحدةٍ يُسقِط البابَ."""
    trials, rng = [], random.Random(FLIP_SEED)

    def trial(name, fn):
        try:
            trials.append(dict(محاولة=name, رُدَّت=bool(fn())))
        except (JisrError, ValueError, KeyError, ZeroDivisionError):
            trials.append(dict(محاولة=name, رُدَّت=True))

    toy = Counter("ابتث" * 7 + "ج" * 3 + "ح")
    c = assign(toy)
    txt = "ابتثجحاباب"
    b = fold(txt, c)

    trial("① محرفٌ خارجَ التعيين يُطوى صامتًا", lambda: fold(txt + "Z", c) and False)
    trial("② بتّاتٌ مبتورةٌ تُكمَّل بالحشو", lambda: unfold(b + "1" * 40, c) and False)
    trial("③ رمزٌ ليس بتًّا يُقبَل في التيّار", lambda: unfold(b.replace("0", "2", 1), c) and False)
    trial("④ تعيينٌ غيرُ متباينٍ يُفَكّ", lambda: unfold(b, {**c, "ح": c["ج"]}) and False)
    trial("⑤ أبجديةٌ فارغةٌ تُعيَّن", lambda: assign({}) and False)
    trial("⑥ التعيينُ يتأرجح بين تشغيلتين",
          lambda: assign(toy) == assign(dict(reversed(list(toy.items())))))
    trial("⑦ قلبُ القطبين لا يُبالى به",
          lambda: unfold(b.translate(POLARITY), c) != txt)
    trial("⑧ المصنوعُ يمرُّ بالمقياس",
          lambda: power_station(txt, c, toy)["مصنوعاتٌ_مرّت"] == 0)
    trial("⑨ التعيينُ المودَعُ غيرُ بادئيّ", lambda: is_prefix_free(c))
    trial("⑩ مصدرٌ بختمٍ مخالفٍ يُقرَأ",
          lambda: read_sealed(dict(اسم="مصنوع", مسار=os.path.join(HERE, "jisr_gate.py"),
                                   ختم="0" * 64, سند="-")) and False)
    trial("⑪ مصدرٌ غائبٌ يُقرَأ بلا صريخ",
          lambda: read_sealed(dict(اسم="غائب", مسار=os.path.join(HERE, "لا-وجود-له.txt"),
                                   ختم="0" * 64, سند="-")) and False)
    trial("⑫ الفكُّ يرى النصَّ الأصليّ",
          lambda: "text" not in unfold.__code__.co_varnames)
    trial("⑬ عيّنةُ القلب تُقرَأ بلا بذرةٍ معلنة",
          lambda: isinstance(FLIP_SEED, int) and FLIP_SAMPLE > 0)
    trial("⑭ ثابتُ العرض يُحسَب أضيقَ من الأبجدية",
          lambda: 2 ** max(1, math.ceil(math.log2(len(toy)))) >= len(toy))
    trial("⑮ مصدرٌ واحدٌ يُقبَل برهانَ عموم", lambda: len(sealed_sources()) >= 2)
    trial("⑯ ضدُّ المثل لا يُطوى ولا يُفَكّ",
          lambda: rivals_station(txt, c, toy)["أضدادٌ_طُويت_وفُكَّت"] == RIVALS)
    # ⑰ المقياسُ قادرٌ على أن يقول «لم يغلب»: أبجديّةٌ مستويةُ التردُّد لا تَفصِل
    flat = Counter({ch: 8 for ch in "ابتثجحخد"})
    flat_txt = "".join(k * v for k, v in sorted(flat.items()))
    trial("⑰ ضوابطُ المثل تَقبَل كلَّ تعيينٍ ولا تَفصِل",
          lambda: rivals_station(flat_txt, assign(flat), flat)["غلبَ_أدنى_ضدٍّ"] is False)
    # ⑱ الضابطُ الأعمى قناةٌ صحيحةٌ في ذاتها — عيبُها البتُّ المحشوُّ وحدَه، لا الكسر
    toy_c = Counter("ابتثجحخد" * 40 + "اااااااا")
    toy_t = "".join(sorted(toy_c.elements()))
    toy_k = assign(toy_c)
    trial("⑱ الضابطُ الأعمى مكسورٌ فلا يصلح ضابطًا",
          lambda: blind_unfold(blind_fold(toy_t, toy_k), toy_k) == toy_t)
    # ⑲ مقياسُ التمييز أعمى: لا يُسجِّل على الضابطِ بتًّا بلا أثر
    trial("⑲ مصادماتُ التمييز عمياءُ عن بتٍّ لا خبرَ فيه",
          lambda: mutate_tally(toy_t, blind_fold(toy_t, toy_k),
                               lambda s: blind_unfold(s, toy_k))["بتٌّ_بلا_أثر"] > 0)
    # ⑳ وهي في الوقت نفسِه لا تَرمي المودَعَ بالعمى: صفرٌ على القناة الأمينة
    trial("⑳ مصادماتُ التمييز تَرمي القناةَ الأمينةَ بالعمى",
          lambda: mutate_tally(toy_t, fold(toy_t, toy_k),
                               lambda s: unfold(s, toy_k))["بتٌّ_بلا_أثر"] == 0)
    passed = [t["محاولة"] for t in trials if not t["رُدَّت"]]
    return dict(عدد=len(trials), رُدَّت=len(trials) - len(passed),
                نجحت=len(passed), أسماءُ_ما_نجح=passed, صفوف=trials)


# ── ⑧ الديونُ تُسمّى بلا رقم ───────────────────────────────────────────────────────
DEBTS = (
    "الجسرُ على **المحارف** لا على المعاني: يَطوي صورةَ الحرف ولا يَزعم أنّه طوى "
    "دلالتَه — ولا يُستدَلُّ به على بابٍ من أبواب المدلول.",
    "والتعيينُ مشتقٌّ من تردُّدِ مصدرِه بعينه، فجدولُ مصدرٍ لا يَفُكُّ مصدرًا آخرَ "
    "إلّا أن تتّحد أبجديّتاهما — وهذا حدٌّ مقيسٌ أدناه لا دعوى.",
    "ومقامُ الأبجدية بايتاتُ المصدر كما هي: ترويستُه وأرقامُه ومحارفُه اللاتينيّةُ "
    "كلُّها فيه — فلا يُدَّعى أنّ الأبجديةَ عربيّةٌ خالصة.",
    "وبرهانُ الطيِّ والفكِّ برهانُ **إمكان** لا برهانُ أفضليّة: لا يُزعَم أنّ هذا "
    "التعيينَ أمثلُ التعيينات، بل أنّه قائمٌ ومقيسٌ ويَرُدُّ المصنوع.",
)


# ── ⑨ حدُّ العبور بين المصدرين: مقيسٌ لا مُدَّعًى ──────────────────────────────────
def crossing_station(stations, texts, codes):
    """أيَفُكُّ جدولُ مصدرٍ نصَّ مصدرٍ آخر؟ — يُقاس ويُعلَن، ولا يُطوى الحدُّ صامتًا."""
    rows = []
    for i, a in enumerate(stations):
        for j, b in enumerate(stations):
            if i == j:
                continue
            rt = round_trip(texts[j], codes[i])
            rows.append(dict(جدول=a["اسم"], نصّ=b["اسم"], قام=rt["قام"], سبب=rt["سبب"]))
    shared = set(codes[0]) & set(codes[1])
    return dict(صفوف=rows, عبورٌ_قام=sum(1 for r in rows if r["قام"]),
                عبورٌ_سقط=sum(1 for r in rows if not r["قام"]),
                محارفُ_مشتركة=len(shared),
                حدّ="الجسرُ يقوم بجدوله على مصدره؛ والعبورُ يُقاس ولا يُدَّعى")


# ── العرضُ والتوليد ───────────────────────────────────────────────────────────────
def run():
    srcs = sealed_sources()
    stations, texts, codes, streams = [], [], [], []
    for src in srcs:
        st, text, code, bits = source_station(src)
        stations.append(st); texts.append(text); codes.append(code); streams.append(bits)

    tamyiz = [dict(مصدر=s["اسم"], **tamyiz_station(t, c, b))
              for s, t, c, b in zip(stations, texts, codes, streams)]
    power = [dict(مصدر=s["اسم"], **power_station(t, c, Counter(t)))
             for s, t, c in zip(stations, texts, codes)]
    rivals = [dict(مصدر=s["اسم"], **rivals_station(t, c, Counter(t)))
              for s, t, c in zip(stations, texts, codes)]
    hollow = hollow_station(stations)
    cross = crossing_station(stations, texts, codes)
    tri = falsify()

    distinguishable = all(x["مميَّز"] for x in tamyiz)
    non_hollow = all(p["مصنوعاتٌ_مرّت"] == 0 for p in power)
    beats_rivals = all(r["غلبَ_أدنى_ضدٍّ"] for r in rivals)
    folds = all(s["طيٌّ_وفكٌّ_متطابقان"] for s in stations)
    assigned = all(s["تعيينٌ_متباين"] and s["تعيينٌ_بادئيّ"] for s in stations)
    fell = (not (distinguishable and non_hollow and folds and assigned and beats_rivals)
            or tri["نجحت"] > 0)

    return {"الجسر_v0": dict(
        التسجيلُ_المسبق=list(PRE_REGISTERED),
        مصادر=stations,
        التمييز=tamyiz,
        قوّةُ_المقياس=power,
        ضوابطُ_المثل=rivals,
        الخواءُ_المسمّى=hollow,
        العبور=cross,
        محاولاتُ_تكذيب=tri,
        ديونٌ_مسمّاة=list(DEBTS),
        مقيس=dict(
            مصادرُ_مختومة=len(stations),
            أبجدياتٌ_مشتقّة=[s["أبجدية"] for s in stations],
            تعيينٌ_متباينٌ_بادئيّ=sum(1 for s in stations
                                      if s["تعيينٌ_متباين"] and s["تعيينٌ_بادئيّ"]),
            طيٌّ_وفكٌّ_قام=sum(1 for s in stations if s["طيٌّ_وفكٌّ_متطابقان"]),
            مكسبُ_التعيين=[s["مكسبُ_التعيين"] for s in stations],
            بتٌّ_بلا_أثر=sum(x["بتٌّ_بلا_أثر"] for x in tamyiz),
            بتٌّ_بلا_أثرٍ_في_ضابطِ_التمييز=sum(x["بتٌّ_بلا_أثرٍ_في_الضابط"]
                                               for x in tamyiz),
            مقياسُ_التمييزِ_ذو_قوّة=sum(1 for x in tamyiz if x["المقياسُ_ذو_قوّة"]),
            مصنوعاتٌ_عُرضت=sum(p["مصنوعاتٌ_عُرضت"] for p in power),
            مصنوعاتٌ_رُدَّت=sum(p["مصنوعاتٌ_رُدَّت"] for p in power),
            مصنوعاتٌ_مرّت=sum(p["مصنوعاتٌ_مرّت"] for p in power),
            أضدادٌ_عُرضت=sum(r["أضدادٌ"] for r in rivals),
            أضدادٌ_طُويت_وفُكَّت=sum(r["أضدادٌ_طُويت_وفُكَّت"] for r in rivals),
            غلبَ_أدنى_ضدٍّ=sum(1 for r in rivals if r["غلبَ_أدنى_ضدٍّ"]),
            فرقٌ_عن_أدنى_ضدٍّ=[r["فرقٌ_عن_أدنى_ضدٍّ"] for r in rivals],
            مصادماتُ_التمييز=sum(2 * (1 + 2 * FLIP_SAMPLE) for _ in tamyiz),
            نافذةُ_التمييز=TAMYIZ_WINDOW,
            عبورٌ_قام=cross["عبورٌ_قام"], عبورٌ_سقط=cross["عبورٌ_سقط"],
            ديونٌ_مسمّاة=len(DEBTS),
            محاولاتُ_تكذيب=tri["عدد"],
        ),
        حكم=dict(
            معيَّن=assigned, مميَّز=distinguishable,
            يُطوى_ويُفَكّ=folds, المطابقةُ_ذاتُ_مضمون=non_hollow,
            غلبَ_ضوابطَ_المثل=beats_rivals,
        ),
        سقوط=fell,
    )}


def show(R):
    J = R["الجسر_v0"]
    print("بابُ الجسر — بين البتِّ والأبجدية\n")
    print(f"{'المصدر':<22}{'أبجدية':>8}{'محارف':>11}{'بتّات':>12}"
          f"{'ثابتُ العرض':>13}{'مكسب':>12}{'بتٌّ/محرف':>11}")
    for s in J["مصادر"]:
        print(f"{s['اسم']:<22}{s['أبجدية']:>8}{s['محارف']:>11,}{s['بتّاتُ_الطيّ']:>12,}"
              f"{s['ثابتُ_العرض']:>13,}{s['مكسبُ_التعيين']:>12,}{s['بتٌّ_للمحرف']:>11}")
    print("\n— التمييز: أيُبالي الفكُّ بالبتّ؟ —")
    for x in J["التمييز"]:
        m, g = x["المودَع"], x["الضابط"]
        print(f"  {x['مصدر']}: المودَع ⟶ قلبُ القطبين {m['قلبُ_القطبين']} · "
              f"قلبُ بتٍّ {m['قلبُ_بتٍّ_واحد']} · حذفُ بتٍّ {m['حذفُ_بتٍّ_واحد']}")
        print(f"     الضابطُ (قناةٌ فيها بتٌّ محشوّ) ⟶ قلبُ بتٍّ {g['قلبُ_بتٍّ_واحد']} "
              f"· بتٌّ بلا أثر {g['بتٌّ_بلا_أثر']}")
        print(f"     بتٌّ بلا أثرٍ في المودَع: {x['بتٌّ_بلا_أثر']} — {x['حدّ']}")
    print("\n— قوّةُ المقياس: أيَرُدُّ المصنوع؟ —")
    for p in J["قوّةُ_المقياس"]:
        print(f"  {p['مصدر']}: عُرض {p['مصنوعاتٌ_عُرضت']} · رُدَّ {p['مصنوعاتٌ_رُدَّت']} "
              f"· مرَّ {p['مصنوعاتٌ_مرّت']}")
        for r in p["صفوف"]:
            print(f"     {'رُدَّ' if not r['قام'] else '⚑ مرَّ':<8}{r['مصنوع']}")
    print("\n— ضوابطُ المثل: أمجّانيٌّ رقمُ المطابقة؟ —")
    for r in J["ضوابطُ_المثل"]:
        print(f"  {r['مصدر']}: أضدادٌ طُويت وفُكَّت {r['أضدادٌ_طُويت_وفُكَّت']}/"
              f"{r['أضدادٌ']} · المودَع {r['بتّاتُ_المودَع']:,} ⟷ أدنى ضدٍّ "
              f"{r['أدنى_ضدٍّ']:,} · غلبَ={r['غلبَ_أدنى_ضدٍّ']}")
        print(f"     {r['حدّ']}")
    h = J["الخواءُ_المسمّى"]
    print(f"\n— الخواءُ المسمّى — نصيبُ الصفر {h['نصيبُ_الصفر']} "
          f"(أقصى بعدٍ عن النصف {h['أقصى_بعدٍ_عن_النصف']}): {h['حدّ']}")
    c = J["العبور"]
    print(f"\n— العبور — قام {c['عبورٌ_قام']} · سقط {c['عبورٌ_سقط']} "
          f"· محارفُ مشتركة {c['محارفُ_مشتركة']}")
    for r in c["صفوف"]:
        print(f"     جدولُ «{r['جدول']}» على نصِّ «{r['نصّ']}»: "
              f"{'قام' if r['قام'] else 'سقط — ' + (r['سبب'] or '')}")
    print("\n— ديونٌ تُسمّى بلا رقم —")
    for d in J["ديونٌ_مسمّاة"]:
        print(f"  · {d}")
    t = J["محاولاتُ_تكذيب"]
    print(f"\nمحاولاتُ التكذيب: {t['عدد']} · رُدَّت {t['رُدَّت']} · نجحت {t['نجحت']}")
    k = J["حكم"]
    print(f"\nالحكم: معيَّن={k['معيَّن']} · مميَّز={k['مميَّز']} · "
          f"يُطوى ويُفَكّ={k['يُطوى_ويُفَكّ']} · المطابقةُ ذاتُ مضمون="
          f"{k['المطابقةُ_ذاتُ_مضمون']} · غلبَ ضوابطَ المثل="
          f"{k['غلبَ_ضوابطَ_المثل']}")
    if J["سقوط"]:
        print("::error::الجسرُ سقط")


def write_doc(R, path):
    J = R["الجسر_v0"]
    M = J["مقيس"]
    L = ["# JISR — بابُ الجسر: بين البتِّ والأبجدية",
         "",
         "> **مولَّدةٌ آليًّا** بـ`python jisr_gate.py --doc JISR.md`، ويصادمُها CI "
         "بفارق صفر. لا تُحرَّر بيد.",
         "",
         "## ① الدعوى الثلاثية",
         "",
         "| المطلوب | المقياس | الحكم |",
         "|---|---|---|",
         f"| **التعيين** — لكلِّ محرفٍ كلمةُ بتٍّ واحدة | تباينٌ وبادئيّة | "
         f"{M['تعيينٌ_متباينٌ_بادئيّ']}/{M['مصادرُ_مختومة']} |",
         f"| **التمييز** — ٠ و١ ليسا اسمين لشيء | بتٌّ بلا أثرٍ في المودَع، "
         f"وقوّةُ المقياس على ضابطٍ أعمى | {M['بتٌّ_بلا_أثر']} (المطلوب صفر) · "
         f"الضابط {M['بتٌّ_بلا_أثرٍ_في_ضابطِ_التمييز']} (المطلوب موجبًا) |",
         f"| **الطيُّ والفكّ** | مصادمةُ الأصل | "
         f"{M['طيٌّ_وفكٌّ_قام']}/{M['مصادرُ_مختومة']} |",
         "",
         "## ② الفخُّ المنصوبُ له",
         "",
         "الطيُّ ثمّ الفكُّ يُعطي المطابقةَ التامّةَ **لأيِّ تقابلٍ كان** — فهي "
         "تحصيلُ حاصلٍ لا برهان، من جنس هويّة `induction/mirror.py` الساقطة. "
         f"فعُرض على المقياس نفسِه **{M['مصنوعاتٌ_عُرضت']}** تعيينًا مصنوعًا، "
         f"فردَّ **{M['مصنوعاتٌ_رُدَّت']}** ومرَّ **{M['مصنوعاتٌ_مرّت']}**.",
         "",
         "## ③ المصادر — مختومةٌ قبل أن يُعَدَّ منها محرف",
         "",
         "| المصدر | سندُ الختم | أبجدية | محارف | بتّاتُ الطيّ | ثابتُ العرض | مكسب | بتٌّ/محرف |",
         "|---|---|---|---|---|---|---|---|"]
    for s in J["مصادر"]:
        L.append(f"| {s['اسم']} | `{s['سندُ_الختم']}` | {s['أبجدية']} | "
                 f"{s['محارف']:,} | {s['بتّاتُ_الطيّ']:,} | {s['ثابتُ_العرض']:,} | "
                 f"{s['مكسبُ_التعيين']:,} ({s['نصيبُ_المكسب']}) | {s['بتٌّ_للمحرف']} |")
    L += ["",
          "والمكسبُ هو **مضمونُ التعيين**: تقابلٌ بلا بنيةٍ يُطوى ويُفَكُّ أيضًا، "
          "ولا يكسب شيئًا. فالفرقُ عن ثابت العرض هو ما يُميِّز تعيينًا ذا سندٍ من "
          "تسميةٍ حرّة.",
          "",
          "## ④ التمييز — مقيسٌ بالفكِّ لا بالعدّ",
          "",
          "«لم يتبدّل» **مُحالٌ بالبناء** متى كان التعيينُ متباينًا بادئيًّا: الطيُّ "
          "دالّةٌ، فلا تيّارانِ مختلفان يُعطيان نصًّا واحدًا. فالمصادماتُ على المودَع "
          "**لازمُ بناءٍ لا برهانُ تمييز** — وهذا يُقال ولا يُسكَت عنه. وإنّما يَصدُق "
          "حكمُها إن أثبتَت قوّتَها على **ضابطٍ أعمى**: قناةٍ تَحشو بتًّا بعد كلِّ "
          "كلمةٍ وتقفزه في الفكّ، ففيها بتٌّ لا خبرَ فيه بالبناء.",
          "",
          "| المصدر | المقام | قلبُ القطبين | قلبُ بتٍّ | حذفُ بتٍّ | بتٌّ بلا أثر |",
          "|---|---|---|---|---|---|"]
    for x in J["التمييز"]:
        for lbl, d in (("المودَع", x["المودَع"]), ("الضابطُ الأعمى", x["الضابط"])):
            L.append(f"| {x['مصدر']} | {lbl} | {d['قلبُ_القطبين']} | "
                     f"{d['قلبُ_بتٍّ_واحد']} | {d['حذفُ_بتٍّ_واحد']} | "
                     f"{d['بتٌّ_بلا_أثر']} |")
    h = J["الخواءُ_المسمّى"]
    L += ["",
          f"العيّنةُ **{FLIP_SAMPLE}** موضعًا ببذرةٍ معلنة (`{FLIP_SEED}`) لكلِّ مصادمة.",
          "",
          "## ⑤ الخواءُ المسمّى — ما لا يميِّز وإن أوهم",
          "",
          f"نصيبُ الصفر: **{h['نصيبُ_الصفر']}** · أقصى بعدٍ عن النصف "
          f"**{h['أقصى_بعدٍ_عن_النصف']}**.",
          "",
          f"> {h['حدّ']}.",
          "",
          "## ⑥ المصنوعاتُ المعروضة",
          "",
          "| المصدر | المصنوع | الحكم |",
          "|---|---|---|"]
    for p in J["قوّةُ_المقياس"]:
        for r in p["صفوف"]:
            L.append(f"| {p['مصدر']} | {r['مصنوع']} | "
                     f"{'رُدَّ' if not r['قام'] else '⚑ مرَّ'} |")
    L += ["",
          "## ⑥½ ضوابطُ المثل — برهانُ أنّ رقمَ المطابقة مجّانيّ",
          "",
          "| المصدر | أضدادٌ طُويت وفُكَّت | بتّاتُ المودَع | أدنى ضدٍّ | فرق | غلبَ |",
          "|---|---|---|---|---|---|"]
    for r in J["ضوابطُ_المثل"]:
        L.append(f"| {r['مصدر']} | {r['أضدادٌ_طُويت_وفُكَّت']}/{r['أضدادٌ']} | "
                 f"{r['بتّاتُ_المودَع']:,} | {r['أدنى_ضدٍّ']:,} | "
                 f"{r['فرقٌ_عن_أدنى_ضدٍّ']:,} | "
                 f"{'نعم' if r['غلبَ_أدنى_ضدٍّ'] else '⚑ لا'} |")
    L += ["",
          "الضدُّ هو جدولُ التعيين نفسُه وقد خُلطت نسبةُ كلماتِه إلى محارفه ببذرةٍ "
          f"معلنة (`{FLIP_SEED}`). فهو **متباينٌ بادئيٌّ كالأصل سواءً بسواء** — "
          "ومن ثَمَّ يُطوى ويُفَكُّ مطابقةً تامّةً هو أيضًا.",
          "",
          "> وهذا بعينه **برهانُ خواء رقم المطابقة**: أحدَ عشرَ ضدًّا نالته كلُّها. "
          "فلا يبقى للتعيين المودَع فضلٌ إلّا **الثمن**، وهو مقيسٌ أعلاه.",
          ""]
    c = J["العبور"]
    L += ["",
          "## ⑦ العبور بين المصدرين",
          "",
          f"قام **{c['عبورٌ_قام']}** · سقط **{c['عبورٌ_سقط']}** · محارفُ مشتركة "
          f"**{c['محارفُ_مشتركة']}**.",
          "",
          "| جدول | نصّ | الحكم |",
          "|---|---|---|"]
    for r in c["صفوف"]:
        L.append(f"| {r['جدول']} | {r['نصّ']} | "
                 f"{'قام' if r['قام'] else 'سقط'} |")
    L += ["",
          f"> {c['حدّ']}.",
          "",
          "## ⑧ ديونٌ تُسمّى بلا رقم",
          ""]
    for d in J["ديونٌ_مسمّاة"]:
        L.append(f"- {d}")
    t = J["محاولاتُ_تكذيب"]
    L += ["",
          "## ⑨ محاولاتُ التكذيب",
          "",
          f"**{t['عدد']}** محاولةً تُشغَّل ولا تُقرَأ · رُدَّت **{t['رُدَّت']}** · "
          f"نجحت **{t['نجحت']}**. ونجاحُ واحدةٍ يُسقِط البابَ.",
          "",
          "| المحاولة | الحكم |",
          "|---|---|"]
    for r in t["صفوف"]:
        L.append(f"| {r['محاولة']} | {'رُدَّت' if r['رُدَّت'] else '⚑ نجحت'} |")
    L += ["",
          "## ⑩ التسجيلُ المسبق",
          ""]
    for p in J["التسجيلُ_المسبق"]:
        L.append(f"- {p}")
    L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(argv=None):
    ap = argparse.ArgumentParser(description="بابُ الجسر: بين البتِّ والأبجدية")
    ap.add_argument("--json", metavar="مسار", help="إيداعُ القياس (jisr_v0.json)")
    ap.add_argument("--doc", metavar="مسار", nargs="?", const="JISR.md",
                    help="الوثيقةُ المولَّدة (JISR.md ما لم يُسمَّ غيرُها)")
    a = ap.parse_args(argv)
    try:
        R = run()
        if a.json:
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(R, fh, ensure_ascii=False, indent=2, sort_keys=True)
            print(f"JSON ⟵ {a.json}")
        if a.doc:
            write_doc(R, a.doc)
            print(f"الوثيقة ⟵ {a.doc}")
        show(R)
        if R["الجسر_v0"]["سقوط"]:
            return E_BRIDGE
    except JisrError as exc:
        print(f"صريخ: {exc.message}", file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    sys.exit(main())
