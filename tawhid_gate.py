# tawhid_gate.py — بابُ توحيدِ المقام: قسمةُ «الدالِّ وحدَه» وقسمةُ «المدلولِ وحدَه»
# على مقامٍ واحدٍ، بدالّةٍ واحدةٍ مُعلَنةِ الشروط.
#
# ــ ٠) المطلوبُ ههنا ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# قسمتان مقيستان في هذه الشجرة، وكلُّ واحدةٍ منهما قِيست في بابها على حِدَة:
#
#   • **الدالُّ وحدَه**  — ثلاثُ رتبٍ (المطابقةُ · التضمّنُ · الالتزام)، مقيسةٌ في
#     `aqsam_gate.burhan_station` بفاتورة `ta3allum_gate.rule_bill` على سلّمٍ
#     معلنٍ من ثلاثة أدراج.
#   • **المدلولُ وحدَه** — أصنافُ حروف المعاني الواقعةُ في الميدان، مقيسةٌ في
#     `madlul_gate.lexicon_station` بضوابط المثل.
#
# وكلتاهما تُودِع في وديعتها رقمًا اسمُه «مقام». **ومِن أنّ الرقمين متساويان لا
# يلزم أنّ المقامَ واحد**: قد يتساوى عددان على ميدانين مختلفين. فتوحيدُ المقام
# ليس مصادمةَ رقمين، بل **ردُّ القسمتين إلى المواضع نفسِها** موضعًا موضعًا، ثمّ
# إثباتُ أنّ كلَّ واحدةٍ منهما **حاصرةٌ مانعة** على تلك المواضع بعينها. وما لم
# يُفعَل ذلك فلا يُقال «مقامٌ واحد»، ولا يُصادَم رقمٌ برقم.
#
# وهذا ما تفعله الدالّةُ **`wahhid`** ههنا، ولا تفعل سواه.
#
# ــ ١) الدالّة: ما تشترطه وما تردّه ـــــــــــــــــــــــــــــــــــــــــــــــــ
# `wahhid(n, qismat)` تأخذ مقامًا واحدًا n وقسماتٍ شتّى، كلُّ قسمةٍ (اسمُها ·
# اسمُ متبقّيها · أقسامُها بمواضعها)، وتشترط **خمسةَ شروطٍ تُصرَخ عند خرقها ولا
# تُبتلَع**:
#
#   ⑴ **المقامُ موجب**: لا توحيدَ على فراغ.
#   ⑵ **كلُّ موضعٍ من المقام**: موضعٌ خارجَ `range(n)` يُسقِط الدعوى أصلًا، فليس
#      المقامُ واحدًا إن كان أحدُ الطرفين يشير إلى ما ليس فيه.
#   ⑶ **مانعة**: لا يقع موضعٌ في قسمين من قسمةٍ واحدة. وهذا **يُقاس ولا يُفترَض**:
#      قسمةُ الدالِّ مانعةٌ بصياغةِ إطلاقها، وتداخلُها يُعَدُّ في كلِّ تشغيلٍ ويُختَم
#      صفرًا؛ وقسمةُ المدلولِ **ليست مانعةً بالبناء** (صورةٌ واحدةٌ تقع في صنفين)،
#      فتُردُّ بفاصلٍ مُعلَنٍ هو ترتيبُ الأصناف في المتن، **والمتنازَعُ عليه يُعَدُّ
#      ويُسمّى** ولا يُطوى.
#   ⑷ **اسمُ المتبقّي لا يصادم اسمَ قسم**: وإلّا خُلط المسكوتُ عنه بالمنصوص.
#   ⑸ **حاصرة**: تُضَمُّ إليها خانةُ «ما لم يقع» بعددها، ثمّ يُصادَم مجموعُ الكتل
#      بالمقام — فإن خالفه صُرِخ. **فلا قسمةَ ههنا بلا خانةِ متبقٍّ معدودة.**
#
# وتردُّ: لكلِّ قسمةٍ صفوفَها الحاصرةَ المانعة، واسمَ كلِّ موضعٍ فيها.
#
# ــ ٢) وما بعد التوحيد: الاشتراك ـــــــــــــــــــــــــــــــــــــــــــــــــــ
# التوحيدُ **وحدَه لا يقول شيئًا** — إنّما يجعل السؤالَ قابلًا للطرح. فإذا صار
# للقسمتين مقامٌ واحدٌ أمكن أن يُقاس بينهما:
#
#   • `H` لكلِّ قسمةٍ بالبتِّ في الموضع — ثمنُ تسميةِ موضعٍ بقسمه.
#   • `I = H(أ) + H(ب) − H(أ،ب)` — الاطّرادُ المشترك: كم بتًّا يوفِّر علمُ قسمِ
#     الموضعِ في إحداهما من ثمنِ تسميته في الأخرى.
#   • **الخلايا المشغولة** من الجدول: نصُّ صاحب القسمة أنّ الحيثيتين لا تُخلَطان
#     «ولذلك أمكن أن يقع اللفظُ الواحدُ في قسمٍ من كلِّ قسمةٍ بلا تناقض» — وهذه
#     دعوى **قابلةٌ للعدّ** متى وُحِّد المقام: تُعَدُّ الخلايا التي وقع فيها لفظ.
#
# ــ ٣) الحَكَم: ضابطان لا واحد ــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# رقمُ `I` وحدَه **خاوٍ** — درسُ `mirror.py` و`madlul_gate`: كلُّ قسمتين على مقامٍ
# واحدٍ تُعطيان اطّرادًا موجبًا. فلا يُقرأ إلّا مغلوبًا به ضابطان معلنان قبل العدّ:
#
#   ① **خلطُ الأسماء**: تُخلَط أسماءُ قسمةِ المدلول على المواضع بأحجامِ كتلها
#      نفسِها (بذرةُ `ta3allum_gate.CONTROL_SEED`). وهذا ضابطٌ **ضعيف**: يكسر كلَّ
#      بناءٍ لفظيّ.
#   ② **فرقٌ مصنوعةٌ بالأحجام نفسِها**: تُبنى قسمةُ مدلولٍ **مختلقةٌ** من صورٍ
#      تُسحَب من فضاء `ta3allum_gate.hypothesis_space`، بعددِ صورِ كلِّ صنفٍ بعينه.
#      وهذا هو الضابطُ **القويّ**: يسأل «أكلُّ فرقةِ صورٍ بهذه الأحجام تُعطي هذا
#      الاطّراد، أم أصنافُ الحروف بعينها؟».
#
# ولا يُقبَل حكمٌ إلّا إن غلبَ الضابطين معًا، **وفي أدراج السلّم الثلاثة جميعًا**
# (السلّمُ مقروءٌ من `aqsam_gate.RUNGS` لا منسوخًا ههنا).
#
# ــ ٤) الحدُّ المُعلَن: ما لا يقوله هذا الباب ــــــــــــــــــــــــــــــــــــــ
#   • **لا يوحِّد الحيثيتين**، بل المقامَ وحدَه. وقسمةُ الدالِّ تُقرأ من الصورة
#     وحدَها، وقسمةُ المدلولِ من أصنافِ الحروف — ولا تُدمَجان في قسمةٍ ثالثة.
#   • **المُسقَطُ من قسمةِ المدلولِ أصنافُ حروف المعاني وحدَها**، لا خاناتُها
#     الخمس. فخانةُ «لفظًا مفردًا مهمَلًا» نصيبُها في المجمَّد **صفرٌ منصوص**
#     (`madlul_gate`)، وما بقي من الخانات **دَينٌ يُسمّى ولا يُسعَّر**.
#   • **اشتراكُ الصور بين المشروعين مقيسٌ لا مطويّ**: صورُ شواهدِ رتبِ الدالِّ
#     وصورُ أصنافِ المدلولِ تلتقيان في صورٍ معدودة، ويُعلَن عددُها في كلِّ درج.
#     **وكم من الاطّراد راجعٌ إليها — غيرُ مقيسٍ ههنا**، وهو دَينٌ بلا رقم.
#   • `I` بالبتِّ **ليس معنًى**: هو ثمنُ وصفٍ. وكونُه فوقَ الضابطين لا يعني أنّ
#     إحدى القسمتين تُفسِّر الأخرى — يعني أنّ تسميةَ الموضعِ في إحداهما تُنقِص
#     ثمنَ تسميته في الأخرى فوقَ ما تُنقِصه فرقةٌ مصنوعةٌ بالأحجام نفسِها.
#   • الإسقاطان كلاهما **بيدنا**، وهما أضعفُ حلقةٍ ههنا؛ ولذلك كُتب لكلِّ رتبةٍ
#     نصُّ إطلاقها (مقروءًا من `aqsam_gate.RANKS`) ولكلِّ صنفٍ صورُه (مقروءةً من
#     وديعة `madlul_gate`)، ولا صورةَ تُكتَب بيدٍ ههنا البتّة.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بايتاتٌ غائبة · 4 ختمٌ خالف وديعتَه.
#
# التشغيل:
#   python tawhid_gate.py                 تقريرٌ معدودٌ على stdout
#   python tawhid_gate.py --json <ملفّ>   الوديعةُ إلى ملفّ (مولِّدُ الأختام)
#
# ⚑ ولا يُمَسُّ معجمٌ ولا كلفةٌ سابقة: هذا بابُ مقامٍ على ودائعَ مختومة.
import argparse
import json
import math
import os
import random
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
_INDUCTION = os.path.join(ROOT, "induction")
if _INDUCTION not in sys.path:
    sys.path.insert(0, _INDUCTION)

import aqsam_gate as AQ                  # RUNGS · RANKS · fire_of_rank
import ta3allum_gate as TG               # المقامُ والفضاءُ والبذرةُ — من بابها لا منسوخةً

E_OK, E_USAGE, E_MISSING, E_SEAL = 0, 2, 3, 4


class TawhidError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, msg):
        super().__init__(msg)
        self.code, self.msg = code, msg


# ═══ الإعلاناتُ المجمَّدةُ قبل القياس ═══════════════════════════════════════════════
# ① الوديعتان: لا تُقرَأ صورةٌ ولا رتبةٌ من يدٍ ههنا، بل من وديعتَي البابين.
DALL_DEPOSIT = "aqsam_v0.json"
MADLUL_DEPOSIT = "madlul_v0.json"

# ② أسماءُ القسمتين وأسماءُ متبقّيهما — والمتبقّي **يُسمّى ويُعَدّ** ولا يُطوى.
Q_DALL = "الدالُّ وحدَه"
Q_MADLUL = "المدلولُ وحدَه"
RESIDUE = {Q_DALL: "ما لم تُطلِقه رتبة", Q_MADLUL: "ما لم يقع في صنف"}

# ③ ضوابطُ المثل: عددُها معلنٌ قبل العدّ، وبذرتُها بذرةُ الشجرة لا بذرةً جديدة.
RIVALS = 11

# ④ الفاصلُ عند تنازعِ الصورة: **ترتيبُ الأصناف في المتن** كما أودعه `madlul_gate`.
#    وهذا فاصلٌ بيدنا، ولذلك يُعَدُّ المتنازَعُ عليه ويُسمّى في الوديعة.
TIEBREAK = "الصنفُ الأسبقُ في ترتيب المتن كما أُودع في madlul_v0.json"

# ⑤ ديونٌ تُسمّى بلا رقم — ولا يُسعَّر ما لم يُقَس.
DEBTS = (
    "كم من الاطّرادِ المشترك راجعٌ إلى اشتراكِ الصورِ بين المشروعين — معدودٌ عددُها "
    "لا أثرُها",
    "خاناتُ «المدلولِ وحدَه» الخمسُ لم تُسقَط كلُّها على المقام — المُسقَطُ أصنافُ "
    "حروف المعاني وحدَها",
    "ردُّ الصورةِ المتنازَعِ عليها إلى أسبقِ أصنافها بيدنا، ولم يُقَس أثرُ فاصلٍ آخر",
    "توحيدُ المقامِ لا يُثبِت أنّ القسمتين تصدُقان على العربية — ذلك موقوفٌ على النقل",
)


# ═══ ② أدواتُ العدّ ════════════════════════════════════════════════════════════════
def r4(x):
    """تقريبٌ إلى أربعٍ، وتسويةُ −0.0 إلى 0.0 لئلّا تختلف بايتاتُ الوديعة."""
    v = round(float(x), 4)
    return 0.0 if v == 0.0 else v


def entropy(counts, n):
    """H بالبتِّ في الموضع — على كتلٍ معدودة، لا على توزيعٍ مُدَّعًى."""
    if n <= 0:
        raise TawhidError(E_SEAL, "لا إنتروبيا على مقامٍ غيرِ موجب")
    return -sum(v / n * math.log2(v / n) for v in counts.values() if v)


def deposit(name):
    """بايتاتُ وديعةٍ مختومة — غيابُها صريخٌ لا سكوت."""
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        raise TawhidError(E_MISSING, f"وديعةٌ غائبة: {name}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ═══ ③ الدالّةُ المطلوبة: توحيدُ المقام ════════════════════════════════════════════
def wahhid(n, qismat):
    """**توحيدُ المقام**: ردُّ قسماتٍ شتّى إلى مواضعِ مقامٍ واحدٍ حاصرةً مانعة.

    المدخل:
      n       — المقامُ الواحد (عددُ المواضع).
      qismat  — متتاليةٌ من (اسمُ القسمة · اسمُ المتبقّي · ((اسمُ القسم، مواضعُه)…)).

    المخرج: قاموسٌ فيه لكلِّ قسمةٍ صفوفُها الحاصرةُ المانعة وأسماءُ مواضعها.

    والشروطُ الخمسةُ تُصرَخ ولا تُبتلَع — فالدالّةُ **لا تصحِّح مدخلًا فاسدًا**:
    قسمةٌ غيرُ مانعةٍ أو لا تستغرق المقامَ تُسقِط النداءَ كلَّه، لأنّ قبولَها
    قبولُ دعوى «مقامٌ واحد» بلا برهانها.
    """
    if not isinstance(n, int) or n <= 0:
        raise TawhidError(E_SEAL, f"مقامٌ غيرُ موجب: {n!r} — لا توحيدَ على فراغ")
    if len(qismat) < 2:
        raise TawhidError(E_USAGE, "التوحيدُ بين قسمتين فصاعدًا — لا قسمةَ وحدَها")

    out = {}
    for name, residue, blocks in qismat:
        if residue in {b for b, _ in blocks}:
            raise TawhidError(
                E_SEAL, f"«{name}»: اسمُ المتبقّي يصادم اسمَ قسمٍ — خلطُ المسكوتِ بالمنصوص")
        labels = [residue] * n
        overlap = 0
        for part, sites in blocks:
            for i in sites:
                if not isinstance(i, int) or not 0 <= i < n:
                    raise TawhidError(
                        E_SEAL, f"«{name}»: موضعٌ خارجَ المقام {i!r} — فالمقامُ ليس واحدًا")
                if labels[i] != residue:
                    overlap += 1
                labels[i] = part
        if overlap:
            raise TawhidError(
                E_SEAL,
                f"«{name}»: قسمةٌ غيرُ مانعة — {overlap} موضعًا وقع في قسمين")
        counts = Counter(labels)
        total = sum(counts.values())
        if total != n:
            raise TawhidError(
                E_SEAL, f"«{name}»: الكتلُ {total} لا تستغرق المقامَ {n}")
        rows = [dict(قسم=part, مواضع=counts.get(part, 0),
                     نصيب=r4(counts.get(part, 0) / n), متبقٍّ=False)
                for part, _ in blocks]
        rows.append(dict(قسم=residue, مواضع=counts.get(residue, 0),
                         نصيب=r4(counts.get(residue, 0) / n), متبقٍّ=True))
        out[name] = dict(أقسام=len(blocks), صفوف=rows, أسماء=labels,
                         تداخل=overlap, حاصرة=True, مانعة=True,
                         H=r4(entropy(counts, n)))
    return dict(مقام=n, قسمات=list(out), جداول=out)


def ishtirak(n, labels_a, labels_b):
    """الاطّرادُ المشترك بين قسمتين **بعد** توحيد مقامهما — ولا يُقاس قبله."""
    if len(labels_a) != n or len(labels_b) != n:
        raise TawhidError(
            E_SEAL,
            f"مقامان لا يتّحدان: {len(labels_a)} ⟷ {len(labels_b)} ⟷ {n}")
    ca, cb = Counter(labels_a), Counter(labels_b)
    cj = Counter(zip(labels_a, labels_b))
    ha, hb, hj = entropy(ca, n), entropy(cb, n), entropy(cj, n)
    return dict(**{"H_أ": r4(ha), "H_ب": r4(hb), "H_معًا": r4(hj),
                   "I": r4(ha + hb - hj)},
                خلايا_مشغولة=len(cj), خلايا_ممكنة=len(ca) * len(cb),
                نسبةُ_الاطّراد=r4((ha + hb - hj) / min(ha, hb)) if min(ha, hb) else 0.0)


# ═══ ④ الإسقاطان: من الوديعتين لا من يدٍ ═══════════════════════════════════════════
def dall_blocks(stream, dall, k):
    """رتبُ «الدالِّ وحدَه» في درجٍ واحد — الصورُ من الوديعة والإطلاقُ من `aqsam_gate`."""
    blocks, forms = [], {}
    for r in dall["برهانُ_الدالِّ_وحدَه"]["رتب"]:
        if r.get("مصنوعة"):
            continue
        picks = [d["صورُ_الشواهد"] for d in r["أدراج"] if d["درج"] == k]
        if len(picks) != 1:
            raise TawhidError(E_SEAL, f"درجٌ {k} ليس فريدًا في رتبة {r['رتبة']}")
        forms[r["رتبة"]] = list(picks[0])
        blocks.append((r["رتبة"], AQ.fire_of_rank(r["رتبة"], stream, picks[0])))
    if len(blocks) != len(AQ.RANKS):
        raise TawhidError(E_SEAL, f"رتبُ الدالِّ {len(blocks)} ⟷ {len(AQ.RANKS)}")
    return blocks, forms


def madlul_bands(madlul):
    """أصنافُ «المدلولِ وحدَه» الواقعةُ في الميدان — بترتيب المتن كما أُودعت."""
    arena = madlul["معجمُ_حروف_المعاني"]["ميدان"]
    bands = [(b["صنف"], list(b["صور"])) for b in arena["أصناف"] if b.get("في_الميدان")]
    if not bands:
        raise TawhidError(E_SEAL, "لا صنفَ في ميدان المدلول — لا قسمةَ تُسقَط")
    return bands, arena


def madlul_map(bands):
    """ردُّ الصورةِ إلى صنفها بالفاصل المُعلَن — والمتنازَعُ عليه يُعَدُّ ويُسمّى."""
    owner, contested = {}, {}
    for band, forms in bands:
        for f in forms:
            if f in owner:
                contested.setdefault(f, [owner[f]]).append(band)
            else:
                owner[f] = band
    return owner, contested


def madlul_blocks(stream, bands):
    """كتلُ المدلولِ على المقام — كلُّ موضعٍ صورتُه في صنفٍ واحدٍ بعد الفاصل."""
    owner, contested = madlul_map(bands)
    sites = {band: set() for band, _ in bands}
    for i, s in enumerate(stream):
        band = owner.get(s)
        if band is not None:
            sites[band].add(i)
    return [(band, sites[band]) for band, _ in bands], owner, contested


def fabricated_blocks(stream, bands, candidates, rng):
    """قسمةُ مدلولٍ **مختلقة**: صورٌ مسحوبةٌ بأحجامِ الأصناف نفسِها — الضابطُ القويّ."""
    need = sum(len(f) for _, f in bands)
    pick = rng.sample(candidates, need)
    it, owner = iter(pick), {}
    for band, forms in bands:
        for _ in forms:
            owner.setdefault(next(it), band)
    sites = {band: set() for band, _ in bands}
    for i, s in enumerate(stream):
        band = owner.get(s)
        if band is not None:
            sites[band].add(i)
    return [(band, sites[band]) for band, _ in bands]


# ═══ ⑤ المحطّات ════════════════════════════════════════════════════════════════════
def maqam_station(stream, dall, madlul):
    """مصادمةُ مقامِ الوديعتين بالمقامِ الحيّ — **والمصادمةُ شرطٌ لا برهان**.

    تساوي الرقمين لا يُثبِت وحدةَ المقام؛ إنّما يُسقِط الدعوى إن اختلفا. والبرهانُ
    إنّما هو استغراقُ القسمتين للمواضع بأعيانها في `wahhid`.
    """
    n = len(stream)
    a = dall["برهانُ_الدالِّ_وحدَه"]["مقام"]
    b = madlul["معجمُ_حروف_المعاني"]["ميدان"]["مقام"]
    if not (a == b == n):
        raise TawhidError(
            E_SEAL, f"مقاماتٌ لا تتّحد: الدالُّ {a} ⟷ المدلولُ {b} ⟷ الحيُّ {n}")
    return dict(
        بيان=("تساوي الرقمين شرطٌ لا برهان — والبرهانُ استغراقُ القسمتين "
              "للمواضع بأعيانها"),
        المقامُ_الحيّ=n, مقامُ_وديعةِ_الدالّ=a, مقامُ_وديعةِ_المدلول=b,
        اتّحدت=True)


def rung_station(stream, dall, madlul, bands, candidates, k):
    """درجٌ واحدٌ من السلّم: التوحيدُ ثمّ الاشتراكُ ثمّ الضابطان."""
    d_blocks, d_forms = dall_blocks(stream, dall, k)
    m_blocks, owner, contested = madlul_blocks(stream, bands)
    n = len(stream)

    joined = wahhid(n, (
        (Q_DALL, RESIDUE[Q_DALL], d_blocks),
        (Q_MADLUL, RESIDUE[Q_MADLUL], m_blocks),
    ))
    la = joined["جداول"][Q_DALL]["أسماء"]
    lb = joined["جداول"][Q_MADLUL]["أسماء"]
    seen = ishtirak(n, la, lb)

    # ① الضابطُ الضعيف: خلطُ الأسماء بأحجام الكتل نفسِها.
    rng = random.Random(TG.CONTROL_SEED)
    shuffled = []
    for _ in range(RIVALS):
        sh = lb[:]
        rng.shuffle(sh)
        shuffled.append(ishtirak(n, la, sh)["I"])

    # ② الضابطُ القويّ: فرقٌ مصنوعةٌ بالأحجام نفسِها من فضاء الفرضيّات.
    rng2 = random.Random(TG.CONTROL_SEED)
    made = []
    for _ in range(RIVALS):
        blocks = fabricated_blocks(stream, bands, candidates, rng2)
        lab = wahhid(n, ((Q_DALL, RESIDUE[Q_DALL], d_blocks),
                         (Q_MADLUL, RESIDUE[Q_MADLUL], blocks)))
        made.append(ishtirak(n, la, lab["جداول"][Q_MADLUL]["أسماء"])["I"])

    beat_shuffle = seen["I"] > max(shuffled)
    beat_made = seen["I"] > max(made)
    shared = sorted(set(owner) & {f for fs in d_forms.values() for f in fs})
    return dict(
        درج=k,
        صفوفُ_الدالّ=joined["جداول"][Q_DALL]["صفوف"],
        صفوفُ_المدلول=joined["جداول"][Q_MADLUL]["صفوف"],
        تداخلُ_الدالّ=joined["جداول"][Q_DALL]["تداخل"],
        تداخلُ_المدلول=joined["جداول"][Q_MADLUL]["تداخل"],
        اشتراك=seen,
        صورٌ_مشتركةٌ_بين_المشروعين=shared,
        عددُ_المشترك=len(shared),
        ضابطُ_خلطِ_الأسماء=dict(عدد=RIVALS, أعلى=r4(max(shuffled)),
                                 وسيط=r4(sorted(shuffled)[RIVALS // 2])),
        ضابطُ_الفرقِ_المصنوعة=dict(عدد=RIVALS, أعلى=r4(max(made)),
                                    وسيط=r4(sorted(made)[RIVALS // 2])),
        غلبَ_خلطَ_الأسماء=bool(beat_shuffle),
        غلبَ_الفرقَ_المصنوعة=bool(beat_made),
        غلبَ_الضابطين=bool(beat_shuffle and beat_made),
        ليستا_قسمةً_واحدة=bool(seen["نسبةُ_الاطّراد"] < 1.0),
        حكم=("اطّرادٌ فوقَ الضابطين" if beat_shuffle and beat_made
             else "لم يغلب الضابطين — لا يُقرَأ اطّرادًا"),
    )


def ladder_station(stream, dall, madlul):
    """السلّمُ المعلن — مقروءًا من `aqsam_gate.RUNGS` لا منسوخًا، وحكمٌ لا يتقلّب."""
    bands, arena = madlul_bands(madlul)
    candidates, _ = TG.hypothesis_space(stream)
    rows = [rung_station(stream, dall, madlul, bands, candidates, k)
            for k in AQ.RUNGS]
    verdicts = {r["حكم"] for r in rows}
    _, contested = madlul_map(bands)
    return dict(
        سلّم=list(AQ.RUNGS),
        بذرةُ_الضابط=TG.CONTROL_SEED,
        ضوابطُ_المثل=RIVALS,
        فاصلُ_التنازع=TIEBREAK,
        أصنافٌ_في_الميدان=len(bands),
        صورٌ_متنازعٌ_عليها=sorted(contested),
        أدراج=rows,
        حكمٌ_مستقرٌّ_على_السلّم=len(verdicts) == 1,
        حكم=(rows[0]["حكم"] if len(verdicts) == 1 else "متقلّبٌ بالدرج"),
        بيانُ_الميدان=arena["بيان"] if "بيان" in arena else "",
    )


# ═══ ⑥ محاولاتُ التكذيب — تُشغَّل ولا تُقرَأ ════════════════════════════════════════
def falsify(stream, dall, madlul, lad):
    """كلُّ محاولةٍ تُرَدُّ بـ(اسمٍ · أنجحت). ونجاحُ واحدةٍ يُسقِط الباب."""
    T, n = [], len(stream)

    def add(name, fired, note=""):
        T.append(dict(محاولة=name, نجحت=bool(fired), بيان=note))

    def raises(fn):
        try:
            fn()
        except TawhidError:
            return False
        except Exception:                                   # noqa: BLE001
            return True
        return True

    one = [("أ", {0, 1}), ("ب", {2, 3})]
    two = [("ج", {4, 5}), ("د", {6, 7})]
    pair = ((Q_DALL, "متبقٍّ", one), (Q_MADLUL, "متبقٍّ٢", two))

    # ① مقامٌ غيرُ موجبٍ يمرّ.
    add("التوحيدُ يقبل مقامًا غيرَ موجب", raises(lambda: wahhid(0, pair)))

    # ② موضعٌ خارجَ المقام يمرّ — فالمقامُ ليس واحدًا وقد قيل إنّه واحد.
    add("التوحيدُ يقبل موضعًا خارجَ المقام",
        raises(lambda: wahhid(4, ((Q_DALL, "متبقٍّ", [("أ", {9})]),
                                  (Q_MADLUL, "متبقٍّ٢", two)))))

    # ③ قسمةٌ غيرُ مانعةٍ تمرّ.
    add("التوحيدُ يقبل قسمةً غيرَ مانعة",
        raises(lambda: wahhid(8, ((Q_DALL, "متبقٍّ", [("أ", {0, 1}), ("ب", {1, 2})]),
                                  (Q_MADLUL, "متبقٍّ٢", two)))))

    # ④ اسمُ المتبقّي يصادم اسمَ قسمٍ فيُخلَط المسكوتُ بالمنصوص.
    add("التوحيدُ يقبل متبقّيًا باسمِ قسم",
        raises(lambda: wahhid(8, ((Q_DALL, "أ", one), (Q_MADLUL, "متبقٍّ٢", two)))))

    # ⑤ قسمةٌ وحدَها تُوحَّد — والتوحيدُ بين اثنتين فصاعدًا.
    add("التوحيدُ يقبل قسمةً وحدَها",
        raises(lambda: wahhid(8, ((Q_DALL, "متبقٍّ", one),))))

    # ⑥ الاشتراكُ يُقاس على مقامين مختلفين.
    add("الاشتراكُ يُقاس على مقامين مختلفين",
        raises(lambda: ishtirak(4, ["أ"] * 4, ["ب"] * 3)))

    # ⑦ مرساةُ الهوية: I(أ;أ) لا يساوي H(أ) — فالمقياسُ نفسُه معطوب.
    lab = ["أ"] * 30 + ["ب"] * 50 + ["ج"] * 20
    ident = ishtirak(100, lab, lab)
    add("مرساةُ الهوية سقطت: I(أ;أ) ≠ H(أ)",
        ident["I"] != ident["H_أ"], f"I {ident['I']} ⟷ H {ident['H_أ']}")

    # ⑧ إعادةُ تسمية الأقسام تغيِّر الاطّراد.
    other = ["س" if x == "أ" else ("ص" if x == "ب" else "ع") for x in lab]
    flip = [x for x in reversed(lab)]
    add("إعادةُ التسمية تغيِّر الاطّراد",
        ishtirak(100, other, flip)["I"] != ishtirak(100, lab,
                                                    [x for x in reversed(lab)])["I"])

    # ⑨ التناظر: I(أ;ب) ≠ I(ب;أ).
    add("الاطّرادُ غيرُ متناظر",
        ishtirak(100, lab, flip)["I"] != ishtirak(100, flip, lab)["I"])

    # ⑩ الفرقُ المصنوعةُ بالأحجام نفسِها تبلغ المرصودَ — فالدالّةُ خاوية.
    hollow = [r for r in lad["أدراج"] if not r["غلبَ_الفرقَ_المصنوعة"]]
    add("فرقٌ مصنوعةٌ بالأحجام نفسِها بلغت المرصود",
        bool(hollow), f"أدراجٌ لم تغلب: {len(hollow)}")

    # ⑪ خلطُ الأسماء يبلغ المرصود.
    weak = [r for r in lad["أدراج"] if not r["غلبَ_خلطَ_الأسماء"]]
    add("خلطُ الأسماء بلغ المرصود", bool(weak), f"أدراجٌ لم تغلب: {len(weak)}")

    # ⑫ قسمةُ الدالِّ غيرُ مانعةٍ مقيسًا — والمنعُ يُعَدُّ ولا يُفترَض.
    add("تداخلُ قسمةِ الدالِّ ليس صفرًا",
        any(r["تداخلُ_الدالّ"] for r in lad["أدراج"]))

    # ⑬ إحدى القسمتين تحدِّد الأخرى — فهما قسمةٌ واحدةٌ بِاسمين.
    add("قسمةٌ تحدِّد الأخرى (نسبةُ الاطّراد ١)",
        any(not r["ليستا_قسمةً_واحدة"] for r in lad["أدراج"]))

    # ⑭ الحكمُ يتقلّب بالدرج.
    add("الحكمُ متقلّبٌ بأدراج السلّم", not lad["حكمٌ_مستقرٌّ_على_السلّم"])

    # ⑮ التوحيدُ غيرُ حتميّ: نداءان متماثلان يعطيان غيرَ ما أعطيا.
    b1, _ = dall_blocks(stream, dall, AQ.RUNGS[0])
    bands, _ = madlul_bands(madlul)
    m1, _, _ = madlul_blocks(stream, bands)
    q = ((Q_DALL, RESIDUE[Q_DALL], b1), (Q_MADLUL, RESIDUE[Q_MADLUL], m1))
    first = wahhid(n, q)["جداول"][Q_DALL]["صفوف"]
    second = wahhid(n, q)["جداول"][Q_DALL]["صفوف"]
    add("التوحيدُ غيرُ حتميّ", first != second)

    # ⑯ خانةُ المتبقّي غائبةٌ من صفوف قسمةٍ — فالحصرُ مُدَّعًى لا معدود.
    rows = lad["أدراج"][0]
    add("قسمةٌ بلا خانةِ متبقٍّ معدودة",
        not (any(x["متبقٍّ"] for x in rows["صفوفُ_الدالّ"])
             and any(x["متبقٍّ"] for x in rows["صفوفُ_المدلول"])))

    return T


# ═══ ⑦ الأختامُ المجمَّدة ═══════════════════════════════════════════════════════════
SEALED_TAWHID = {
    "المقامُ الواحد": 77801,
    "قسماتٌ وُحِّد مقامُها": 2,
    "أقسامُ الدالِّ وحدَه": 3,
    "أصنافُ المدلولِ في الميدان": 8,
    "خلايا ممكنة": 36,
    "صورٌ متنازعٌ عليها بين الأصناف": 9,
    "أدراجُ السلّم": 3,
    "تداخلٌ في القسمتين": 0,
    "أدراجٌ غلبت الضابطين": 3,
    "أدراجٌ ليستا قسمةً واحدة": 3,
    "حكمٌ مستقرٌّ على السلّم": 1,
    "I في الدرج الأوّل": 0.3701,
    "I في الدرج الثاني": 0.4247,
    "I في الدرج الثالث": 0.3642,
    "أعلى الفرقِ المصنوعةِ في الدرج الثاني": 0.2239,
    "أعلى خلطِ الأسماءِ في الدرج الثاني": 0.0004,
    "خلايا مشغولةٌ في الدرج الثاني": 26,
    "صورٌ مشتركةٌ في الدرج الثاني": 11,
    "ديونٌ بلا رقم": 4,
    "محاولاتُ_تكذيب": 16,
}


# ═══ ⑧ التشغيل ═════════════════════════════════════════════════════════════════════
def run():
    try:
        _, stream, _ = TG.corpus_surfaces()
    except TG.Ta3allumError as exc:
        raise TawhidError(exc.code, exc.message) from exc
    dall = deposit(DALL_DEPOSIT)["الأقسام_v0"]
    madlul = deposit(MADLUL_DEPOSIT)["المدلول_v0"]

    mq = maqam_station(stream, dall, madlul)
    lad = ladder_station(stream, dall, madlul)
    trials = falsify(stream, dall, madlul, lad)
    fired = [t["محاولة"] for t in trials if t["نجحت"]]
    if fired:
        raise TawhidError(E_SEAL, "محاولةُ تكذيبٍ نجحت: " + " · ".join(fired))

    mid = lad["أدراج"][1]
    measured = {
        "المقامُ الواحد": mq["المقامُ_الحيّ"],
        "قسماتٌ وُحِّد مقامُها": 2,
        "أقسامُ الدالِّ وحدَه": len(mid["صفوفُ_الدالّ"]) - 1,
        "أصنافُ المدلولِ في الميدان": len(mid["صفوفُ_المدلول"]) - 1,
        "خلايا ممكنة": mid["اشتراك"]["خلايا_ممكنة"],
        "صورٌ متنازعٌ عليها بين الأصناف": len(lad["صورٌ_متنازعٌ_عليها"]),
        "أدراجُ السلّم": len(lad["أدراج"]),
        "تداخلٌ في القسمتين": sum(r["تداخلُ_الدالّ"] + r["تداخلُ_المدلول"]
                                   for r in lad["أدراج"]),
        "أدراجٌ غلبت الضابطين": sum(1 for r in lad["أدراج"] if r["غلبَ_الضابطين"]),
        "أدراجٌ ليستا قسمةً واحدة": sum(1 for r in lad["أدراج"]
                                        if r["ليستا_قسمةً_واحدة"]),
        "حكمٌ مستقرٌّ على السلّم": int(lad["حكمٌ_مستقرٌّ_على_السلّم"]),
        "I في الدرج الأوّل": lad["أدراج"][0]["اشتراك"]["I"],
        "I في الدرج الثاني": mid["اشتراك"]["I"],
        "I في الدرج الثالث": lad["أدراج"][2]["اشتراك"]["I"],
        "أعلى الفرقِ المصنوعةِ في الدرج الثاني": mid["ضابطُ_الفرقِ_المصنوعة"]["أعلى"],
        "أعلى خلطِ الأسماءِ في الدرج الثاني": mid["ضابطُ_خلطِ_الأسماء"]["أعلى"],
        "خلايا مشغولةٌ في الدرج الثاني": mid["اشتراك"]["خلايا_مشغولة"],
        "صورٌ مشتركةٌ في الدرج الثاني": mid["عددُ_المشترك"],
        "ديونٌ بلا رقم": len(DEBTS),
        "محاولاتُ_تكذيب": len(trials),
    }
    out = {"توحيدُ_المقام_v0": dict(
        الدالّة=dict(
            اسم="wahhid",
            بيان=("ردُّ قسماتٍ شتّى إلى مواضعِ مقامٍ واحدٍ حاصرةً مانعة — "
                  "وشروطُها الخمسةُ تُصرَخ ولا تُصحَّح"),
            شروط=[
                "المقامُ موجب",
                "كلُّ موضعٍ من المقام",
                "مانعةٌ: لا موضعَ في قسمين",
                "اسمُ المتبقّي لا يصادم اسمَ قسم",
                "حاصرةٌ: خانةُ المتبقّي معدودةٌ ومجموعُ الكتلِ هو المقام",
            ],
            مصادر=dict(
                الدالّ=f"{DALL_DEPOSIT} · aqsam_gate.fire_of_rank · aqsam_gate.RANKS",
                المدلول=f"{MADLUL_DEPOSIT} · ميدانُ معجمِ حروف المعاني",
                السلّم="aqsam_gate.RUNGS — مقروءٌ لا منسوخ",
                المقام="ta3allum_gate.corpus_surfaces",
            ),
        ),
        المقام=mq,
        السلّم=lad,
        ديونٌ_بلا_رقم=dict(عدد=len(DEBTS), بنود=list(DEBTS)),
        الحدُّ_المُعلَن=(
            "يوحَّد المقامُ لا الحيثية. والمُسقَطُ من «المدلولِ وحدَه» أصنافُ حروف "
            "المعاني وحدَها لا خاناتُه الخمس. واشتراكُ الصورِ بين المشروعين معدودٌ "
            "عددُه لا أثرُه. وI بالبتِّ ثمنُ وصفٍ لا معنًى."),
        محاولاتُ_التكذيب=trials,
        مقيس=measured,
    )}
    return out, measured


def collide(measured):
    extra = [k for k in measured if k not in SEALED_TAWHID]
    if extra:
        raise TawhidError(E_SEAL, "قيمٌ مقيسةٌ بلا ختم: " + " · ".join(extra))
    bad = [(k, SEALED_TAWHID[k], measured.get(k)) for k in SEALED_TAWHID
           if k not in measured or measured[k] != SEALED_TAWHID[k]]
    if bad:
        raise TawhidError(E_SEAL, "أختامٌ خالفت: " + " · ".join(
            f"{k}: وديعة {a} ⟷ مقيس {b}" for k, a, b in bad))
    return len(SEALED_TAWHID)


def show(out):
    g = out["توحيدُ_المقام_v0"]
    mq, lad = g["المقام"], g["السلّم"]
    print("بابُ توحيدِ المقام — قسمتان على مقامٍ واحدٍ بدالّةٍ مُعلَنةِ الشروط")
    print("=" * 78)
    print(f"الدالّة: {g['الدالّة']['اسم']} — {g['الدالّة']['بيان']}")
    for mark, s in zip("⑴⑵⑶⑷⑸", g["الدالّة"]["شروط"]):
        print(f"   {mark} {s}")
    print()
    print(f"① المقام: الحيُّ {mq['المقامُ_الحيّ']:,} · وديعةُ الدالِّ "
          f"{mq['مقامُ_وديعةِ_الدالّ']:,} · وديعةُ المدلولِ "
          f"{mq['مقامُ_وديعةِ_المدلول']:,} ⟶ اتّحدت ✓")
    print(f"   {mq['بيان']}")
    print()
    mid = lad["أدراج"][1]
    print(f"② القسمتان حاصرتان مانعتان (الدرج {mid['درج']}):")
    for row in mid["صفوفُ_الدالّ"]:
        tag = " ⟵ متبقٍّ" if row["متبقٍّ"] else ""
        print(f"   الدالّ · {row['قسم']:22s} {row['مواضع']:7,} "
              f"({row['نصيب']}){tag}")
    for row in mid["صفوفُ_المدلول"]:
        tag = " ⟵ متبقٍّ" if row["متبقٍّ"] else ""
        print(f"   المدلول · {row['قسم']:22s} {row['مواضع']:7,} "
              f"({row['نصيب']}){tag}")
    print(f"   تداخلٌ: الدالّ {mid['تداخلُ_الدالّ']} · المدلول "
          f"{mid['تداخلُ_المدلول']} · صورٌ متنازعٌ عليها "
          f"{len(lad['صورٌ_متنازعٌ_عليها'])} ⟶ {lad['فاصلُ_التنازع']}")
    print()
    print("③ السلّمُ والاشتراك — والحَكَمُ ضابطان لا واحد:")
    for r in lad["أدراج"]:
        sh = r["اشتراك"]
        print(f"   درج {r['درج']:2d}: H(د) {sh['H_أ']} · H(م) {sh['H_ب']} · "
              f"I {sh['I']} · نسبةُ الاطّراد {sh['نسبةُ_الاطّراد']} · "
              f"خلايا {sh['خلايا_مشغولة']}/{sh['خلايا_ممكنة']}")
        print(f"          خلطُ الأسماء ≤ {r['ضابطُ_خلطِ_الأسماء']['أعلى']} "
              f"{'✓' if r['غلبَ_خلطَ_الأسماء'] else '✗'} · "
              f"فرقٌ مصنوعةٌ ≤ {r['ضابطُ_الفرقِ_المصنوعة']['أعلى']} "
              f"{'✓' if r['غلبَ_الفرقَ_المصنوعة'] else '✗'} · "
              f"مشتركٌ من الصور {r['عددُ_المشترك']} ⟶ {r['حكم']}")
    print(f"   حكمٌ مستقرٌّ على السلّم: {lad['حكمٌ_مستقرٌّ_على_السلّم']} ⟶ {lad['حكم']}")
    print()
    print(f"ديونٌ بلا رقم: {g['ديونٌ_بلا_رقم']['عدد']}")
    for x in g["ديونٌ_بلا_رقم"]["بنود"]:
        print(f"  · {x}")
    print(f"\nمحاولاتُ التكذيب: {len(g['محاولاتُ_التكذيب'])} — لم تنجح واحدة ✓")


def main(argv=None):
    ap = argparse.ArgumentParser(description="بابُ توحيدِ المقام")
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args(argv)
    try:
        out, measured = run()
        n = collide(measured)
    except TawhidError as e:
        print(f"صريخ: {e.msg}", file=sys.stderr)
        return e.code
    show(out)
    print(f"الأختام: {n} مصادَمًا بفارق صفر ✓")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"JSON ⟵ {args.json}")
    return E_OK


if __name__ == "__main__":
    sys.exit(main())
