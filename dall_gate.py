# dall_gate.py — بابُ الدالّ: الحقلُ 112 وانتقالاتُه، وأيُّ ترخيصٍ يشترطُ مدلولًا.
#
# ــ ٠) الدعوى المقيسة ههنا ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# الدعوى: **جزءُ الدالِّ يدلُّ على معناه** — فكلُّ انتقالٍ في بنية الدالِّ وحدَه
# مشروطٌ بالارتباطِ بمدلول، وكلُّ ترخيصٍ مرخَّصٌ بقالبٍ من الميزان.
# وهذه دعوى **قابلةٌ للتكذيب** متى عُيِّن المقياسُ قبل العدّ. والمقياسُ ههنا
# مُعلَنٌ بتمامه قبل أن يُقرَأ بايتٌ واحد:
#
#   • **المقام**: الحقلُ 112 من `field112_laws` بعينه — لا نسخةَ ثانيةً منه.
#     الوحدةُ (حرفٌ من BASE28 × حركةٌ من HARAKAT4)، والانتقالُ زوجُ خليّتين
#     متجاورتين **داخلَ الكلمة الواحدة**. وما خرج عن 112 (العريُ والمنشأُ
#     المولَّد) ليس طرفًا في انتقال — وهذا حدٌّ من `field112_laws` لا منّا.
#
#   • **الفاتورة**: فاتورةُ `field112_laws` نفسِها — `harakat_layer.heldout_ce`
#     بالبتّ، وهي التي يحتكم إليها `governor_bridge` هناك. **ولا عدّادَ جديد**:
#     المكسبُ فرقُ إنتروبيا متقاطعةٍ محجوزةِ العيّنة، مضروبًا في عدد الانتقالات.
#
#   • **الطائفتان تُعلَنان قبل العدّ من مصادرَ مختومةٍ قائمة**:
#       (أ) **ذواتُ المدلول** = زوائدُ «سألتمونيها» العشر (`projection_specs.md`)
#           ∪ أدواتُ `madlul_gate.MU3JAM` التي هي حرفٌ واحد. وأسماءُ الأدوات
#           تُردُّ إلى حروفها بـ`madlul_gate.HIJA_NAMES` **بالترتيب** — اشتقاقٌ
#           من مصدرٍ مختوم، لا جدولَ يدٍ.
#       (ب) **وما سواها** = بقيّةُ BASE28.
#
#   • **الحَكَم**: ضوابطُ المثل — كما استقرّ في `madlul_gate`. فالحكمُ المفردُ
#     (مكسبٌ موجبٌ ⟹ قامت الدعوى) **خاوٍ** ههنا كما ثبت هناك: كلُّ طائفةٍ من
#     الحروف تكسِب بتّاتٍ لأنّ المجاورةَ في اللغة مقيَّدةٌ على كلِّ حال. فلا
#     تُفصَل طائفةٌ إلا إن **غلبت أدنى إحدى عشرةَ فرقةً عشوائيّةً بعددها**
#     (بذرةُ `ta3allum_gate.CONTROL_SEED`).
#
# ــ ١) المحطّاتُ الأربع ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
#   ① **الحقلُ وانتقالاتُه** — عددُ الانتقالات، والخلايا المشغولة، والمكسبُ
#      بالخليّة السابقة. عدٌّ مشتقٌّ لا رقمَ يدٍ.
#   ② **الطائفتان** — أتكسِبُ طائفةُ ذواتِ المدلولِ فوقَ ما سواها؟ وأتغلِبُ
#      ضوابطَ المثل؟
#   ③ **الخلايا المرخَّصة** — `awzan_engine.PREFIX` ستُّ **خلايا** من الحقل
#      (و/ف بفتحة · ب/ل/ك بكسرة · ل بفتحة) يقلَعنَ في طبقة «و٣-قلع». فهذه
#      دعوى «جزءُ الدالِّ له مدلول» **مُودَعةٌ في المحرّك قائمةً**. ويُقاس:
#      أتُضيِّقُ الخليّةُ المرخَّصةُ ما بعدَها أم تُطلِقه؟
#   ④ **الترخيصُ بالقالب** — قوالبُ `algebra_engine.T` الخمسةَ عشرَ (I مجرَّدٌ
#      وما بعده مزيد)، ومصفوفةُ `COLS` الثماني (ماضٍ ومضارعٌ معلومًا ومجهولًا ·
#      أمرٌ · مصدرٌ · اسما الفاعل والمفعول) — أي المبنيُّ للمعلوم والمبنيُّ
#      للمجهول والأسماءُ والأفعالُ والمصادر. ويُقاس: أيكسِبُ القالبُ بتّاتٍ
#      **فوقَ الخليّةِ السابقة**، وأيغلِبُ قوالبَ مخلوطةً على الكلمات؟
#
# ــ ٢) الحدُّ المُعلَن: ما لا يقوله هذا الباب ــــــــــــــــــــــــــــــــــــــ
#   • لا يقيس أنّ لكلِّ حرفٍ مدلولًا ولا ينفيه — يقيس **دعوى محدَّدة**: أنّ
#     طائفةَ ذواتِ المدلولِ المعلَنةَ تَفصِل انتقالاتِ الحقل. وسقوطُها سقوطُ
#     هذه الصياغةِ بعينها، لا سقوطُ كلِّ صياغةٍ ممكنة.
#   • لا يُدَّعى تحليلٌ صرفيٌّ للكلمة: مطابقةُ القالبِ مطابقةُ `awzan_engine`
#     بطبقاتها المعلَنة وأخطائها المعدودة، وهي تصيب بعضَ المقام لا كلَّه.
#   • المكسبُ بالبتِّ **ليس** معنًى: هو ثمنُ وصفٍ. وكونُ القالبِ يَكسِب لا
#     يعني أنّ القالبَ مدلولٌ — يعني أنّ الانتقالَ مشروطٌ بشيءٍ سوى جارِه،
#     وأنّ ذلك الشيءَ هو الميزانُ لا الحرف.
from math import log2
import argparse
import collections
import itertools
import json
import math
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_INDUCTION = os.path.join(_HERE, "induction")
if _INDUCTION not in sys.path:
    sys.path.insert(0, _INDUCTION)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import awzan_engine as AE                 # PREFIX · hit · tokenize_rich
import dalalat_gate as DG                 # fold — تسويةُ البايتات بعينها
import field112_laws as F                 # الحقلُ 112 وحدودُه
import madlul_gate as MG                  # MU3JAM · HIJA_NAMES
import ta3allum_gate as TG                # CONTROL_SEED
from algebra_engine import COLS, LAZIM_MAHD, NAWADER, T, W10, paradigm_cell
from harakat_layer import heldout_ce

E_OK, E_USAGE, E_MISSING, E_SEAL = 0, 2, 3, 4


class DallError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code, self.message = code, message


# ═══ ① المقامُ والحدود — تُقرأ من field112_laws لا تُكتَب ثانيةً ═════════════════
BASE28 = tuple(F.BASE28)
HARAKAT4 = tuple(F.HARAKAT4)
M112 = len(BASE28) * len(HARAKAT4)
assert M112 == 112, "الحقلُ ليس 112 — صريخ"

# ② حدُّ العيّنة: خليّةٌ صدرٌ دونَ مئتَي كلمةٍ لا تُحكَم، تُسمّى وتُعلَّق.
MIN_N = 200

# ③ ضوابطُ المثل: إحدى عشرةَ فرقةً — العددُ نفسُه في `madlul_gate`.
RIVALS = 11

# ④ زوائدُ «سألتمونيها» — من `projection_specs.md` المختوم، تُنتزَع من بايتاته.
ZAWAID_KEY = "سألتمونيها"
SPECS = os.path.join(_HERE, "projection_specs.md")

# ⑤ المصنوعُ للتكذيب: طائفةٌ باسمٍ لا وجودَ له في الحقل.
FABRICATED_BAND = "قزمط"

# ⑥ حدُّ بحثِ الرتبةِ البوليانيّة: رتبةً وعرضًا — ليُعطيَ حدًّا أعلى في زمنٍ مقطوع.
RANK_CAP, RANK_WIDTH = 3, 40


def zawaid_letters():
    """الزوائدُ العشرُ مقروءةً من بايتات `projection_specs.md` — لا جدولَ يدٍ."""
    if not os.path.isfile(SPECS):
        raise DallError(E_MISSING, f"وثيقةُ الإسقاط غائبة: {SPECS}")
    blob = open(SPECS, "rb").read().decode("utf-8")
    if ZAWAID_KEY not in blob:
        raise DallError(E_MISSING, f"«{ZAWAID_KEY}» غائبةٌ عن {SPECS} — صريخ")
    letters = {c for c in DG.fold(ZAWAID_KEY) if c in BASE28}
    if len(letters) != 9:
        raise DallError(E_SEAL,
                        f"حروفُ «{ZAWAID_KEY}» المطويّةُ المميّزة {len(letters)} ≠ 9")
    return letters


def adat_letters():
    """أدواتُ `madlul_gate.MU3JAM` التي هي حرفٌ واحد.

    والأداةُ في المتن تُسمّى باسمها («الباءُ» لا «ب»)، فتُردُّ إلى حرفها
    بـ`HIJA_NAMES` **بترتيبها** المصادَمِ بالأبجدية — اشتقاقٌ لا جدول.
    """
    order = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
    if len(order) != 28 or len(MG.HIJA_NAMES) != 28:
        raise DallError(E_SEAL, "ترتيبُ أسماء الهجاء خُولف — صريخ")
    name2letter = {DG.fold(n): order[i] for i, n in enumerate(MG.HIJA_NAMES)}
    out = set()
    for band in MG.MU3JAM:
        for group in band["فرق"]:
            for token, _ in group["أدوات"]:
                folded = DG.fold(token)
                for word in folded.split():
                    if word in name2letter:
                        out.add(name2letter[word])
                        break
                else:
                    if len(folded) == 1 and folded in BASE28:
                        out.add(folded)
    return out


# ═══ ② بناءُ الانتقالات ══════════════════════════════════════════════════════════
def cells_of(unit):
    """خلايا الحقلِ في وحدةٍ واحدة — وما خرج عن 112 يسقط بحدِّ field112_laws."""
    return [(ch, st) for ch, st, _ in unit if ch in BASE28 and st in HARAKAT4]


def key(cell):
    return f"{cell[0]}|{cell[1]}"


def transitions():
    """كلُّ انتقالٍ (حرف،حركة) ⟶ (حرف،حركة) داخلَ الكلمة، مشتقًّا من decompose."""
    verses = F.read_words(F.CORPUS)
    v112, _, _ = F.decompose(verses)
    pairs, words = [], []
    for row in v112:
        for unit in row:
            cs = cells_of(unit)
            words.append(cs)
            pairs.extend(zip(cs, cs[1:]))
    return pairs, words


def bill(rows):
    """فاتورةُ field112_laws بعينها: إنتروبيا متقاطعةٌ محجوزةُ العيّنة بالبتّ."""
    free = heldout_ce(rows, None, M112)
    given = heldout_ce(rows, 0, M112)
    return free, given, free - given


def band_bill(pairs, letters):
    """فاتورةُ طائفةٍ: انتقالاتٌ صدرُها حرفٌ من الطائفة، مسعَّرةً بالخليّة السابقة."""
    rows = [(key(a), key(b)) for a, b in pairs if a[0] in letters]
    if len(rows) < MIN_N:
        return None
    free, given, gain = bill(rows)
    return dict(عدّةُ_الحروف=len(letters), انتقالات=len(rows),
                بلا_شرط=round(free, 4), بالخليّة_السابقة=round(given, 4),
                مكسبٌ_بالبتّ=round(gain, 4),
                مكسبٌ_كلّيّ=round(gain * len(rows), 1))


def field_station(pairs, words):
    """① الحقلُ وانتقالاتُه — عدٌّ مشتقٌّ وفاتورةٌ واحدة."""
    rows = [(key(a), key(b)) for a, b in pairs]
    free, given, gain = bill(rows)
    heads = {key(c[0]) for c in words if c}
    targets = {key(b) for _, b in pairs}
    return dict(
        كلماتٌ_في_المقام=len(words),
        انتقالاتٌ_داخلَ_الكلمة=len(rows),
        خلايا_الحقل=M112,
        خلايا_هدفٍ_مشغولة=len(targets),
        خلايا_صدرٍ_مشغولة=len(heads),
        بلا_شرط=round(free, 4),
        بالخليّة_السابقة=round(given, 4),
        مكسبٌ_بالبتّ=round(gain, 4),
        مكسبٌ_كلّيّ=round(gain * len(rows), 1))


# ═══ ③ محطّةُ الطائفتين ═════════════════════════════════════════════════════════
def bands_station(pairs):
    """② أتفصِلُ طائفةُ ذواتِ المدلولِ الانتقالاتِ؟ وضوابطُ المثل هي الحَكَم."""
    zaw, adat = zawaid_letters(), adat_letters()
    madlul = (zaw | adat) & set(BASE28)
    other = set(BASE28) - madlul
    a = band_bill(pairs, madlul)
    b = band_bill(pairs, other)
    if a is None or b is None:
        raise DallError(E_SEAL, "طائفةٌ دونَ حدِّ العيّنة — لا حكمَ عليها")

    rng = random.Random(TG.CONTROL_SEED)
    base = sorted(BASE28)
    rivals = []
    for i in range(RIVALS):
        band = set(rng.sample(base, len(madlul)))
        r = band_bill(pairs, band)
        if r is None:
            raise DallError(E_SEAL, f"ضابطُ مثلٍ {i + 1} دونَ حدِّ العيّنة")
        r["رقم"] = i + 1
        rivals.append(r)

    worst = min(r["بالخليّة_السابقة"] for r in rivals)
    beaten = sum(1 for r in rivals if a["بالخليّة_السابقة"] < r["بالخليّة_السابقة"])
    return dict(
        ذواتُ_المدلول=dict(
            حروف=sorted(madlul), من_سألتمونيها=sorted(zaw),
            أدواتٌ_حرفيّةٌ_من_المعجم=sorted(adat), **a),
        ما_سواها=dict(حروف=sorted(other), **b),
        ضوابطُ_المثل=rivals,
        غلبت_ما_سواها=bool(a["مكسبٌ_بالبتّ"] > b["مكسبٌ_بالبتّ"]),
        غلبت_ضوابطَ_المثل=bool(a["بالخليّة_السابقة"] < worst),
        ضوابطُ_غُلِبت=beaten,
        حكم=("فصَلت" if a["بالخليّة_السابقة"] < worst else "سقطت"),
        بيان=("الطائفةُ تُحكَم بأضيقِ انتروبيا مشروطة: كلَّما ضاقت فالانتقالُ "
              "أشدُّ اشتراطًا. والحكمُ لا يُعطى بمكسبٍ موجبٍ مفردًا — فذاك خاوٍ "
              "كما ثبت في `madlul_gate` — بل بغلبةِ أضيقِ ضوابطِ المثل."))


# ═══ ④ محطّةُ الخلايا المرخَّصة ═════════════════════════════════════════════════
def prefix_station(pairs, words):
    """③ خلايا `awzan_engine.PREFIX`: أتُضيِّقُ ما بعدَها أم تُطلِقه؟

    والقياسُ وجهان لا وجهٌ واحد: انتروبيا التالي بعدَ الخليّة، ونصيبُ البقيةِ
    أن تكونَ هيكلًا واقعًا في المقام حرًّا (أي: أهي لاصقةٌ تُقلَع؟).
    """
    after = collections.defaultdict(collections.Counter)
    for a, b in pairs:
        after[a][key(b)] += 1

    skel = lambda cs: "".join(ch for ch, _ in cs)
    vocab = {skel(w) for w in words if w}
    head = collections.Counter()
    free = collections.Counter()
    for w in words:
        if len(w) < 3:
            continue
        head[w[0]] += 1
        if skel(w[1:]) in vocab:
            free[w[0]] += 1

    def ent(counter):
        n = sum(counter.values())
        return -sum(v / n * log2(v / n) for v in counter.values())

    rows = []
    for cell, n in head.items():
        if n < MIN_N or not after[cell]:
            continue
        rows.append(dict(خليّة=key(cell), مرخَّصة=cell in AE.PREFIX, صدرًا=n,
                         انتروبيا_التالي=round(ent(after[cell]), 4),
                         خلايا_تالية=len(after[cell]),
                         بقيّةٌ_هيكلٌ_حرّ=round(free[cell] / n, 4)))
    rows.sort(key=lambda r: (-r["انتروبيا_التالي"], r["خليّة"]))

    lic = [r for r in rows if r["مرخَّصة"]]
    oth = [r for r in rows if not r["مرخَّصة"]]
    if not lic or not oth:
        raise DallError(E_SEAL, "طائفةُ الخلايا المرخَّصةِ أو أختُها خاوية")
    lo = min(r["بقيّةٌ_هيكلٌ_حرّ"] for r in lic)
    return dict(
        خلايا_PREFIX=sorted(key(c) for c in AE.PREFIX),
        خلايا_مقيسة=len(rows),
        مرخَّصةٌ_مقيسة=len(lic),
        سواها_مقيسة=len(oth),
        متوسطُ_انتروبيا_المرخَّصة=round(sum(r["انتروبيا_التالي"] for r in lic) / len(lic), 4),
        متوسطُ_انتروبيا_سواها=round(sum(r["انتروبيا_التالي"] for r in oth) / len(oth), 4),
        المرخَّصةُ_تُضيِّق=bool(sum(r["انتروبيا_التالي"] for r in lic) / len(lic)
                          < sum(r["انتروبيا_التالي"] for r in oth) / len(oth)),
        أدنى_بقيّةٍ_حرّةٍ_في_المرخَّصة=lo,
        سواها_فوقَ_أدنى_المرخَّصة=sum(1 for r in oth if r["بقيّةٌ_هيكلٌ_حرّ"] >= lo),
        صفوف=rows,
        بيان=("الخليّةُ المرخَّصةُ لاصقةٌ تُقلَع، واللاصقُ يَلحَق بالمفتوح — "
              "فانتروبيا تاليها **أوسعُ** لا أضيق. وهذا يُسقِط قراءةَ «جزءُ "
              "الدالِّ يُضيِّق ما بعدَه»، ولا يُسقِط كونَه لاصقًا: الترخيصُ في "
              "الخليّة نفسِها لا في تقييدِ جارها. ونصيبُ البقيّةِ هيكلًا حرًّا "
              "لا يفصِل أيضًا — القلعُ العَرَضيُّ يبلغُه ويزيد."))


# ═══ ⑤ محطّةُ الترخيصِ بالقالب ═══════════════════════════════════════════════════
def stirling2(n, k):
    """سترلنج من النوعِ الثاني S(n,k) — عددُ قسمةِ n عنصرًا إلى k كتلةٍ غيرِ خالية."""
    if k < 1 or k > n:
        return 0
    row = [1] + [0] * k
    for i in range(1, n + 1):
        row = [0] + [j * row[j] + row[j - 1] for j in range(1, k + 1)]
    return row[k]


def _blocks(vectors):
    """كتلُ المتّجهاتِ المتطابقة — القسمةُ الأخشنُ الصادقةُ لا قسمةً مُدَّعاة."""
    out = {}
    for i, v in enumerate(vectors):
        out.setdefault(tuple(v), []).append(i)
    return list(out.values())


def _transpose(g):
    return [[g[i][j] for i in range(len(g))] for j in range(len(g[0]))]


def _maximal_rects(g):
    """المستطيلاتُ القصوى: لكلِّ مجموعةِ أعمدةٍ صفوفُها التي تحويها كلَّها."""
    n, m = len(g), len(g[0])
    rects = set()
    for mask in range(1, 1 << m):
        cols = tuple(j for j in range(m) if mask >> j & 1)
        rows = tuple(i for i in range(n) if all(g[i][j] for j in cols))
        if rows:
            rects.add((rows, cols))
    return sorted(rects, key=lambda r: (-len(r[0]) * len(r[1]), r))


def bool_rank(g, cap=RANK_CAP, width=RANK_WIDTH):
    """أصغرُ عددِ مستطيلاتٍ يغطّي المأذونَ ولا يمسُّ ممنوعًا — بحثٌ صاعدٌ محدود.

    محدودٌ بـ`cap` رتبةً و`width` مستطيلًا، فهو **حدٌّ أعلى** للرتبةِ لا قطعٌ
    بها. ولا يُستعمَل حَكَمًا: ثمنُه يُصادَم مع سواه والأدنى هو الحكم.
    """
    ones = {(i, j) for i, r in enumerate(g) for j, x in enumerate(r) if x}
    rects = _maximal_rects(g)[:width]
    for r in range(1, cap + 1):
        for combo in itertools.combinations(rects, r):
            cover = set()
            for rows, cols in combo:
                cover |= {(i, j) for i in rows for j in cols}
            if cover == ones:
                return r, combo
    return None, None


def grid_codes(g):
    """ستّةُ رموزٍ تصفُ الشبكةَ كاملةً — والأدنى ثمنًا هو الحكم، لا اليدُ.

    الرموزُ كلُّها **مكتمِلة**: يستردُّ كلٌّ منها الخلايا كلَّها بلا فقد. وثمنُ
    كلِّ رمزٍ ثمنُ اختيارِ بنيتِه (سترلنج أو التوافيق) زائدَ حمولتِه بالبتّ.
    """
    n, m = len(g), len(g[0])
    N, z = n * m, sum(1 for r in g for x in r if not x)
    rb, cb = _blocks(g), _blocks(_transpose(g))
    kr, kc = len(rb), len(cb)
    codes = {
        "الخام": float(N),
        "بالتوافيق": log2(N + 1) + log2(math.comb(N, z)),
        "بالصفوف": log2(n) + log2(stirling2(n, kr)) + kr * m,
        "بالأعمدة": log2(m) + log2(stirling2(m, kc)) + kc * n,
    }
    # حاصلُ القسمتين لا يُدَّعى: يُصادَم بأنّ كلَّ مقصورةٍ ثابتةُ القيمة.
    product = all(len({g[i][j] for i in R for j in C}) == 1 for R in rb for C in cb)
    if product:
        codes["بحاصلِ القسمتين"] = (log2(n) + log2(stirling2(n, kr))
                                    + log2(m) + log2(stirling2(m, kc)) + kr * kc)
    rank, _ = bool_rank(g)
    if rank:
        codes["بالرتبةِ البوليانيّة"] = log2(min(n, m)) + rank * (n + m)
    return codes, kr, kc, rank


def _roundtrip(g):
    """مرّةً وعكسَ مرّة: تُرمَّز الشبكةُ بالقسمتين ثمّ تُفَكُّ وتُصادَم خليّةً خليّة."""
    n, m = len(g), len(g[0])
    rb, cb = _blocks(g), _blocks(_transpose(g))
    block = [[g[R[0]][C[0]] for C in cb] for R in rb]          # الترميز
    back = [[None] * m for _ in range(n)]                       # الفكّ
    for a, R in enumerate(rb):
        for b, C in enumerate(cb):
            for i in R:
                for j in C:
                    back[i][j] = block[a][b]
    return back == g, sum(1 for i in range(n) for j in range(m)
                          if back[i][j] != g[i][j])


def minimal_bound():
    """الحدُّ الأدنى المكتمِل لشبكةِ الميزان — مشتقًّا بالبتّات لا معدودًا باليد.

    الدعوى المقيسة: الشبكةُ ليست اثنتين وعشرين استثناءً حُرّةً؛ فإن كانت بنيةً
    فلا بدّ أن يصفَها رمزٌ **أرخصُ** من حدِّ التوافيق `log₂C(120,22)` الذي هو
    ثمنُ أيِّ شبكةٍ بعدّةِ الممنوعِ نفسِها بلا بنية. والحَكَمُ ضوابطُ المثل.
    """
    g = [[1 if paradigm_cell(w, c) == "✓" else 0 for c in COLS] for w in T]
    codes, kr, kc, rank = grid_codes(g)
    floor = min(codes.values())
    null = codes["بالتوافيق"]
    complete, lost = _roundtrip(g)

    # تنقيحُ القسمةِ لا يُرخِص: الثمنُ صاعدٌ في kr وkc، فالأخشنُ الصادقُ هو الأدنى.
    n, m = len(T), len(COLS)
    finer = [round(log2(n) + log2(stirling2(n, a)) + log2(m)
                   + log2(stirling2(m, b)) + a * b, 4)
             for a, b in ((kr + 1, kc), (kr, kc + 1), (kr + 1, kc + 1))]

    rng = random.Random(TG.CONTROL_SEED)
    ones = sum(sum(r) for r in g)
    rivals = []
    for _ in range(RIVALS):
        flat = [1] * ones + [0] * (n * m - ones)
        rng.shuffle(flat)
        rg = [flat[i * m:(i + 1) * m] for i in range(n)]
        rc, ra, rb_, rr = grid_codes(rg)
        rivals.append(dict(أنماطُ_صفوف=ra, أنماطُ_أعمدة=rb_,
                           رتبةٌ_بوليانيّة=rr, أدنى=round(min(rc.values()), 4),
                           أرخصُ_رمزٍ=min(rc, key=rc.get)))
    worst = min(r["أدنى"] for r in rivals)

    rank_rects = bool_rank(g)[1] or ()
    return dict(
        أنماطُ_الصفوف=kr, أنماطُ_الأعمدة=kc, رتبةٌ_بوليانيّة=rank,
        الأثمان={k: round(v, 4) for k, v in sorted(codes.items(),
                                                   key=lambda x: x[1])},
        الحدُّ_الأدنى=round(floor, 4), أرخصُ_رمزٍ=min(codes, key=codes.get),
        حدُّ_التوافيق=round(null, 4), وفرٌ_عن_التوافيق=round(null - floor, 4),
        الرحلةُ_مكتملة=complete, خلايا_ضاعت=lost,
        أثمانُ_التنقيح=finer, التنقيحُ_يُرخِص=any(f < floor for f in finer),
        مستطيلاتُ_الرتبة=[{"قوالب": [list(T)[i] for i in rows],
                          "أعمدة": [COLS[j] for j in cols]}
                         for rows, cols in rank_rects],
        ضوابطُ_المثل=rivals, أدنى_مثلٍ=worst,
        غلبَ_ضوابطَ_المثل=sum(1 for r in rivals if floor < r["أدنى"]),
        بيان=("الشبكةُ لا تُعَدُّ بل تُسعَّر. حدُّ التوافيق "
              f"`log₂C(120,22)` = {null:.4f} بتًّا هو ثمنُ أيِّ شبكةٍ بعدّةِ "
              "الممنوعِ نفسِها بلا بنية — وهو ما بلغَته ضوابطُ المثل كلُّها "
              "بلا استثناء. والمودَعةُ تنزلُ إلى "
              f"{floor:.4f} لأنّ صفوفَها {kr} أنماطٍ لا خمسةَ عشرَ، وأعمدتَها "
              f"{kc} أنماطٍ لا ثمانيةً، وهي حاصلُ ضربِ القسمتين تمامًا. "
              f"ورتبتُها البوليانيّةُ {rank}: مستطيلان يغطّيان المأذونَ كلَّه، "
              "أي **استثناءان** — المصدرُ عن المجرَّد، والمجهولُ عن اللازم — "
              "لا اثنان وعشرون. وثمنُ التنقيحِ صاعدٌ في kr وkc، فالقسمةُ "
              "الأخشنُ الصادقةُ هي الأدنى بالبناء لا بالاختيار. والرحلةُ "
              "مكتملة: يُفَكُّ الترميزُ فيطابقُ الشبكةَ خليّةً خليّة."))


def mizan_grid():
    """شبكةُ الميزان مقروءةً من `algebra_engine` — 15 قالبًا × 8 أعمدة، لا نسخة."""
    cells = [(w, c, paradigm_cell(w, c)) for w in T for c in COLS]
    return dict(
        الحدُّ_الأدنى_المكتمل=minimal_bound(),
        قوالب=len(T), مجرَّد=1, مزيد=len(T) - 1,
        عشرةُ_الأوزان=len(W10), نوادر=len(NAWADER),
        أعمدة=len(COLS), خلايا=len(cells),
        مأذونة=sum(1 for _, _, v in cells if v == "✓"),
        امتناعُ_لزوم=sum(1 for _, _, v in cells if v == "⚑ل"),
        سماعيّ=sum(1 for _, _, v in cells if v == "⚑س"),
        لازمٌ_محض=len(LAZIM_MAHD),
        ثمنُ_إعلانِ_الشبكة=round(TG.declaration_cost(sorted(T.values())), 4),
        بيان=("الأعمدةُ الثمانيةُ هي المبنيُّ للمعلوم والمبنيُّ للمجهول ماضيًا "
              "ومضارعًا، والأمرُ، والمصدرُ، واسما الفاعل والمفعول — أي الأفعالُ "
              "والمصادرُ والأسماءُ في شبكةٍ واحدة. والقالبُ I مجرَّدٌ وما بعده "
              "مزيد. **وهذه الأعدادُ عدٌّ لا برهان**: الحكمُ عليها في "
              "«الحدُّ_الأدنى_المكتمل» بالبتّات."))


def matched_words():
    """كلماتُ المقامِ التي طابقَها قالبٌ في طبقةِ «و٣-قلع» — مرّةً واحدة."""
    rich = AE.tokenize_rich()
    total, out = 0, []
    for verse in rich:
        for word in verse:
            total += 1
            h = AE.hit(word, "و٣-قلع")
            if h:
                cs = cells_of(word)
                if len(cs) > 1:
                    out.append((h[0], cs))
    return total, out


def qalab_rows(matched, labels=None):
    """صفوفُ الفاتورة: (الخليّةُ السابقةُ · القالبُ والموضع) ⟶ الخليّةُ التالية."""
    prev, both = [], []
    labels = labels if labels is not None else [q for q, _ in matched]
    for (_, cs), lab in zip(matched, labels):
        for i in range(1, len(cs)):
            p, t = key(cs[i - 1]), key(cs[i])
            prev.append((p, t))
            both.append((f"{p}·{lab}@{i}", t))
    return prev, both


def qalab_station(total, matched):
    """④ أيَكسِبُ القالبُ بتّاتٍ فوقَ الخليّةِ السابقة، وأيغلِبُ قوالبَ مخلوطة؟"""
    prev, both = qalab_rows(matched)
    if len(prev) < MIN_N:
        raise DallError(E_SEAL, "مطابقاتُ القوالبِ دونَ حدِّ العيّنة")
    free = heldout_ce(prev, None, M112)
    given = heldout_ce(prev, 0, M112)
    joint = heldout_ce(both, 0, M112)
    only = heldout_ce([(f"{q}@{i}", key(cs[i]))
                       for q, cs in matched for i in range(1, len(cs))], 0, M112)
    gain = given - joint

    labels = [q for q, _ in matched]
    rng = random.Random(TG.CONTROL_SEED)
    rivals = []
    for i in range(RIVALS):
        shuffled = labels[:]
        rng.shuffle(shuffled)
        _, rb = qalab_rows(matched, shuffled)
        rivals.append(dict(رقم=i + 1,
                           مكسبٌ_فوقَ_السابقة=round(given - heldout_ce(rb, 0, M112), 4)))
    best = max(r["مكسبٌ_فوقَ_السابقة"] for r in rivals)

    used = collections.Counter(q for q, _ in matched)
    return dict(
        كلماتُ_المقام=total,
        كلماتٌ_طابقَها_قالب=len(matched),
        نصيبُ_المطابقة=round(len(matched) / total, 4),
        قوالبُ_وقعت=len(used),
        أكثرُها_وقوعًا=[[w, used[w]] for w in sorted(used, key=lambda x: (-used[x], x))],
        انتقالاتٌ_في_المطابَق=len(prev),
        بلا_شرط=round(free, 4),
        بالخليّة_السابقة=round(given, 4),
        بالقالبِ_والموضعِ_وحدَه=round(only, 4),
        بهما_معًا=round(joint, 4),
        مكسبُ_القالبِ_فوقَ_السابقة=round(gain, 4),
        مكسبٌ_كلّيّ=round(gain * len(prev), 1),
        ضوابطُ_المثل=rivals,
        أعلى_مثلٍ=round(best, 4),
        غلبَ_ضوابطَ_المثل=bool(gain > best),
        حكم=("مُودَعٌ بالفاتورة" if gain > best else "ساقطٌ بالفاتورة"),
        بيان=("المثلُ ههنا قوالبُ مخلوطةٌ على الكلمات: العدّةُ نفسُها والتوزيعُ "
              "نفسُه والموضعُ نفسُه، ولا يتغيّر إلا ارتباطُ القالبِ بكلمته. "
              "فإن كسِبَ المودَعُ وخسِر المخلوطُ فالمكسبُ من الميزانِ نفسِه "
              "لا من عدّةِ المعالم."))


# ═══ ⑥ محاولاتُ التكذيب ═════════════════════════════════════════════════════════
def falsify(pairs, words, matched, field, bands, prefix, qalab, grid):
    trials = []

    def T_(name, ok, note=""):
        trials.append(dict(محاولة=name, نجحت=bool(ok), بيان=note))

    # ① طائفةٌ مصنوعةٌ باسمٍ لا حرفَ له في الحقل ⟹ لا بدّ أن تسقط قبل الحكم.
    fab = {c for c in DG.fold(FABRICATED_BAND) if c in BASE28}
    T_("طائفةٌ مصنوعةٌ تُحكَم بلا عيّنة",
       fab and band_bill([p for p in pairs if False], fab) is not None,
       f"«{FABRICATED_BAND}» ⟶ {sorted(fab)} على مقامٍ خاوٍ")

    # ② الطائفةُ كلُّها (28 حرفًا) تغلِب ضوابطَ المثل ⟹ المقياسُ تحصيلُ حاصل.
    whole = band_bill(pairs, set(BASE28))
    T_("الطائفةُ الجامعةُ تغلِب أضيقَ مثلٍ",
       whole["بالخليّة_السابقة"] < min(r["بالخليّة_السابقة"]
                                      for r in bands["ضوابطُ_المثل"]),
       f"الجامعة {whole['بالخليّة_السابقة']}")

    # ③ الفاتورةُ تُكافئ الشرطَ العشوائيَّ ⟹ الفاتورةُ خاوية.
    rng = random.Random(TG.CONTROL_SEED)
    noise = [(str(rng.randrange(M112)), key(b)) for _, b in pairs[:20000]]
    _, ng, gn = bill(noise)
    T_("شرطٌ عشوائيٌّ يكسِب بتّاتٍ موجبة", gn > 0, f"مكسبُ الضوضاء {gn:.4f}")

    # ④ خلطُ الأهدافِ يُبقي المكسب ⟹ المكسبُ من العدّة لا من البنية.
    tgt = [key(b) for _, b in pairs]
    rng.shuffle(tgt)
    _, _, sg = bill(list(zip([key(a) for a, _ in pairs], tgt)))
    T_("خلطُ الأهدافِ يُبقي مكسبًا معتدًّا به", sg > 0.05, f"بعدَ الخلط {sg:.4f}")

    # ⑤ قوالبُ مخلوطةٌ تغلِب المودَعة ⟹ الترخيصُ بالقالبِ وهم.
    T_("قالبٌ مخلوطٌ يغلِب المودَع",
       qalab["أعلى_مثلٍ"] >= qalab["مكسبُ_القالبِ_فوقَ_السابقة"],
       f"أعلى مثلٍ {qalab['أعلى_مثلٍ']} ⟷ المودَع "
       f"{qalab['مكسبُ_القالبِ_فوقَ_السابقة']}")

    # ⑥ قالبٌ واحدٌ لجميع الكلماتِ يكسِب مثلَ المودَع ⟹ المكسبُ من الموضعِ وحدَه.
    _, one = qalab_rows(matched, ["I"] * len(matched))
    og = qalab["بالخليّة_السابقة"] - heldout_ce(one, 0, M112)
    T_("قالبٌ واحدٌ للجميع يبلُغ مكسبَ المودَع",
       og >= qalab["مكسبُ_القالبِ_فوقَ_السابقة"], f"قالبٌ واحدٌ {og:.4f}")

    # ⑦ خلايا الحقلِ المشغولةُ أكثرُ من 112 ⟹ الحدُّ خُولف.
    T_("خلايا الحقلِ تجاوزت 112",
       field["خلايا_هدفٍ_مشغولة"] > M112 or field["خلايا_صدرٍ_مشغولة"] > M112,
       f"هدفٌ {field['خلايا_هدفٍ_مشغولة']} · صدرٌ {field['خلايا_صدرٍ_مشغولة']}")

    # ⑧ انتقالٌ طرفُه خارجَ 112 ⟹ حدُّ field112_laws خُولف.
    bad = sum(1 for a, b in pairs
              if a[0] not in BASE28 or b[0] not in BASE28
              or a[1] not in HARAKAT4 or b[1] not in HARAKAT4)
    T_("انتقالٌ طرفُه خارجَ الحقل", bad > 0, f"مخالفاتٌ {bad}")

    # ⑨ الخلايا المرخَّصةُ تُضيِّق ما بعدَها ⟹ القراءةُ المضيِّقةُ قائمة.
    T_("الخليّةُ المرخَّصةُ تُضيِّق ما بعدَها", prefix["المرخَّصةُ_تُضيِّق"],
       f"{prefix['متوسطُ_انتروبيا_المرخَّصة']} ⟷ "
       f"{prefix['متوسطُ_انتروبيا_سواها']}")

    # ⑩ شبكةُ الميزانِ خلاياها ليست 120 ⟹ نسخةٌ ثانيةٌ تخلَّفت.
    T_("شبكةُ الميزانِ خُولفت", grid["خلايا"] != len(T) * len(COLS),
       f"{grid['خلايا']} ⟷ {len(T) * len(COLS)}")

    # ⑪ ذواتُ المدلولِ تغلِب كلَّ ضوابطِ المثل ⟹ الدعوى قامت بصياغتها.
    T_("ذواتُ المدلولِ غلبت كلَّ المثل", bands["غلبت_ضوابطَ_المثل"],
       f"ضوابطُ غُلِبت {bands['ضوابطُ_غُلِبت']}/{RIVALS}")

    # ⑫ كلمةٌ بخليّةٍ واحدةٍ تُولِّد انتقالًا ⟹ البناءُ خاطئ.
    T_("كلمةٌ بخليّةٍ واحدةٍ ولَّدت انتقالًا",
       any(len(w) < 2 and w for w in words) and
       len(pairs) != sum(max(0, len(w) - 1) for w in words),
       f"الانتقالاتُ {len(pairs)}")

    b = grid["الحدُّ_الأدنى_المكتمل"]

    # ⑬ شبكةٌ مخلوطةٌ بعدّةِ الممنوعِ نفسِها تبلُغ الحدَّ ⟹ البنيةُ وهمٌ والعدّةُ هي الحكم.
    T_("شبكةٌ مخلوطةٌ تبلُغ الحدَّ الأدنى",
       b["غلبَ_ضوابطَ_المثل"] < RIVALS,
       f"غلبَ {b['غلبَ_ضوابطَ_المثل']}/{RIVALS} · أدنى مثلٍ {b['أدنى_مثلٍ']} "
       f"⟷ المودَع {b['الحدُّ_الأدنى']}")

    # ⑭ تنقيحُ القسمةِ يُرخِص ⟹ الأخشنُ ليس أدنى، والدعوى بالمنعِ لا بالبناء.
    T_("تنقيحُ القسمةِ يُرخِّص الثمن", b["التنقيحُ_يُرخِص"],
       f"أثمانُ التنقيح {b['أثمانُ_التنقيح']} ⟷ {b['الحدُّ_الأدنى']}")

    # ⑮ الرحلةُ ناقصةٌ ⟹ الرمزُ ليس مكتمِلًا فلا يُقاس به حدٌّ أدنى.
    T_("رحلةُ الترميزِ ناقصة",
       (not b["الرحلةُ_مكتملة"]) or b["خلايا_ضاعت"] > 0,
       f"ضاعت {b['خلايا_ضاعت']} خليّة")

    # ⑯ حدُّ التوافيقِ لا يبلُغُه المثل ⟹ المقارنةُ بمقامٍ غيرِ مقامِه.
    T_("مثلٌ نزلَ دونَ حدِّ التوافيق",
       b["أدنى_مثلٍ"] < b["حدُّ_التوافيق"],
       f"أدنى مثلٍ {b['أدنى_مثلٍ']} ⟷ حدُّ التوافيق {b['حدُّ_التوافيق']}")
    return trials


# ═══ ⑦ الأختامُ والتشغيل ════════════════════════════════════════════════════════
SEALED_DALL = {
    "انتقالاتُ الحقل": 185312,
    "خلايا هدفٍ مشغولة": 108,
    "خلايا صدرٍ مشغولة": 107,
    "مكسبُ الخليّةِ السابقة": 1.4635,
    "حروفُ ذوات المدلول": 12,
    "أدواتٌ حرفيّةٌ من المعجم": 7,
    "ذواتُ المدلولِ غلبت سواها": 0,
    "ذواتُ المدلولِ غلبت المثل": 0,
    "ضوابطُ مثلٍ غُلِبت": 6,
    "خلايا مرخَّصةٌ مقيسة": 5,
    "المرخَّصةُ تُضيِّق": 0,
    "سواها فوقَ أدنى المرخَّصة": 22,
    "كلماتٌ طابقَها قالب": 6979,
    "قوالبُ وقعت": 12,
    "مكسبُ القالبِ فوقَ السابقة": 0.0325,
    "القالبُ غلبَ المثل": 1,
    "خلايا الميزان": 120,
    "خلايا مأذونة": 98,
    "خلايا ممنوعةٌ لزومًا": 21,
    "خلايا سماعيّة": 1,
    "أنماطُ صفوفِ الميزان": 3,
    "أنماطُ أعمدةِ الميزان": 3,
    "رتبةُ الميزانِ البوليانيّة": 2,
    "الحدُّ الأدنى المكتمِل": 47.0023,
    "حدُّ التوافيق": 85.9816,
    "وفرٌ عن التوافيق": 38.9793,
    "الميزانُ غلبَ المثل": 11,
    "رحلةُ الميزانِ مكتملة": 1,
    "محاولاتُ_تكذيب": 16,
}


def run():
    pairs, words = transitions()
    field = field_station(pairs, words)
    bands = bands_station(pairs)
    prefix = prefix_station(pairs, words)
    total, matched = matched_words()
    qalab = qalab_station(total, matched)
    grid = mizan_grid()
    trials = falsify(pairs, words, matched, field, bands, prefix, qalab, grid)

    measured = {
        "انتقالاتُ الحقل": field["انتقالاتٌ_داخلَ_الكلمة"],
        "خلايا هدفٍ مشغولة": field["خلايا_هدفٍ_مشغولة"],
        "خلايا صدرٍ مشغولة": field["خلايا_صدرٍ_مشغولة"],
        "مكسبُ الخليّةِ السابقة": field["مكسبٌ_بالبتّ"],
        "حروفُ ذوات المدلول": bands["ذواتُ_المدلول"]["عدّةُ_الحروف"],
        "أدواتٌ حرفيّةٌ من المعجم": len(bands["ذواتُ_المدلول"]["أدواتٌ_حرفيّةٌ_من_المعجم"]),
        "ذواتُ المدلولِ غلبت سواها": int(bands["غلبت_ما_سواها"]),
        "ذواتُ المدلولِ غلبت المثل": int(bands["غلبت_ضوابطَ_المثل"]),
        "ضوابطُ مثلٍ غُلِبت": bands["ضوابطُ_غُلِبت"],
        "خلايا مرخَّصةٌ مقيسة": prefix["مرخَّصةٌ_مقيسة"],
        "المرخَّصةُ تُضيِّق": int(prefix["المرخَّصةُ_تُضيِّق"]),
        "سواها فوقَ أدنى المرخَّصة": prefix["سواها_فوقَ_أدنى_المرخَّصة"],
        "كلماتٌ طابقَها قالب": qalab["كلماتٌ_طابقَها_قالب"],
        "قوالبُ وقعت": qalab["قوالبُ_وقعت"],
        "مكسبُ القالبِ فوقَ السابقة": qalab["مكسبُ_القالبِ_فوقَ_السابقة"],
        "القالبُ غلبَ المثل": int(qalab["غلبَ_ضوابطَ_المثل"]),
        "خلايا الميزان": grid["خلايا"],
        "خلايا مأذونة": grid["مأذونة"],
        "خلايا ممنوعةٌ لزومًا": grid["امتناعُ_لزوم"],
        "خلايا سماعيّة": grid["سماعيّ"],
        "أنماطُ صفوفِ الميزان": grid["الحدُّ_الأدنى_المكتمل"]["أنماطُ_الصفوف"],
        "أنماطُ أعمدةِ الميزان": grid["الحدُّ_الأدنى_المكتمل"]["أنماطُ_الأعمدة"],
        "رتبةُ الميزانِ البوليانيّة": grid["الحدُّ_الأدنى_المكتمل"]["رتبةٌ_بوليانيّة"],
        "الحدُّ الأدنى المكتمِل": grid["الحدُّ_الأدنى_المكتمل"]["الحدُّ_الأدنى"],
        "حدُّ التوافيق": grid["الحدُّ_الأدنى_المكتمل"]["حدُّ_التوافيق"],
        "وفرٌ عن التوافيق": grid["الحدُّ_الأدنى_المكتمل"]["وفرٌ_عن_التوافيق"],
        "الميزانُ غلبَ المثل": grid["الحدُّ_الأدنى_المكتمل"]["غلبَ_ضوابطَ_المثل"],
        "رحلةُ الميزانِ مكتملة": int(grid["الحدُّ_الأدنى_المكتمل"]["الرحلةُ_مكتملة"]),
        "محاولاتُ_تكذيب": len(trials),
    }
    for k, sealed in SEALED_DALL.items():
        if k not in measured:
            raise DallError(E_SEAL, f"«{k}» مختومٌ ولا مقيسَ له")
        if measured[k] != sealed:
            raise DallError(E_SEAL, f"«{k}» = {measured[k]} ≠ المختوم {sealed}")
    if any(t["نجحت"] for t in trials):
        names = [t["محاولة"] for t in trials if t["نجحت"]]
        raise DallError(E_SEAL, f"محاولةُ تكذيبٍ نجحت — البابُ ساقط: {names}")

    return {"الدالّ_v0": {
        "الحقلُ_وانتقالاتُه": field,
        "الطائفتان": bands,
        "الخلايا_المرخَّصة": prefix,
        "الترخيصُ_بالقالب": qalab,
        "شبكةُ_الميزان": grid,
        "محاولاتُ_التكذيب": trials,
        "الحدُّ_المُعلَن": (
            "المقامُ حقلُ 112 من `field112_laws` بعينه، والفاتورةُ فاتورتُه "
            "(`heldout_ce`) لا عدّادًا جديدًا، والحَكَمُ ضوابطُ المثل لا المكسبُ "
            "المفرد. **ثلاثُ نتائجَ لا تُخلَط**: (أ) طائفةُ ذواتِ المدلولِ "
            "المعلَنةُ — سألتمونيها وأدواتُ المعجمِ الحرفيّة — **لا تفصِل** "
            "انتقالاتِ الحقل؛ (ب) خلايا `PREFIX` المرخَّصةُ **تُطلِق** ما بعدَها "
            "ولا تُضيِّقه، فالترخيصُ في الخليّةِ نفسِها لا في تقييدِ جارها؛ "
            "(ج) **القالبُ يُرخِّص**: مكسبُه فوقَ الخليّةِ السابقة موجبٌ ويغلِب "
            "قوالبَ مخلوطةً بالعدّةِ نفسِها. فالدعوى «كلُّ انتقالٍ مرخَّصٌ» "
            "تقومُ بالميزانِ لا بالحرف. وما سقط ههنا سقوطُ **هذه الصياغةِ** "
            "بعينها لا سقوطُ كلِّ صياغةٍ ممكنة، وبقيّةُ الصياغاتِ **دَينٌ "
            "يُسمّى ولا يُسعَّر**. و(د) **شبكةُ الميزانِ لا تُعَدُّ بل تُسعَّر**: "
            "عدُّ `120 · 98 · 21 · 1` عدُّ جدولٍ لا برهانَ فيه، والبرهانُ ثمنُها "
            "بالبتّ — تنزلُ إلى الحدِّ الأدنى المكتمِل دونَ حدِّ التوافيق "
            "`log₂C(120,22)` الذي بلغَته ضوابطُ المثل كلُّها، ورتبتُها "
            "البوليانيّةُ اثنتان: استثناءان لا اثنان وعشرون."),
        "مقيس": measured,
    }}


def show(R):
    A = R["الدالّ_v0"]
    m = A["مقيس"]
    print("╔═══ بابُ الدالّ: الحقلُ 112 وانتقالاتُه · أيُّ ترخيصٍ يشترطُ مدلولًا ═══╗")

    f = A["الحقلُ_وانتقالاتُه"]
    print("\n  ① الحقلُ وانتقالاتُه — (حرف،حركة) ⟶ (حرف،حركة) داخلَ الكلمة")
    print(f"     كلماتٌ {f['كلماتٌ_في_المقام']:,} · انتقالاتٌ "
          f"{f['انتقالاتٌ_داخلَ_الكلمة']:,}")
    print(f"     خلايا الحقل {f['خلايا_الحقل']} · مشغولةٌ هدفًا "
          f"{f['خلايا_هدفٍ_مشغولة']} · صدرًا {f['خلايا_صدرٍ_مشغولة']}")
    print(f"     بلا شرط {f['بلا_شرط']} ⟶ بالخليّةِ السابقة "
          f"{f['بالخليّة_السابقة']} · مكسبٌ {f['مكسبٌ_بالبتّ']} بت "
          f"= {f['مكسبٌ_كلّيّ']:,} بت")

    b = A["الطائفتان"]
    md, ot = b["ذواتُ_المدلول"], b["ما_سواها"]
    print("\n  ② الطائفتان المعلنتان قبلَ العدّ")
    print(f"     ذواتُ المدلول ({md['عدّةُ_الحروف']}): {''.join(md['حروف'])}")
    print(f"       سألتمونيها {''.join(md['من_سألتمونيها'])} · أدواتُ المعجم "
          f"{''.join(md['أدواتٌ_حرفيّةٌ_من_المعجم'])}")
    print(f"       ن={md['انتقالات']:,} · مشروطٌ {md['بالخليّة_السابقة']} · "
          f"مكسبٌ {md['مكسبٌ_بالبتّ']}")
    print(f"     ما سواها ({ot['عدّةُ_الحروف']}): ن={ot['انتقالات']:,} · مشروطٌ "
          f"{ot['بالخليّة_السابقة']} · مكسبٌ {ot['مكسبٌ_بالبتّ']}")
    print(f"     ضوابطُ المثل {len(b['ضوابطُ_المثل'])} · أضيقُها "
          f"{min(r['بالخليّة_السابقة'] for r in b['ضوابطُ_المثل'])} · "
          f"غُلِب منها {b['ضوابطُ_غُلِبت']}")
    print(f"     ⟵ {b['حكم']}")

    p = A["الخلايا_المرخَّصة"]
    print("\n  ③ خلايا الترخيصِ في المحرّك — awzan_engine.PREFIX")
    print(f"     {' · '.join(p['خلايا_PREFIX'])}")
    print(f"     متوسطُ انتروبيا التالي: مرخَّصةٌ "
          f"{p['متوسطُ_انتروبيا_المرخَّصة']} ⟷ سواها "
          f"{p['متوسطُ_انتروبيا_سواها']}")
    print(f"     المرخَّصةُ تُضيِّق؟ {'نعم' if p['المرخَّصةُ_تُضيِّق'] else 'لا — تُطلِق'}"
          f" · سواها فوقَ أدنى المرخَّصة {p['سواها_فوقَ_أدنى_المرخَّصة']}")

    q = A["الترخيصُ_بالقالب"]
    print("\n  ④ الترخيصُ بالقالب — قوالبُ algebra_engine")
    print(f"     كلماتٌ طابقَها قالبٌ {q['كلماتٌ_طابقَها_قالب']:,}/"
          f"{q['كلماتُ_المقام']:,} ({q['نصيبُ_المطابقة']}) · قوالبُ وقعت "
          f"{q['قوالبُ_وقعت']}")
    print(f"     بالخليّةِ السابقة {q['بالخليّة_السابقة']} ⟶ بهما معًا "
          f"{q['بهما_معًا']}")
    print(f"     مكسبُ القالبِ فوقَ السابقة {q['مكسبُ_القالبِ_فوقَ_السابقة']} بت "
          f"= {q['مكسبٌ_كلّيّ']:,} بت · أعلى مثلٍ مخلوطٍ {q['أعلى_مثلٍ']}")
    print(f"     ⟵ {q['حكم']}")

    g = A["شبكةُ_الميزان"]
    print("\n  ⑤ شبكةُ الميزان — المجرَّدُ والمزيدُ × معلومٍ ومجهولٍ وأسماءَ ومصادر")
    print(f"     قوالبُ {g['قوالب']} (مجرَّدٌ {g['مجرَّد']} · مزيدٌ {g['مزيد']}) × "
          f"أعمدةٌ {g['أعمدة']} = خلايا {g['خلايا']}")
    print(f"     مأذونةٌ {g['مأذونة']} · ممنوعةٌ لزومًا {g['امتناعُ_لزوم']} · "
          f"سماعيّةٌ {g['سماعيّ']} · ثمنُ الإعلان {g['ثمنُ_إعلانِ_الشبكة']} بت")

    print(f"\n  ⑥ محاولاتُ التكذيب — {m['محاولاتُ_تكذيب']}، ولم تنجح واحدة:")
    for t in A["محاولاتُ_التكذيب"]:
        print(f"     ✗ {t['محاولة']} — {t['بيان']}")

    print("\n  ⑦ الحدُّ المُعلَن")
    print(f"     {A['الحدُّ_المُعلَن']}")
    print("\n  ⑧ المقيس")
    for k, v in m.items():
        print(f"     {k}: {v}")
    print("\n╚" + "═" * 70 + "╝")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="بابُ الدالّ: انتقالاتُ الحقل 112 وترخيصُها بالمدلولِ والقالب")
    ap.add_argument("--json", metavar="ملفّ", help="وديعةُ الباب إلى ملفّ")
    args = ap.parse_args(argv)
    try:
        R = run()
    except DallError as e:
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
