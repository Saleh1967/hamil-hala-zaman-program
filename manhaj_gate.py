# manhaj_gate.py — بابُ المنهج: مراجعةُ كيفيّةِ بنائهم قبل الحكمِ على بنائهم.
#
# ــ ٠) المسبارُ مُعلَنٌ قبل التجميد، ولا يُكتَم ـــــــــــــــــــــــــــــــــــــــــــ
# هذا البابُ سُبق بمسبارٍ على بايتات مغني اللبيب المختومة، وحصيلتُه أسقطت أربعةَ
# افتراضاتٍ كانت في خطّته الأولى — فتُكتَب ههنا لا في تقريرٍ يُنسى:
#   ① **لا وسمَ للشاهد ولا عنوانَ للقاعدة**: في شاهد الجامع الكبير صفرُ عنوانٍ (`###`)،
#      وفي شاهد الشيعة صفر، وفي شاهد الشاملة عناوينُ جلُّها أرقامٌ خاوية. ولفظُ «الشاهد»
#      تسعُ مرّاتٍ في مئةٍ وإحدى وخمسين ألفَ كلمة. فالقاعدةُ والشاهدُ **لا يُنتزعان**.
#   ② **ووسمُ الاقتباس صنعةُ ناسخٍ لا نصُّ مؤلِّف**: `@QB@` في شاهد الجامع الكبير آلافٌ،
#      وفي الشاهدين الآخرين **صفر**. فالمرايا تتخالف في الوسم نفسِه — ولذلك يُقاس الوسمُ
#      ويُودَع تخالفُه، و**لا يُتَّخذ سندًا** البتّة: الجسرُ صيغةُ التصريح التي في الشهود كلِّهم.
#   ③ **والحدّان لا يتقاطعان إلا في سُدس العُشر**: مادّتُه التي تقع في المجمَّد حرفًا
#      نسبةٌ صغيرةٌ تُشتقُّ أدناه. فـ«عددُ شواهدها الكامل في D» مقامٌ لا وجودَ له لأكثرِ
#      مادّته — وهذا **حدُّنا لا حدُّهم**، صنفًا خامسًا في دفتر العطوب لا يُخلَط بالأربعة.
#   ④ **والضابطُ لا يُستخرَج — يُعلَن**: نصُّهم نثرٌ بلا وسم، فالمتاحُ صادقًا مرساةٌ عندهم
#      ومقامٌ تنفيذيٌّ بأيدينا وحقلٌ مُصرَّحٌ به أنّ الترجمةَ يدوية. وادّعاءُ الانتزاع
#      اختلاقُ وسمٍ لم يكتبوه، وهو من جنس اختلاق البايتات الممنوع.
#
# ــ ١) العلّةُ التي يفتحها هذا الباب ـــــــــــــــــــــــــــــــــــــــــــــــــــــ
# النقدُ الجافُّ لقواعدهم بلا معرفةِ كيف بنوها يُنتج ظلمًا مزدوجًا: يحكم على صوابٍ خارجَ D
# فيظلمه، ويُقرُّ خطأً لأنّه لا يعرف أين يقف الضابطُ عندهم. فالمقصودُ ههنا ليس الحكمَ على
# القواعد، بل **ثلاثةُ أرقام**: ما صمد من ترجمتنا لضابطهم · توزيعُ أصنافِ العطب ·
# وحجمُ ما خرج عن حدِّنا معدودًا لا مُهمَلًا.
#
# ــ ٢) والكيلُ ليس هنا ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# كلُّ بتٍّ يخرج من `deposit_law.price`، وكلُّ حكمٍ من `deposit_law.verdict`، و`ω` و`n₀`
# من `alama_layer` — تُستدعى ولا تُنسَخ. ولا مكيالَ خاصًّا بهذا الباب: بابٌ يكيل بمكياله
# يعيد العطلَ الذي قتله `sole_judge`.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بايتاتُ شاهدٍ غائبة · 4 ختمٌ أو مرساةٌ خالفت.
#
# التشغيل:
#   bash fetch_source.sh --fetch ibnhisham_mughni_jk     (وأخواه — شبكةٌ مرّةً واحدة)
#   python manhaj_gate.py                 تقريرٌ معدودٌ على stdout
#   python manhaj_gate.py --json <ملفّ>   الوديعةُ إلى ملفّ (مولِّدُ الأختام)
#
# ⚑ ولا يُمَسُّ معجمٌ ولا كلفةٌ سابقة: هذه طبقةُ مراجعةٍ لمنهجٍ يدويّ، لا تصنيفُ كلمات.
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from math import lgamma, log, log2

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "induction"))

import sources_census                                   # لا نسخةَ ثانيةَ من مصادمة البايتات
from induction_engine import parse_verses, TAN          # ولا قارئَ ثانيًا للمجمَّد
from deposit_law import price, verdict, ALPHA
from alama_layer import omega_drop                      # ω = 0 يحذف الحافةَ لا العقدة

CORPUS = os.path.join(ROOT, "induction", "mujammad.txt")

E_USAGE = 2
E_MISSING = 3
E_SEAL = 4


class ManhajError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ═══ التطبيعُ والقراءة ═══════════════════════════════════════════════════════════════
_STRIP = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")
_FOLD = {"\u0671": "ا", "\u0622": "ا", "\u0623": "ا", "\u0625": "ا",
         "\u0649": "ي", "\u0629": "ه", "\u0624": "و", "\u0626": "ي"}
_NONAR = re.compile(r"[^\u0621-\u064A\s]")


def fold(text):
    """تطبيعٌ واحدٌ يُطبَّق على الطرفين معًا — فلا يُقارَن مطبَّعٌ بغير مطبَّع."""
    text = _STRIP.sub("", text)
    for a, b in _FOLD.items():
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", _NONAR.sub(" ", text)).strip()


# ═══ الإعلاناتُ المجمَّدةُ قبل القياس ════════════════════════════════════════════════
# ثلاثةُ شهودٍ لكتابٍ واحد: لا يُوسَّط بينهم ولا يُنتقى أحدُهم صامتًا. والمرساةُ في
# **شاهدٍ واحدٍ مسمًّى** لأنّ الإزاحةَ خاصّةُ بايتاتِه، ولا تنتقل إلى غيره بحال.
WITNESSES = ("ibnhisham_mughni_jk", "ibnhisham_mughni_sham", "ibnhisham_mughni_shia")
ANCHOR_WITNESS = "ibnhisham_mughni_jk"

# صيغُ التصريح بالاستشهاد — **قائمةٌ مرتَّبةٌ مجمَّدة**، والترتيبُ جزءٌ من الوديعة:
# الموضعُ يقع في أوّلِ صيغةٍ تطابقه ولا يُعَدّ مرّتين (سنّةُ BARE_ORDER في باب العلامة).
# والأطولُ أوّلًا وجوبًا، وإلّا ابتلعت «قوله تعالى» ما هو «وقوله تعالى» فضاع التمييز.
TASRIH_FORMS = (
    "قال الله تعالى",
    "وقوله تعالى",
    "قوله تعالى",
    "قال تعالى",
    "قوله سبحانه",
)

# وسمٌ يُقاس ولا يُتَّخذ سندًا: قد يكون في شاهدٍ ويغيب عن أخويه.
MARKUP = ("@QB@", "@QE@")

# حروفُ المضارعة بعد التطبيع (أ ⟵ ا) — معلنةٌ قبل القياس.
MUDARAA = ("ا", "ن", "ي", "ت")
# الجوارُّ الخمسةُ المعلنةُ في induction_engine — وتُكتَب ههنا **بعد التطبيع** وجوبًا:
# «على» تصير «علي» و«إلى» تصير «الي»، فلو كُتبت بصورتها المرسومة لما طابقت شيئًا
# و**لسقط ثلثا مواضع الإطلاق صامتين**. وهذا عطلٌ وقع فعلًا في أوّل تشغيلٍ فأُصلح.
# الأحكامُ المجمَّدة: تُشتقُّ من مواضعها في كلِّ تشغيلٍ وتُصادَم بفارق صفرٍ في `run`.
# وكلُّ تغييرٍ في التقشير أو في الشهود أو في المقامات يُسقِط البابَ ههنا — لا في التقرير.
SEALED_MANHAJ = {
    "مواضعُ_تصريحٍ_في_المُرسى": 426, "مطابقٌ_في_المُرسى": 409,
    "وسمٌ_في_المُرسى": 2784, "وسمٌ_في_الشاملة": 0, "وسمٌ_في_الشيعة": 0,
    "كلماتُ_المُرسى": 151161, "واقعٌ_في_حدِّنا": 9535,
    "إطلاقُ_لن": 59, "إطلاقُ_لم": 163, "إطلاقُ_أل": 11855, "إطلاقُ_الجارّة": 4890,
    "ذوبانُ_لم": 3, "ذوبانُ_الجارّة": 34,
    "صامد": 4, "مختبَر": 4,
}

JAR_WORDS = tuple(fold(w) for w in ("من", "عن", "على", "في", "إلى"))
TANWIN = tuple(TAN.values())

# نافذةُ الجسر: كم كلمةً تُقرأ بعد صيغة التصريح، وأطولُ مطابقةٍ وأدناها.
BRIDGE_WINDOW = 8
BRIDGE_MAX = 6
BRIDGE_MIN = 2
COVERAGE_N = 5                       # شبكةُ قياسِ «ما خرج عن D» — معلنةٌ لا مختارةٌ بعدُ

# الفواصلُ وحدودُ الشواهد: لكلِّ واحدٍ اتجاهاه وتبريرُه، ولا فاصلَ يُنقَل عادةً من باب.
THRESHOLDS = {
    "n₀ مواضع": dict(قيمة=30,
                     اتجاهان="مواضعُ إطلاقٍ ≥ 30 ⟵ يُقاس · دونها ⟵ «غيرُ مختبَر» لا «صامد»",
                     تبرير=("الصدقُ الخاوي: ضابطٌ لا يُطلِقه إلا مواضعُ قليلةٌ يصدُق بلا "
                            "استثناءٍ لأنّه لم يُعرَض للتكذيب أصلًا. والثلاثون أدنى ما "
                            "يجعل نسبةَ شذوذٍ قدرُها 1/30 دون فاصل الشذوذ المعلن — فلا "
                            "يصير الحدُّ الأدنى بابًا خلفيًّا لقبول الشاذّ")),
    "فاصلُ الشذوذ": dict(قيمة=0.05,
                        اتجاهان="مخالفاتٌ ≤ 5% من مواضع الإطلاق ⟵ يصمد · فوقها ⟵ ساقط",
                        تبرير=("فوق هذا الحدِّ لا تكون المخالفةُ شاذًّا يُقصى بل بابًا ثانيًا "
                               "أُهمِل — وهذا صنفُ العطب الرابع بعينه. ولا يُرفَع الفاصلُ "
                               "ليمرَّ ضابطٌ، ولا يُخفَّض ليسقط: المخالفاتُ مدفوعةُ الثمن "
                               "في الفاتورة على كلِّ حال، فالفاصلُ حكمٌ لا حيلةُ ترميز")),
    "Δ الضابط": dict(قيمة=0.0,
                     اتجاهان="Δ < 0 ⟵ العلّةُ موزونة · Δ ≥ 0 ⟵ علّةٌ بلا وزن",
                     تبرير=("حدُّ deposit_law.verdict بحرفه ولا يُلَيَّن: ضابطٌ لا يشتري بتًّا "
                            "واحدًا في وصف D وصفٌ لما وقع لا قاعدةٌ تولِّده. ورفعُ الحدِّ "
                            "يشتري قبولًا بالاصطلاح لا بالبتّات")),
    "حدُّ المطابقة": dict(قيمة=BRIDGE_MIN,
                          اتجاهان="كلمتان متّصلتان فأكثرُ ⟵ مطابقٌ مُرسًى · دونهما ⟵ فشلٌ مسمًّى",
                          تبرير=("الكلمةُ الواحدةُ تقع في المجمَّد بالمصادفة (حروفُ الجرّ "
                                 "والضمائرُ تقع آلافًا)، فلا تكون مطابقةً. والكلمتان أدنى "
                                 "ما يُخرِج المصادفةَ ويُبقي الاستشهادَ القصيرَ مرصودًا — "
                                 "ورفعُه إلى ثلاثٍ يطوي استشهاداتٍ واقعةً فيصير الفشلُ مصنوعًا")),
}

# ═══ المراسي: مُعرِّفُ شاهدٍ مختوم · إزاحةُ بايت · طولٌ · بصمةُ المقتطَع ══════════════
# الإزاحةُ تُجمَّد ههنا، والبصمةُ تُشتقُّ من البايتات عند كلِّ تشغيلٍ وتُصادَم. فإن زحفت
# بايتةٌ واحدةٌ سقطت المرساةُ باسمها — وهذا هو «الاقتباسُ بالبصمة لا بالاسم» مطبَّقًا
# على نصٍّ خارج الشجرة لأوّل مرّة. ويُشترَط مع ذلك أن يكون المقتطَعُ **فريدًا** في بايتات
# الشاهد: المرساةُ المتكرّرةُ إشارةٌ غامضةٌ تصدُق على موضعين، فلا تُرسي شيئًا.
ANCHORS = {
    "لن": dict(شاهد=ANCHOR_WITNESS, إزاحة=1428189, طول=44,
               بصمة="eb87bb31fd89fd61bc1710772fda027c360cd528d59373e6f61f95931c15dfb7"),
    "لم": dict(شاهد=ANCHOR_WITNESS, إزاحة=580971, طول=59,
               بصمة="3758e3c5806c5e8c67addddd3296f636a6f04a914cb365e6215c68ded8425500"),
    "التنوين وأل": dict(شاهد=ANCHOR_WITNESS, إزاحة=1372513, طول=40,
                        بصمة="578a57ce9ad0231a7865ef3156acb1319034d56d00bf1b5cfc700c0e63d8fbd7"),
    "الباء جارّة": dict(شاهد=ANCHOR_WITNESS, إزاحة=210399, طول=66,
                        بصمة="5052f8cd943ffa939ddccbbada06a9729eb0618e1611facbd5321c7cc43ea9e0"),
}


# ═══ ① وعاءُ الاقتباس المُرسى ═══════════════════════════════════════════════════════
def witness_bytes(source_id):
    """بايتاتُ شاهدٍ مختوم، مصادَمةً بالبيان قبل أن تُقرَأ — لا نسخةَ ثانيةَ للمصادمة."""
    try:
        rows = sources_census.manifest_rows()
        path, digest = sources_census.sealed_bytes(source_id, rows)
    except sources_census.CensusError as exc:
        raise ManhajError(exc.code, exc.message) from exc
    return open(path, "rb").read(), digest


def sanad_anchor(name, blob):
    """المرساةُ مصادَمةً: بصمةُ المقتطَع عند الإزاحة المجمَّدة، وفرادتُه في الشاهد.

    يُرَدّ سجلُّ المرساة، ويُصرَخ بالمخرج 4 إن خالفت البصمةُ أو تكرّر المقتطَع أو خرجت
    الإزاحةُ عن الشاهد. ولا يُبحَث عن النصِّ ليُصحَّح موضعُه: المرساةُ إزاحةٌ مجمَّدةٌ
    تُصادَم، ولو بحثنا عنه لصار الاسمُ هو السندَ من جديد.
    """
    a = ANCHORS[name]
    off, ln = a["إزاحة"], a["طول"]
    if off < 0 or off + ln > len(blob):
        raise ManhajError(E_SEAL, f"مرساةُ «{name}»: إزاحةٌ خارج الشاهد ({off}+{ln})")
    cut = blob[off:off + ln]
    got = hashlib.sha256(cut).hexdigest()
    if got != a["بصمة"]:
        raise ManhajError(
            E_SEAL, f"مرساةُ «{name}»: البصمةُ {got} والمجمَّدُ {a['بصمة']} — إزاحةٌ زحفت")
    if blob.count(cut) != 1:
        raise ManhajError(
            E_SEAL, f"مرساةُ «{name}»: المقتطَعُ متكرِّرٌ {blob.count(cut)} مرّةً — إشارةٌ غامضة")
    return dict(اسم=name, شاهد=a["شاهد"], إزاحة=off, طول=ln, بصمة=got,
                نصّ=cut.decode("utf-8", "replace"))


def witness_words(blob):
    """كلماتُ الشاهد بعد نزع الترويسة وأرقام الصفحات ووسمِ الناسخ."""
    text = blob.decode("utf-8-sig", "replace")
    if "#META#Header#End#" in text:
        text = text.split("#META#Header#End#", 1)[1]
    text = re.sub(r"PageV\d+P\d+", " ", text)
    for m in MARKUP:
        text = text.replace(m, " ")
    return fold(text).split()


def corpus_tokens():
    """المجمَّدُ رموزًا: لكلِّ كلمةٍ صورتُها المطبَّعةُ وهيئاتُها — بقارئ induction_engine."""
    verses = parse_verses(CORPUS)
    toks = []
    for vi, words in enumerate(verses):
        for wi, w in enumerate(words):
            skel = fold("".join(ch for ch, _ in w))
            toks.append(dict(صورة=skel, هيئات=[st for _, st in w],
                             آية=vi, موضع=wi, آخرُ_الآية=wi == len(words) - 1))
    return toks


def ngram_index(forms, n):
    idx = {}
    for i in range(len(forms) - n + 1):
        idx.setdefault(tuple(forms[i:i + n]), []).append(i)
    return idx


# ═══ ② جسرُ الاستشهاد المصرَّح ══════════════════════════════════════════════════════
def tasrih_sites(blob):
    """مواضعُ صيغ التصريح ببايتاتها — أطولُ صيغةٍ أوّلًا ولا موضعَ يُعَدّ مرّتين."""
    sites = []
    taken = []
    for form in TASRIH_FORMS:
        pat = form.encode()
        start = 0
        while True:
            i = blob.find(pat, start)
            if i < 0:
                break
            start = i + 1
            if any(i < e and i + len(pat) > s for s, e in taken):
                continue
            taken.append((i, i + len(pat)))
            sites.append(dict(صيغة=form, إزاحة=i, طول=len(pat)))
    sites.sort(key=lambda s: s["إزاحة"])
    return sites


def tasrih_bridge(source_id, idx_by_n, verbose_cap=4):
    """لكلِّ موضعِ تصريحٍ: مرساةٌ في الشاهد ومطابقٌ في D — أو **فشلٌ مسمًّى**.

    لا يُستعمَل وسمُ الناسخ (`@QB@`) البتّة: هو في شاهدٍ ويغيب عن أخويه، فاتخاذُه سندًا
    يجعل العددَ دالّةَ نسخةٍ لا دالّةَ كتاب. والمطابقةُ أطولُ سلسلةٍ متّصلةٍ تقع في
    المجمَّد بحرفها، ودونَ حدِّ المطابقة المعلن **فشلٌ يُسمّى ويُعَدّ** ولا يُطوى.
    """
    blob, digest = witness_bytes(source_id)
    sites = tasrih_sites(blob)
    lengths = Counter()
    failures = Counter()
    spans = []
    samples = []
    for s in sites:
        start = s["إزاحة"] + s["طول"]
        after = blob[start:start + 400].decode("utf-8", "ignore")
        for m in MARKUP:
            after = after.replace(m, " ")
        words = fold(re.sub(r"PageV\d+P\d+", " ", after)).split()[:BRIDGE_WINDOW]
        hit = 0
        pos = None
        for n in range(min(BRIDGE_MAX, len(words)), BRIDGE_MIN - 1, -1):
            key = tuple(words[:n])
            if key in idx_by_n[n]:
                hit, pos = n, idx_by_n[n][key][0]
                break
        if hit:
            lengths[hit] += 1
            spans.append((pos, pos + hit))
        else:
            kind = ("كلماتٌ دون حدِّ المطابقة" if len(words) < BRIDGE_MIN
                    else "لا مطابقَ في المجمَّد")
            failures[kind] += 1
            if len(samples) < verbose_cap:
                samples.append(dict(إزاحة=s["إزاحة"], صيغة=s["صيغة"],
                                    تلاها=" ".join(words[:5]), فشل=kind))
    matched = sum(lengths.values())
    return dict(
        شاهد=source_id, بصمة=digest,
        مواضعُ_التصريح=len(sites),
        صيغ=dict(Counter(s["صيغة"] for s in sites)),
        مطابق=matched,
        أطوالُ_المطابقة={str(k): v for k, v in sorted(lengths.items(), reverse=True)},
        فشلٌ_مسمًّى=dict(failures),
        نسبةُ_المطابقة=round(matched / len(sites), 4) if sites else 0.0,
        أمثلةُ_الفشل=samples,
        وسمُ_الناسخ=sum(blob.count(m.encode()) for m in MARKUP[:1]),
    ), spans


def markup_divergence(counts):
    """تخالفُ المرايا في الوسم — يُودَع ولا يُوسَّط، ويُمنَع اتخاذُه سندًا."""
    present = [w for w, n in counts.items() if n > 0]
    return dict(
        عدد=counts, حاضرٌ_في=present, غائبٌ_عن=[w for w in counts if w not in present],
        حكم=("الوسمُ في شاهدٍ واحدٍ وغائبٌ عن أخويه — فهو صنعةُ ناسخٍ لا نصُّ مؤلِّف"
             if len(present) < len(counts) else "الوسمُ في الشهود كلِّهم"),
        يُتَّخذُ_سندًا=False,
    )


# ═══ ③ دفترُ ضوابطهم — مُعلَنًا لا مُستخرَجًا ═══════════════════════════════════════
def _initial(tok):
    return tok["صورة"][0] if tok["صورة"] else ""


def _is_jar_by_mark(tok):
    """جارّةٌ **بعلامتها**: «مِن» بكسر الميم · «عَن» بفتح العين · على/في/الى بصورتها.

    وهذا هو موضعُ الترجمة اليدوية: النحويُّ يميّز مِنْ الجارّةَ من مَنْ الموصولة بحسِّه،
    ونحن نميّزهما **بالعلامة المرسومة** — وهي في المجمَّد مقيسةٌ لا مقدَّرة.
    """
    s = tok["صورة"]
    if s == "من":
        return tok["هيئات"][0] == "كسرة"
    if s == "عن":
        return tok["هيئات"][0] == "فتحة"
    return s in JAR_WORDS


def _is_jar_by_shape(tok):
    """الصورةُ وحدَها بلا علامة — مقامُ من لا يرى الحركة. يُقاس ليُظهِر الذوبان."""
    return tok["صورة"] in JAR_WORDS


def dabit_fields(toks):
    """المقاماتُ الأربعةُ منفَّذةً على D: لكلِّ ضابطٍ كونٌ وإطلاقٌ ومرخَّصٌ وصورةٌ ساذجة.

    الكونُ (universe) تيّارُ رموزٍ واحدٌ يشمل مواضعَ الإطلاق وغيرَها، والضابطُ يدّعي على
    مواضع إطلاقِه وحدَها. وهذه هي الصيغةُ الخارجةُ من الدور: **هل تُرخِّص معرفةُ الضابط
    ترميزَ تلك المواضع أرخص؟** — لا «كم شاهدًا يوافقه».
    """
    n = len(toks)
    nxt_initial = [_initial(toks[i + 1]) for i in range(n - 1)]
    last_state = [t["هيئات"][-1] if t["هيئات"] else "عري" for t in toks]
    nxt_is_jar = ["جارّة" if _is_jar_by_mark(toks[i + 1]) else "سواها" for i in range(n - 1)]
    nxt_is_jar_shape = ["جارّة" if _is_jar_by_shape(toks[i + 1]) else "سواها"
                        for i in range(n - 1)]

    def trig_lan(i):
        return toks[i]["صورة"] == "لن"

    def trig_lam(i):
        return toks[i]["صورة"] == "لم" and toks[i]["هيئات"][-1] == "سكون"

    def trig_lam_naive(i):
        return toks[i]["صورة"] == "لم"

    def trig_al(i):
        return toks[i]["صورة"][:2] == "ال" and len(toks[i]["صورة"]) > 2

    states = sorted(set(last_state))
    licensed_al = tuple(s for s in states if s not in TANWIN)
    shapes = [t["صورة"] for t in toks]

    out = {
        "لن": dict(كون=nxt_initial, إطلاق=[i for i in range(n - 1) if trig_lan(i)],
                   مرخَّص=MUDARAA, ساذج=[i for i in range(n - 1) if trig_lan(i)],
                   كونٌ_ساذج=nxt_initial),
        "لم": dict(كون=nxt_initial, إطلاق=[i for i in range(n - 1) if trig_lam(i)],
                   مرخَّص=MUDARAA, ساذج=[i for i in range(n - 1) if trig_lam_naive(i)],
                   كونٌ_ساذج=nxt_initial),
        "التنوين وأل": dict(كون=last_state, إطلاق=[i for i in range(n) if trig_al(i)],
                            مرخَّص=licensed_al,
                            ساذج=[i for i in range(n) if trig_al(i)], كونٌ_ساذج=last_state),
        "الباء جارّة": dict(كون=nxt_is_jar,
                            إطلاق=[i for i in range(n - 1) if _is_jar_by_mark(toks[i])],
                            مرخَّص=("سواها",),
                            ساذج=[i for i in range(n - 1) if _is_jar_by_shape(toks[i])],
                            كونٌ_ساذج=nxt_is_jar_shape),
    }
    for f in out.values():
        f["صور"] = shapes          # لتُسمَّى المخالفاتُ بصورها في الفاتورة لا تُعَدَّ صمّاء
    return out


# نصُّ الضابط عندهم (مُرسًى بالبايتات)، ومقامُنا التنفيذيُّ بإزائه — والترجمةُ يدويةٌ
# مُصرَّحٌ بها في كلِّ سطر. والقالبُ الرمزيُّ هو ما يُدفَع ثمنُه في الفاتورة مُملًى من
# الأبجدية المعلنة (ALPHA) — فلا قاعدةَ مجّانية.
DABITS = (
    dict(مفتاح="لن", قالب="لن>مضارع{ا,ن,ي,ت}",
         مقام="كلُّ «لن» يليها كلمةٌ أوّلُها حرفُ مضارعةٍ من الأربعة المعلنة",
         ترجمةٌ_يدوية=True,
         حدُّ_الترجمة=("قولُهم «حرفُ نفيٍ ونصبٍ واستقبال» يقتضي فعلًا مضارعًا بعده. "
                       "ونحن لا نملك كاشفَ فعلٍ، فترجمنا «مضارع» إلى **حرفِ مضارعةٍ في "
                       "أوّل التالي** — شرطٌ لازمٌ لا كافٍ: يصدُق على الفعل وعلى اسمٍ "
                       "بدأ بأحد الأربعة. فالضابطُ يُختبَر بلازمه، وهذا أضعفُ ممّا "
                       "قالوه لا أقوى")),
    dict(مفتاح="لم", قالب="لم[سكون]>مضارع{ا,ن,ي,ت}",
         مقام="كلُّ «لم» **ساكنةِ الميم** يليها كلمةٌ أوّلُها حرفُ مضارعة",
         ترجمةٌ_يدوية=True,
         حدُّ_الترجمة=("قيدُ السكون من عندنا لا من نصِّهم: «لم» الجازمةُ تُخالف «لِمَ» "
                       "الاستفهاميةَ في العلامة لا في الصورة. وبدونه يذوب الضابطُ — "
                       "وذلك مقيسٌ في دفتر العطوب، لا مُدَّعًى")),
    dict(مفتاح="التنوين وأل", قالب="ال~>خاتمة¬تنوين",
         مقام="كلُّ كلمةٍ مبدوءةٍ بـ«ال» لا تُختَم بتنوين",
         ترجمةٌ_يدوية=True,
         حدُّ_الترجمة=("«ال» عندنا صورةٌ في أوّل الكلمة لا «أل» التعريفيةُ بحدِّها، "
                       "ويزيدها التطبيعُ (أ ⟵ ا) فيدخل في الإطلاق نحو «أَلَمْ» و«أَلا». "
                       "والتوسيعُ **ضدَّ الضابط** لا معه: يزيد مواضعَ تكذيبه ولا ينقصها، "
                       "فما صمد عليه صمد على مقامٍ أوسعَ من مقامهم")),
    dict(مفتاح="الباء جارّة", قالب="جارّة>¬جارّة",
         مقام="الجارّةُ **بعلامتها** لا تقع قبل جارّةٍ بعلامتها",
         ترجمةٌ_يدوية=True,
         حدُّ_الترجمة=("نصُّهم يقرّر أنّ الباءَ حرفُ جرٍّ لأربعةَ عشرَ معنًى، ولم يقولوا "
                       "هذه العبارةَ بحرفها. والمقامُ لازمٌ من تعريفهم: الجارُّ يقتضي "
                       "مجرورًا، والحرفُ لا يكون مجرورًا. فهذه ترجمةٌ يدويةٌ لِلازِمِ "
                       "التعريف، وتُعلَن كذلك — لا يُدَّعى أنّها منتزَعةٌ من نصّ")),
)


# ═══ ④ الفاتورة: هل تُرخِّص معرفةُ الضابط ترميزًا أرخص؟ ══════════════════════════════
def _log2_choose(n, k):
    if k <= 0 or k >= n:
        return 0.0
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / log(2)


def dabit_bill(field, template, restrict_all=False):
    """Δ = (كلفةُ الكون بعد نزع مواضع الإطلاق + كلفةُ المواضع بالضابط + ثمنُ القالب) − كلفةُ الكون.

    الكيلُ كلُّه بـ`price` — المكيالِ العامِّ نفسِه الذي يُسعِّر المجمَّدَ والعثمانيّ.
    وثمنُ الاستثناءات **مدفوعٌ صراحة**: موضعُ كلِّ مخالفةٍ (log₂C) وصورتُها — فلا تُقصى
    الشواذُّ مجّانًا لراحة القاعدة.
    `restrict_all` هو **نزعُ شرط العلّة**: يُطبَّق الترخيصُ على الكون كلِّه لا على مواضع
    الإطلاق — فيظهر هل كان الشرطُ يحمل وزنًا أم كان زينة.
    """
    universe = field["كون"]
    trig = set(range(len(universe))) if restrict_all else set(field["إطلاق"])
    licensed = set(field["مرخَّص"])
    if not universe or not trig:
        return None
    alphabet = set(universe)
    outside = max(1, len(alphabet - licensed))

    L0 = price(universe, 0)["كلفة"]
    rest = [s for i, s in enumerate(universe) if i not in trig]
    L_rest = price(rest, 0)["كلفة"] if rest else 0.0

    n = len(trig)
    viol = [i for i in trig if universe[i] not in licensed]
    k = len(viol)
    L_trig = n * log2(max(1, len(licensed))) + _log2_choose(n, k) + k * log2(outside)
    L_model = len(template) * log2(ALPHA) + log2(n + 1)
    delta = L_rest + L_trig + L_model - L0
    shapes = field.get("صور") or []
    top = Counter(shapes[i] for i in viol if i < len(shapes)).most_common(5)
    return dict(مواضعُ_الكون=len(universe), مواضعُ_الإطلاق=n, مخالفات=k,
                صورُ_المخالفة=[[w, c] for w, c in top],
                نسبةُ_المخالفة=round(k / n, 6),
                كلفةُ_الكون=round(L0, 2), كلفةُ_المتبقّي=round(L_rest, 2),
                كلفةُ_المواضع=round(L_trig, 2), ثمنُ_القالب=round(L_model, 2),
                Δ=round(delta, 2), حكمُ_الفاتورة=verdict(delta))


# ═══ ⑤ دفترُ العطوب: خمسةُ أصنافٍ، ولكلٍّ منعٌ يُنفَّذ ═══════════════════════════════
DEFECTS = (
    ("انتقاءُ شواهدَ داخل D",
     "مخالفاتٌ واقعةٌ في حدِّنا لم يقع منها شيءٌ في مادّته المُرساة — فالعيّنةُ منتقاة",
     "ban_cherry_pick"),
    ("ذوبانُ ضابط",
     "المقامُ بالصورة وحدَها يبتلع ما ليس منه، فيصدُق الضابطُ على غير بابه",
     "ban_dissolution"),
    ("علّةٌ بلا وزن",
     "الضابطُ لا يشتري بتًّا واحدًا في وصف D — يُقاس بنزع الشرط وإعادة التسعير",
     "ban_unweighed_illa"),
    ("شاذٌّ أُقصي لراحة القاعدة",
     "المخالفاتُ فوق فاصل الشذوذ المعلن — فهي بابٌ أُهمِل لا شاذٌّ يُقصى",
     "ban_comfort_exclusion"),
    ("حدُّنا لا حدُّهم",
     "مادّةٌ استشهد بها خارجَ المجمَّد — تُعَدّ ولا تدخل الحكمَ البتّة",
     "ban_our_limit"),
)


def ban_cherry_pick(field, universe, cited_positions, toks):
    """منعُ ①: المخالفاتُ تُقاس على الكون كلِّه لا على مادّته المُرساة.

    ويُنفَّذ: يُحسَب عددُ المخالفات مرّتين — على مواضع الإطلاق كلِّها، وعلى ما وقع منها
    في مادّته وحدَها. فإن كانت في D مخالفاتٌ ولم يقع منها في مادّته شيءٌ، فالعطبُ قائم.
    """
    licensed = set(field["مرخَّص"])
    trig = field["إطلاق"]
    viol = [i for i in trig if universe[i] not in licensed]
    cited_viol = [i for i in viol if i in cited_positions]
    return dict(مخالفاتٌ_في_الكون=len(viol), منها_في_مادّته=len(cited_viol),
                عطب=bool(viol) and not cited_viol)


def ban_dissolution(field):
    """منعُ ②: يُقاس المقامُ بالصورة وحدَها بإزاء المقام بالعلامة — والفرقُ هو الذوبان."""
    licensed = set(field["مرخَّص"])
    u, un = field["كون"], field["كونٌ_ساذج"]
    precise = sum(1 for i in field["إطلاق"] if u[i] not in licensed)
    naive = sum(1 for i in field["ساذج"] if un[i] not in licensed)
    return dict(بالعلامة=dict(مواضع=len(field["إطلاق"]), مخالفات=precise),
                بالصورة=dict(مواضع=len(field["ساذج"]), مخالفات=naive),
                فرقُ_الذوبان=naive - precise, عطب=naive > precise)


def ban_unweighed_illa(field, template):
    """منعُ ③: يُنزَع شرطُ العلّة (يُطبَّق الترخيصُ على الكون كلِّه) ويُعاد التسعير."""
    with_cond = dabit_bill(field, template)
    without = dabit_bill(field, template, restrict_all=True)
    if with_cond is None or without is None:
        return dict(عطب=True, علّة="لا تيّارَ يُسعَّر")
    return dict(بالشرط=with_cond["Δ"], بنزع_الشرط=without["Δ"],
                وزنُ_الشرط=round(without["Δ"] - with_cond["Δ"], 2),
                عطب=with_cond["Δ"] >= THRESHOLDS["Δ الضابط"]["قيمة"])


def ban_comfort_exclusion(bill):
    """منعُ ④: الشاذُّ مدفوعُ الثمن في الفاتورة، وفوق الفاصل المعلن يسقط الضابط."""
    ratio = bill["نسبةُ_المخالفة"]
    cap = THRESHOLDS["فاصلُ الشذوذ"]["قيمة"]
    return dict(نسبة=ratio, فاصل=cap, ثمنُ_الاستثناءات_مدفوع=True, عطب=ratio > cap)


def ban_our_limit(rows, outside_share):
    """منعُ ⑤: رقمُ «ما خرج عن حدِّنا» يُعلَن ولا يدخل حكمًا — والمنعُ يُنفَّذ لا يُقرأ.

    ويُحرَس بشقَّين لئلّا تكون الحراسةُ صادقةً خاوية:
    ① **المطابقة**: حكمُ الخطّ المنفَّذ يُقابَل بحكمٍ يُعاد حسابُه من الفاتورة وحدَها،
       بلا أثرٍ لنصيب الخارج — ويجب أن يتطابقا حرفًا بحرف.
    ② **ذو أثر**: يُحسَب حكمٌ **ملوَّثٌ** يُحقَن فيه الرقمُ فعلًا (مواضعُ الإطلاق تُخصَم
       بنصيب ما خرج، كمن يخصم شهادةَ النحويِّ لأنّ جُلَّ مادّته خارج مجمَّدنا) — فإن
       جاء الملوَّثُ مطابقًا للنظيف فالحارسُ خاوٍ: لا يحرس شيئًا، ويسقط الباب.
    """
    clean = [rule_verdict(r["فاتورة"], r["مواضعُ_الإطلاق"]) for r in rows]
    run_time = [r["حكم"] for r in rows]
    tainted = [rule_verdict(r["فاتورة"],
                            int(r["مواضعُ_الإطلاق"] * (1.0 - outside_share)))
               for r in rows]
    return dict(نصيبُ_ما_خرج=outside_share,
                الحكمُ_المنفَّذ=run_time, الحكمُ_النظيف=clean, الحكمُ_الملوَّث=tainted,
                ذو_أثر=tainted != clean, عطب=run_time != clean)


# ═══ ⑥ الحكم: n₀ ثمّ الشذوذ ثمّ الفاتورة ════════════════════════════════════════════
def n0_gate(observed):
    t = THRESHOLDS["n₀ مواضع"]
    return observed >= t["قيمة"], t["قيمة"]


def rule_verdict(bill, triggers):
    """الحكمُ الواحد: دون n₀ «غيرُ مختبَر» — ثمّ الشذوذُ ثمّ الفاتورةُ بحكم القانون."""
    tested, _ = n0_gate(triggers)
    if not tested:
        return "غيرُ مختبَر"
    if bill["نسبةُ_المخالفة"] > THRESHOLDS["فاصلُ الشذوذ"]["قيمة"]:
        return "ساقط"
    return "صامد" if bill["حكمُ_الفاتورة"] == verdict(-1.0) else "ساقط"


# ═══ ⑦ الإحاطةُ وما خرج عن الحدّ ═════════════════════════════════════════════════════
def outside_share(words, idx_n):
    """نصيبُ مادّته التي لا تقع في حدِّنا — معدودًا لا مُهمَلًا، بشبكةٍ معلنة."""
    covered = [False] * len(words)
    for i in range(len(words) - COVERAGE_N + 1):
        if tuple(words[i:i + COVERAGE_N]) in idx_n:
            for j in range(i, i + COVERAGE_N):
                covered[j] = True
    inside = sum(covered)
    return dict(كلماتُه=len(words), واقعٌ_في_حدِّنا=inside,
                نصيبُ_الخارج=round(1 - inside / len(words), 4), شبكة=COVERAGE_N)


# ═══ ⑧ محاولاتُ التكذيب ═════════════════════════════════════════════════════════════
def falsify(blob, fields, toks, idx_by_n):
    T = []

    # ① مرساةٌ زحفت بايتةً واحدةً تُقبَل.
    saved = ANCHORS["لن"]["إزاحة"]
    ANCHORS["لن"]["إزاحة"] = saved + 1
    try:
        sanad_anchor("لن", blob)
        drift_ok = True
    except ManhajError:
        drift_ok = False
    finally:
        ANCHORS["لن"]["إزاحة"] = saved
    T.append(("مرساةٌ زاحفةٌ ببايتةٍ قُبلت", drift_ok))

    # ② مرساةٌ غيرُ فريدةٍ تُقبَل (مقتطَعٌ متكرِّرٌ إشارةٌ غامضة).
    common = blob.find("والله".encode())
    ANCHORS["فحص"] = dict(شاهد=ANCHOR_WITNESS, إزاحة=common, طول=10,
                          بصمة=hashlib.sha256(blob[common:common + 10]).hexdigest())
    try:
        sanad_anchor("فحص", blob)
        dup_ok = True
    except ManhajError:
        dup_ok = False
    finally:
        del ANCHORS["فحص"]
    T.append(("مرساةٌ غيرُ فريدةٍ قُبلت", dup_ok))

    # ③ شاهدٌ ليس في البيان يُقبَل للإرساء.
    try:
        witness_bytes("لا_وجودَ_له")
        ghost_ok = True
    except ManhajError:
        ghost_ok = False
    T.append(("شاهدٌ ليس في البيان قُبل", ghost_ok))

    # ④ نصٌّ مختلقٌ يجد مطابقًا في المجمَّد.
    fake = tuple(fold("زيدٌ قائمٌ في الدار عندنا").split())[:BRIDGE_MIN]
    T.append(("نصٌّ مختلقٌ طابق المجمَّد", fake in idx_by_n[BRIDGE_MIN]))

    # ⑤ مقامٌ يُرخِّص كلَّ شيءٍ يربح بتّات (الضابطُ الذائبُ تمامًا).
    f = dict(fields["لن"])
    f["مرخَّص"] = tuple(sorted(set(f["كون"])))
    b = dabit_bill(f, "كلُّ شيءٍ مرخَّص")
    T.append(("مقامٌ يُرخِّص كلَّ شيءٍ اشترى بتّات", b is not None and b["Δ"] < 0))

    # ⑥ ضابطٌ مختلقٌ («لن يليها جارّة») يصمد.
    g = dict(fields["لن"])
    g["مرخَّص"] = ("م", "ع", "ف")
    gb = dabit_bill(g, "لن>جارّة")
    T.append(("ضابطٌ مختلقٌ صمد",
              gb is not None and rule_verdict(gb, gb["مواضعُ_الإطلاق"]) == "صامد"))

    # ⑦ الصدقُ الخاوي: ضابطٌ بموضعٍ واحدٍ يُحكَم عليه بـ«صامد».
    T.append(("ضابطٌ بموضعٍ واحدٍ حُكم له بالصمود",
              rule_verdict(dict(نسبةُ_المخالفة=0.0, حكمُ_الفاتورة=verdict(-1.0)), 1) == "صامد"))

    # ⑧ ω = 0 يحذف الحافةَ لا العقدة.
    T.append(("ω=0 أسقط البابَ وثمَّ حافةٌ موجبة",
              not omega_drop([("أ", 0), ("ب", 5)])["موصولة"]))
    T.append(("انقطاعُ الحافّات كلِّها لم يُسقِط البابَ",
              omega_drop([("أ", 0)])["موصولة"]))

    # ⑨ وسمُ الناسخ يُتَّخذ سندًا رغم تخالف المرايا.
    T.append(("وسمُ الناسخ اتُّخذ سندًا",
              markup_divergence({"أ": 10, "ب": 0})["يُتَّخذُ_سندًا"]))

    # ⑩ المكيالُ يسعّر تيّارًا فارغًا.
    try:
        price([], 0)
        empty_ok = True
    except ValueError:
        empty_ok = False
    T.append(("المكيالُ سعّر تيّارًا فارغًا", empty_ok))

    # ⑪ الاستثناءُ مجّانيٌّ: مخالفاتٌ كثيرةٌ لا تُكلِّف شيئًا.
    free = _log2_choose(1000, 50)
    T.append(("خمسون استثناءً من ألفٍ بثمنِ صفر", free <= 0))

    return [dict(محاولة=n, نجحت=bool(b), حكم="نُقضت ✗" if b else "رُدّت ✓") for n, b in T]


# ═══ ⑨ التشغيل ══════════════════════════════════════════════════════════════════════
def run():
    toks = corpus_tokens()
    forms = [t["صورة"] for t in toks]
    idx_by_n = {n: ngram_index(forms, n) for n in range(BRIDGE_MIN, BRIDGE_MAX + 1)}

    # ① المراسي مصادَمةً قبل كلِّ شيء — ولا يُقاس على مرساةٍ لم تصمد.
    blob, digest = witness_bytes(ANCHOR_WITNESS)
    anchors = {k: sanad_anchor(k, blob) for k in ANCHORS}

    # ② الجسرُ على الشهود الثلاثة، والتخالفُ يُودَع لا يُوسَّط.
    bridges, spans_by_w, markup = {}, {}, {}
    for w in WITNESSES:
        b, spans = tasrih_bridge(w, idx_by_n)
        bridges[w] = b
        spans_by_w[w] = spans
        raw, _ = witness_bytes(w)
        markup[w] = raw.count(MARKUP[0].encode())

    cited = set()
    for spans in spans_by_w.values():
        for a, b in spans:
            cited.update(range(a, b))

    # ③ ما خرج عن حدِّنا — من الشاهد المُرسى، معدودًا لا مُهمَلًا.
    words = witness_words(blob)
    out = outside_share(words, idx_by_n[COVERAGE_N])

    # ④ الضوابطُ: فاتورةٌ ثمّ حكمٌ ثمّ عطوب.
    fields = dabit_fields(toks)
    rows, edges = [], []
    for d in DABITS:
        key = d["مفتاح"]
        f = fields[key]
        bill = dabit_bill(f, d["قالب"])
        edges.append((key, len(f["إطلاق"])))
        if bill is None:
            rows.append(dict(ضابط=key, حكم="غيرُ مختبَر", علّة="لا موضعَ إطلاقٍ في الحدّ",
                             مواضعُ_الإطلاق=0, فاتورة=None, مرساة=anchors[key], عطوب={}))
            continue
        defects = {
            "انتقاءُ شواهدَ داخل D": ban_cherry_pick(f, f["كون"], cited, toks),
            "ذوبانُ ضابط": ban_dissolution(f),
            "علّةٌ بلا وزن": ban_unweighed_illa(f, d["قالب"]),
            "شاذٌّ أُقصي لراحة القاعدة": ban_comfort_exclusion(bill),
        }
        trig = set(f["إطلاق"])
        rows.append(dict(
            ضابط=key, نصُّهم=anchors[key]["نصّ"], مقامُنا=d["مقام"],
            ترجمةٌ_يدوية=d["ترجمةٌ_يدوية"], حدُّ_الترجمة=d["حدُّ_الترجمة"],
            قالب=d["قالب"], مرساة=anchors[key],
            مواضعُ_الإطلاق=len(f["إطلاق"]), فاتورة=bill,
            إحاطة=dict(مواضعُ_حدِّنا=len(f["إطلاق"]),
                       ما_وقع_في_مادّته=len(trig & cited),
                       نسبةُ_الإحاطة=round(len(trig & cited) / max(1, len(f["إطلاق"])), 4),
                       حدّ=("الوقوعُ في المادّة المُرساة لا الاستشهادُ للضابط: هذا حدٌّ "
                            "أعلى لإحاطته، لا قياسُ قصدِه — ويُعلَن كذلك")),
            عطوب=defects,
            حكم=rule_verdict(bill, len(f["إطلاق"]))))

    by_key = {r["ضابط"]: r for r in rows}
    omega = omega_drop(edges)
    limit_ban = ban_our_limit([r for r in rows if r["فاتورة"]], out["نصيبُ_الخارج"])

    tested = [r for r in rows if r["حكم"] != "غيرُ مختبَر"]
    stood = [r for r in tested if r["حكم"] == "صامد"]
    tally = Counter()
    for r in rows:
        for name, dd in r.get("عطوب", {}).items():
            if dd.get("عطب"):
                tally[name] += 1
    if limit_ban["عطب"]:
        tally["حدُّنا لا حدُّهم"] += 1

    tries = falsify(blob, fields, toks, idx_by_n)

    # ــ المصادمةُ بفارق صفر: الأحكامُ المجمَّدةُ تُشتقُّ من مواضعها وتُقابَل ــ
    derived = dict(
        مواضعُ_تصريحٍ_في_المُرسى=bridges[ANCHOR_WITNESS]["مواضعُ_التصريح"],
        مطابقٌ_في_المُرسى=bridges[ANCHOR_WITNESS]["مطابق"],
        وسمٌ_في_المُرسى=markup[ANCHOR_WITNESS],
        وسمٌ_في_الشاملة=markup["ibnhisham_mughni_sham"],
        وسمٌ_في_الشيعة=markup["ibnhisham_mughni_shia"],
        كلماتُ_المُرسى=out["كلماتُه"],
        واقعٌ_في_حدِّنا=out["واقعٌ_في_حدِّنا"],
        إطلاقُ_لن=len(fields["لن"]["إطلاق"]),
        إطلاقُ_لم=len(fields["لم"]["إطلاق"]),
        إطلاقُ_أل=len(fields["التنوين وأل"]["إطلاق"]),
        إطلاقُ_الجارّة=len(fields["الباء جارّة"]["إطلاق"]),
        ذوبانُ_لم=by_key["لم"]["عطوب"]["ذوبانُ ضابط"]["فرقُ_الذوبان"],
        ذوبانُ_الجارّة=by_key["الباء جارّة"]["عطوب"]["ذوبانُ ضابط"]["فرقُ_الذوبان"],
        صامد=len(stood), مختبَر=len(tested),
    )
    assert not [t for t in tries if t["نجحت"]], \
        f"محاولةُ تكذيبٍ نجحت: {[t['محاولة'] for t in tries if t['نجحت']]}"
    assert omega["موصولة"], "انقطعت حافّاتُ الباب كلُّها"
    assert not limit_ban["عطب"], "رقمُ ما خرج عن الحدّ دخل الحكمَ — وهو ممنوع"
    assert limit_ban["ذو_أثر"], "حارسُ الحدّ خاوٍ: حقنُ الرقم لم يغيِّر حكمًا فلا يحرس شيئًا"
    for k, v in SEALED_MANHAJ.items():
        assert derived[k] == v, f"ختمٌ خُولف: {k} = {derived[k]} والمجمَّدُ {v}"

    return dict(
        التسجيلُ_المسبق=dict(
            مسبارٌ_مُعلَن=("سُبق البابُ بمسبارٍ على بايتات الشهود الثلاثة قِيست به أربعةُ "
                          "مقادير قبل التجميد: خلوُّ الشاهدَين من العناوين · خواءُ عناوين "
                          "الثالث · ندرةُ لفظ «الشاهد» · وتخالفُ المرايا في وسم الاقتباس. "
                          "مُصرَّحٌ به لا مكتوم"),
            شهود=list(WITNESSES), شاهدُ_المراسي=ANCHOR_WITNESS,
            صيغُ_التصريح=list(TASRIH_FORMS),
            ضوابطُ_معلنة=[dict(مفتاح=d["مفتاح"], قالب=d["قالب"], مقام=d["مقام"],
                               ترجمةٌ_يدوية=d["ترجمةٌ_يدوية"]) for d in DABITS],
            أصنافُ_العطب=[dict(صنف=a, حدّ=b, منع=c) for a, b, c in DEFECTS],
            فواصل=THRESHOLDS),
        مراسٍ=anchors,
        جسرُ_التصريح=dict(
            شهود=bridges,
            تخالفُ_الوسم=markup_divergence(markup),
            حدّ=("الجسرُ على صيغة التصريح وحدَها — وهي في الشهود كلِّهم. ووسمُ الناسخ "
                 "يُقاس ويُودَع تخالفُه ولا يُتَّخذ سندًا")),
        ما_خرج_عن_حدِّنا=dict(out, حدّ=(
            "هذا الرقمُ **لا يدخل حكمًا**: مادّةٌ استشهد بها خارجَ المجمَّد صوابٌ قد يكون "
            "صوابًا، والحكمُ عليه بحدِّنا هو الظلمُ الأوّلُ الذي فُتح هذا البابُ لمنعه. "
            "ومنعُه منفَّذٌ في ban_our_limit: الحكمُ يُحسَب مرّتين ويجب أن يتطابق")),
        دفترُ_الضوابط=rows,
        دفترُ_العطوب=dict(توزيع=dict(tally), منعُ_الحدّ=limit_ban,
                          أصناف=[a for a, _, _ in DEFECTS]),
        ω=omega,
        الأرقامُ_الثلاثة=dict(
            ما_صمد_من_ترجمتنا=dict(صامد=len(stood), مختبَر=len(tested), جملة=len(rows),
                                    نسبة=round(len(stood) / max(1, len(tested)), 4)),
            توزيعُ_أصنافِ_العطب=dict(tally),
            حجمُ_ما_خرج_عن_الحدّ=out["نصيبُ_الخارج"]),
        محاولاتُ_التكذيب=tries,
        ختمُ_المصادمة=derived,
    )


def show(R):
    o = R["ما_خرج_عن_حدِّنا"]
    print("— الرقمُ الأوّلُ في الصدر: حجمُ ما خرج عن حدِّنا —")
    print(f"  كلماتُ الشاهد {o['كلماتُه']:,} · واقعٌ في المجمَّد بحرفه {o['واقعٌ_في_حدِّنا']:,}"
          f" · **نصيبُ الخارج {o['نصيبُ_الخارج']:.2%}** (شبكةُ {o['شبكة']})")

    print("\n— المراسي: إزاحةٌ مجمَّدةٌ وبصمةٌ تُشتقّ —")
    for k, a in R["مراسٍ"].items():
        print(f"  {k:14s} @{a['إزاحة']:>9,} +{a['طول']:<3} {a['بصمة'][:16]}… «{a['نصّ'][:46]}»")

    print("\n— جسرُ التصريح على ثلاثة شهود —")
    for w, b in R["جسرُ_التصريح"]["شهود"].items():
        print(f"  {w:24s} مواضع {b['مواضعُ_التصريح']:>4,} · مطابق {b['مطابق']:>4,}"
              f" ({b['نسبةُ_المطابقة']:.2%}) · فشلٌ مسمًّى {sum(b['فشلٌ_مسمًّى'].values()):>3}")
    m = R["جسرُ_التصريح"]["تخالفُ_الوسم"]
    print(f"  وسمُ الاقتباس: {m['عدد']} ⟵ {m['حكم']}")

    print("\n— دفترُ الضوابط: نصُّهم مُرسًى · مقامُنا مُعلَن · الترجمةُ يدوية —")
    for r in R["دفترُ_الضوابط"]:
        b = r["فاتورة"]
        if not b:
            print(f"  [{r['ضابط']}] {r['حكم']} — {r.get('علّة','')}")
            continue
        print(f"  [{r['ضابط']:14s}] إطلاق {b['مواضعُ_الإطلاق']:>6,} · مخالفات {b['مخالفات']:>3}"
              f" ({b['نسبةُ_المخالفة']:.4%}) · Δ {b['Δ']:+,.1f} ب · {r['حكم']}"
              f" · إحاطةٌ عليا {r['إحاطة']['نسبةُ_الإحاطة']:.2%}")
        if b["صورُ_المخالفة"]:
            forms = " · ".join(f"{w} ×{c}" for w, c in b["صورُ_المخالفة"])
            print(f"        صورُ المخالفة (لم تُطرَح، وثمنُها مدفوع): {forms}")
        d = r["عطوب"]["ذوبانُ ضابط"]
        if d["عطب"]:
            print(f"        ذوبانٌ بالصورة: مخالفاتُ الصورة {d['بالصورة']['مخالفات']} ⟷ "
                  f"بالعلامة {d['بالعلامة']['مخالفات']} — والعلامةُ هي التي أنقذت الضابط")

    print("\n— دفترُ العطوب —")
    t = R["دفترُ_العطوب"]["توزيع"]
    for name in R["دفترُ_العطوب"]["أصناف"]:
        print(f"  {name:26s} {t.get(name,0)}")

    a = R["الأرقامُ_الثلاثة"]["ما_صمد_من_ترجمتنا"]
    print(f"\n— ما صمد من ترجمتنا لضابطهم: {a['صامد']}/{a['مختبَر']} ({a['نسبة']:.2%}) "
          f"من جملة {a['جملة']} —")
    ok = sum(1 for x in R["محاولاتُ_التكذيب"] if not x["نجحت"])
    print(f"— محاولاتُ التكذيب: {ok}/{len(R['محاولاتُ_التكذيب'])} رُدّت ✓")


def main():
    ap = argparse.ArgumentParser(description="بابُ المنهج — مراجعةُ كيفيّةِ بنائهم")
    ap.add_argument("--json", metavar="PATH", help="يودِع الحمولةَ جسونًا")
    a = ap.parse_args()
    try:
        R = run()
    except ManhajError as exc:
        print(f"::error::{exc.message}", file=sys.stderr)
        return exc.code
    show(R)
    if a.json:
        json.dump({"المنهج_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"\nJSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
