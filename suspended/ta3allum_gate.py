# ta3allum_gate.py — محطّةُ التعلُّم: قواعدُ النبهانيِّ **يُعاد بناؤها**، والحَكَمُ الفاتورة.
#
# ــ ٠) العلّةُ التي تفتحها هذه المحطّة ــــــــــــــــــــــــــــــــــــــــــــــــــ
# في `dalalat_gate` القواعدُ **مأخوذةٌ من الكتاب** ثمّ يُحكَم عليها بسلّمٍ من عتبتين:
# `n₀ = 30` و`فاصلُ الذوبان = 0.05`. والعتبتان مُبرَّرتان، لكنّهما **مختارتان بيدٍ**:
# لو حُرِّكت إحداهما لتحرّك الحكم. فالبابُ يراجع دعوًى بمكيالٍ فيه شيءٌ من إرادتنا.
#
# وهذه المحطّةُ تقلب الترتيب: **لا تُؤخَذ القاعدةُ من التعريف، بل تُنتزَع من المقام
# المختوم؛ ولا يحكم عليها سلّمٌ، بل تحكم عليها فاتورةُ الوصف الأدنى وحدَها.** فتصير
# قواعدُ النبهانيِّ **فرضياتٍ في ميدانٍ مفتوح**: تدخله مع مئةٍ وثلاثين صورةً أخرى من
# المقام نفسِه، وتُسعَّر بالمكيال نفسِه، ويقال بالرقم: أيُّها اشترى بتًّا وأيُّها خسر.
#
# ــ ١) الحَكَمُ: فاتورةُ التقسيم المشروط — لا عتبةَ فيها ـــــــــــــــــــــــــــــــ
# قاعدةٌ تدّعي أنّ صورةً ما **تفتح بابًا**. وأدنى ما يلزم من ذلك في مقامنا: أن يكون
# الواقعُ بعدها مختلفًا عمّا سواه اختلافًا **يُشترى ببتّات**. فتُقاس هكذا:
#
#     L₀        = price(صورِ المجمَّد كلِّها، ٠)              ← بلا قاعدة
#     L(D|M)    = price(ما بعدَ الإطلاق، ٠) + price(الباقي، ٠) ← بالقاعدة، جدولان
#     L(M)      = Σ (طولُ الصورة + ١)·log₂(ALPHA) + log₂(عددُ الصور + ١)
#     Δ         = L(D|M) + L(M) − L₀        والحكمُ `deposit_law.verdict(Δ)`
#
# والبياناتُ **هي هي** في الطرفين: صورُ المجمَّد كلُّها، لا قُصاصةٌ منها — فالمقارنةُ
# قائمةٌ لا متجاورة. وثمنُ التشابك لا يُدفَع، **ويُعلَن سببُه**: المفكِّكُ يفكُّ الرمزَ
# قبل تاليه، فيعرف جدولَ التالي من سابقِه بلا بتٍّ زائد. وليس هنا مكيالٌ خاصّ: كلُّ
# بتٍّ من `deposit_law.price`، وكلُّ حكمٍ من `deposit_law.verdict`.
#
# ــ ٢) وشرطان يمنعان الفاتورةَ أن تكون صدقًا خاويًا ــــــــــــــــــــــــــــــــــ
#   ① **الضابطُ العشوائيّ**: لكلِّ قاعدةٍ ضابطٌ بحجمِ إطلاقها من مواضعَ عشوائيةٍ ببذرةٍ
#      معلنة. فإن لم تهزم القاعدةُ ضابطَها فكسبُها **من الحجم لا من البنية**.
#   ② **حارسُ الانحلال**: قاعدةٌ تُطلِق على نصفِ المقام فأكثرَ تُرَدّ **مهما كانت
#      فاتورتُها** — و«كلُّ موضعٍ يُطلِق» تمرُّ بالفاتورة (Δ<0) ويُسقِطها هذا الحارس،
#      فهو يحرس شيئًا لا خواء (`falsify` ②).
#
# ــ ٣) والشواهدُ هي المُختار، لا الزينة ــــــــــــــــــــــــــــــــــــــــــــــــ
# «قواعدُ تعلُّم» تقتضي مُختارًا من البيانات. والمُختارُ ههنا **شواهدُ النبهانيِّ نفسُه**:
# القاعدةُ المتعلَّمةُ لصفٍّ هي أدنى Δ من بين الصور الواقعة في **كلِّ** شواهد الصفِّ
# الواقعةِ في حدِّنا. ثمّ — وهذا شرطُ النزاهة — **تُعزَل آياتُ الشواهد من التيّار
# وتُعاد الفاتورة**: فلا تُحكَم القاعدةُ على البياناتِ التي اختارتها.
# وصفٌّ بشاهدٍ واحدٍ في حدِّنا **لا اختيارَ فيه** (المرشّحون لا يُنافَس بينهم بشاهدٍ
# واحد)، فيُعلَن «تعلُّمٌ بلا اختيار» ولا يُعَدّ في المتعلَّم بالاختيار.
#
# ــ ٤) الحدُّ المُعلَن: ما لا تقوله هذه المحطّة ــــــــــــــــــــــــــــــــــــــــ
# الفاتورةُ **قبلت المرشّحين كلَّهم** في الفضاء المعلن (0 مردودًا من 132). فقبولُها
# ليس شهادةً بأنّ الصورةَ **بابٌ شرعيّ**، بل بأنّ لها **سياقًا لاحقًا منضبطًا**. فالذي
# يُميِّز ليس الحكمَ الثنائيَّ وحدَه بل **الرتبةُ** في الميدان، و**الضابطُ**، و**المحكُّ
# بعد العزل**. ورأسُ الميدان المتعلَّمُ «من» ليس بابًا من أبواب النبهانيِّ أصلًا —
# يُعلَن كما هو، ولا يُلبَس لَبوسَ اكتشاف.
# وستّةُ صفوفٍ من أحدَ عشرَ **لا تدخل الميدان أصلًا**: تعريفُها بلا صورةٍ تُطلِقها،
# فلا فرضيةَ لها تُسعَّر — وغيابُها معدودٌ معلن، لا مطويّ.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بايتاتٌ غائبة · 4 ختمٌ خالف وديعتَه.
#
# التشغيل:
#   python ta3allum_gate.py                 تقريرٌ معدودٌ على stdout
#   python ta3allum_gate.py --json <ملفّ>   الوديعةُ إلى ملفّ (مولِّدُ الأختام)
#
# ⚑ ولا يُمَسُّ معجمٌ ولا كلفةٌ سابقة: هذه محطّةُ فرضياتٍ على المجمَّد، لا تصنيفُ كلمات.
import argparse
import json
import os
import random
import sys
from collections import Counter
from math import log2

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "induction"))

import dalalat_gate as DG                      # الصفوفُ والشواهدُ من بابها الوحيد لا نسخةً
from alama_layer import parse_marked, CORPUS
from deposit_law import price, verdict, ALPHA, ACCEPT, REJECT

E_USAGE = 2
E_MISSING = 3
E_SEAL = 4


class Ta3allumError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ═══ الإعلاناتُ المجمَّدةُ قبل القياس ═══════════════════════════════════════════════
# ① فضاءُ الفرضيات: **مغلقٌ بشرطين معلنين**، لا مُنتقًى باليد ولا مفتوحٌ بلا حدّ.
#    والطولُ ≤ 3 حدُّ الأدوات في العربية (حرفٌ · حرفان · ثلاثة)، والتكرارُ ≥ n₀ هو
#    عينُ n₀ المعلنِ في `dalalat_gate.THRESHOLDS` — يُقرَأ منه ولا يُعاد كتابتُه،
#    لئلّا يصير في المستودع عتبتان متوافقتان بالصدفة.
SPACE = dict(
    أقصى_طول=3,
    أدنى_تكرار=DG.THRESHOLDS["n₀ مواضع"]["قيمة"],
    تبرير=("الطولُ ≤ ٣ حدُّ أدوات العربية صورةً، والتكرارُ ≥ n₀ يمنع «الصدقَ الخاوي»: "
           "صورةٌ لا تقع إلا مواضعَ قليلةً لا تُعرَض للتكذيب أصلًا. والشرطان يُقاس "
           "عدُّهما ولا يُقرَّر — فلو تغيّرت المدوَّنةُ تغيّر عددُ المرشّحين بمقياسه"),
)

# ② الضابطُ العشوائيُّ ببذرةٍ **معلنةٍ قبل القياس** — ولا تُجرَّب بذورٌ حتى تُوافِق.
CONTROL_SEED = 11

# ③ حارسُ الانحلال: نصيبُ الإطلاق. والنصفُ حدُّ المعنى لا حدُّ الذوق — قاعدةٌ تُطلِق
#    على أكثرَ من نصف المقام لا تفصل بابًا عن سواه، فهي تسميةٌ للمقام لا قاعدةٌ فيه.
COVER_CEILING = 0.5

# ④ قواعدُ الكتاب في الميدان: تُقرأ صورُها من `dalalat_gate.TRIGGERS` — مصدرُ حقيقةٍ
#    واحد. و`الإيماء` صنفٌ ثانٍ (صدرُ الكلمة لا صورتُها كاملةً)، ويُعلَن صنفُه.
BOOK_KINDS = ("صورة", "صدر")

# ⑤ صورةٌ مصنوعةٌ لا تقع في المقام — تُعرَض على المسعِّر في `falsify` ليُثبَت أنّه
#    **يصرخ ولا يُسعِّر فراغًا**. ولا تُعَدّ مرشّحًا ولا تدخل ميدانًا.
FABRICATED_FORM = "ڤڠ"

# ⑥ الأحكامُ المجمَّدة: تُشتقُّ من مواضعها في كلِّ تشغيلٍ وتُصادَم بفارق صفرٍ في `run`.
SEALED_TA3ALLUM = {
    "مرشّحون": 132,
    "صفوفٌ في الميدان": 5,
    "صفوفٌ خارجَ الميدان": 6,
    "مُودَعةٌ بالبرهان": 4,
    "مردودةٌ بالبرهان": 1,
    "مردودٌ من الفضاء": 0,
    "تعلَّمت بالشواهد": 5,
    "تعلُّمٌ باختيار": 1,
    "أعادت صورةَ الكتاب": 1,
    "محاولاتُ_تكذيب": 7,
}


# ═══ ① المقامُ: صورُ المجمَّد، مقروءةً من بابها الوحيد ═══════════════════════════════
def corpus_surfaces():
    """صورُ المجمَّد آيةً آيةً ثمّ مسرودةً — و`fold`/`surface` من `dalalat_gate` لا نسخةً.

    ويُرَدُّ الثلاثةُ معًا لأنّ العزلَ يحتاج حدَّ الآية، والفاتورةُ تحتاج السردَ،
    والاختيارُ بالشواهد يحتاج نصَّ الآية مطويًّا.
    """
    if not os.path.exists(CORPUS):
        raise Ta3allumError(E_MISSING, f"بايتاتُ المجمَّد غائبةٌ: {CORPUS}")
    verses = [[DG.surface(w) for w in v] for v in parse_marked(CORPUS)]
    if not verses:
        raise Ta3allumError(E_MISSING, "المجمَّدُ خلا من آية — لا مقامَ يُقاس")
    return verses, [s for v in verses for s in v], [" ".join(v) for v in verses]


def hypothesis_space(stream):
    """الفضاءُ المغلق: صورٌ طولُها ≤ الأقصى وتكرارُها ≥ الأدنى — مرتَّبةً لا عشوائية."""
    c = Counter(stream)
    return sorted(s for s, n in c.items()
                  if n >= SPACE["أدنى_تكرار"] and 1 <= len(s) <= SPACE["أقصى_طول"]), c


# ═══ ② الفاتورةُ: الحَكَمُ الوحيد — بلا عتبةٍ ولا سلّم ═══════════════════════════════
def declaration_cost(forms):
    """L(M): إملاءُ صورِ القاعدة حرفًا حرفًا بالأبجدية المعلنة، وترميزُ عدَّتها.

    ولا يُخصَم منها شيء: قاعدةٌ بصورتين تدفع ضعفَ ما تدفعه قاعدةٌ بصورة — وهذا
    عينُ ما يمنع القاعدةَ الشرهةَ أن تشتري المقامَ بتكديس الصور.
    """
    return sum((len(f) + 1) * log2(ALPHA) for f in forms) + log2(len(forms) + 1)


def split_bill(stream, fire, forms):
    """Δ = L(D|M) + L(M) − L₀ على **البيانات نفسِها** — تقسيمٌ مشروطٌ على السابق.

    `fire` مجموعةُ إزاحاتِ الكلمات المُطلِقة؛ والمقسومُ هو **تالي** كلِّ مُطلِق. ولا
    تُسعَّر قاعدةٌ لا تُطلِق ولا قاعدةٌ تُطلِق على الكلِّ: كلاهما تقسيمٌ بطرفٍ فارغ،
    وفاتورةُ فراغٍ لا تُقاس — فيُصرَخ ولا يُردُّ رقمٌ مُلفَّق.
    """
    n = len(stream)
    after = [stream[i] for i in range(1, n) if (i - 1) in fire]
    rest = [stream[i] for i in range(n) if i == 0 or (i - 1) not in fire]
    if not after or not rest:
        raise Ta3allumError(E_SEAL, "تقسيمٌ بطرفٍ فارغ — لا فاتورةَ تُقاس على فراغ")
    base = price(stream, 0)["كلفة"]
    lm = declaration_cost(forms)
    return price(after, 0)["كلفة"] + price(rest, 0)["كلفة"] + lm - base


def fire_of(stream, forms=None, head=None):
    """مواضعُ الإطلاق: بالصورة كاملةً، أو بصدرِ الكلمة — والصنفان معلنان لا مخلوطان."""
    if (forms is None) == (head is None):
        raise Ta3allumError(E_USAGE, "الإطلاقُ بصورةٍ أو بصدرٍ — لا بكليهما ولا بلا واحد")
    if head is not None:
        return {i for i, s in enumerate(stream) if s.startswith(head)}
    return {i for i, s in enumerate(stream) if s in forms}


def rule_bill(stream, forms, fire, rng):
    """حكمُ القاعدة كاملًا: الفاتورةُ · الضابطُ العشوائيُّ · حارسُ الانحلال.

    والحكمُ الثلاثيُّ **مُعلَنُ الترتيب**: الانحلالُ أوّلًا لأنّه يُسقِط بلا نظرٍ في
    الفاتورة، ثمّ الفاتورةُ، ثمّ الضابط. ولا حكمَ رابع.
    """
    share = round(len(fire) / len(stream), 4)
    delta = split_bill(stream, fire, forms)
    control = split_bill(stream, set(rng.sample(range(len(stream)), len(fire))), forms)
    degenerate = share >= COVER_CEILING
    if degenerate:
        ruling = "مردودةٌ بالانحلال"
    elif verdict(delta) == REJECT:
        ruling = "مردودةٌ بالفاتورة"
    elif delta >= control:
        ruling = "مردودةٌ بالضابط"
    else:
        ruling = "مُودَعةٌ بالبرهان"
    return dict(صور=list(forms), إطلاق=len(fire), نصيب=share,
                Δ=round(delta, 1), ضابط=round(control, 1),
                حكمُ_الفاتورة=verdict(delta), منحلّة=degenerate, حكم=ruling)


# ═══ ③ الميدان: قواعدُ الكتاب تُسعَّر مع الفضاء كلِّه بالمكيال نفسِه ══════════════════
def arena(stream, candidates):
    """Δ لكلِّ مرشّحٍ مفرد — مرتَّبًا. والرتبةُ ههنا **هي** الحكمُ المميِّز لا الثنائيّ."""
    scored = []
    for form in candidates:
        fire = fire_of(stream, forms=(form,))
        scored.append(dict(صورة=form, إطلاق=len(fire),
                           Δ=round(split_bill(stream, fire, (form,)), 1)))
    scored.sort(key=lambda r: r["Δ"])
    for rank, row in enumerate(scored, 1):
        row["رتبة"] = rank
    return scored


def book_rules(stream, rng):
    """قواعدُ الكتاب الخمسُ المنصوصةُ في الميدان — صورُها من `dalalat_gate.TRIGGERS`.

    ولا تُكتَب ههنا صورةٌ واحدةٌ بيدٍ: لو زِيدت صورةٌ هناك دخلت الفاتورةَ ههنا
    بمقياسها، ولو حُذفت خرجت. فمصدرُ الحقيقة واحد.
    """
    out = []
    for name, t in DG.TRIGGERS.items():
        if t["صور"] is None:
            kind, forms = "صدر", (t["صدر"],)
            fire = fire_of(stream, head=t["صدر"])
        else:
            kind, forms = "صورة", tuple(t["صور"])
            fire = fire_of(stream, forms=set(forms))
        if kind not in BOOK_KINDS:
            raise Ta3allumError(E_SEAL, f"صنفُ إطلاقٍ غيرُ معلن: {kind}")
        out.append(dict(صفّ=name, صنف=kind, دَين=t["دَين"],
                        **rule_bill(stream, forms, fire, rng)))
    return out


# ═══ ④ التعلُّم: الشواهدُ هي المُختار، والفاتورةُ هي الحَكَم ═══════════════════════════
def witness_verses(verse_texts, witness):
    """آياتُ الشاهد في المجمَّد — بالطيِّ نفسِه المطبَّق على الطرفين في `dalalat_gate`."""
    return [i for i, t in enumerate(verse_texts) if witness in t]


def learn_by_witnesses(verses, stream, verse_texts, ranking):
    """لكلِّ صفٍّ: المرشّحون الواقعون في **كلِّ** شواهده في حدِّنا، وأدناهم Δ.

    ثمّ **العزل**: تُطرَح آياتُ شواهده من التيّار وتُعاد الفاتورة — فالرقمُ المُعلَن
    للقاعدة المتعلَّمة رقمٌ على بياناتٍ **لم تختَرْها**. وشاهدٌ واحدٌ لا اختيارَ معه:
    المرشّحُ الواحدُ ليس مُنتخَبًا، فيُعلَن «بلا اختيار» ويُعَدُّ على حِدَة.
    """
    by_form = {r["صورة"]: r for r in ranking}
    rows = []
    for name, shawahid in DG.SHAWAHID.items():
        located = [(w, witness_verses(verse_texts, w)) for w in shawahid]
        inside = [(w, v) for w, v in located if v]
        if not inside:
            rows.append(dict(صفّ=name, شواهدُ_في_الحدّ=0, مرشّحون=0,
                             متعلَّمة=None, حال="لا شاهدَ في حدِّنا"))
            continue
        shared = [f for f in by_form
                  if all(f in w.split() for w, _ in inside)]
        if not shared:
            rows.append(dict(صفّ=name, شواهدُ_في_الحدّ=len(inside), مرشّحون=0,
                             متعلَّمة=None, حال="لا صورةَ تشترك فيها شواهدُه"))
            continue
        best = min(shared, key=lambda f: by_form[f]["Δ"])
        held = {i for _, v in inside for i in v}
        kept = [s for i, v in enumerate(verses) if i not in held for s in v]
        fire = fire_of(kept, forms=(best,))
        delta_held = split_bill(kept, fire, (best,)) if fire and len(fire) < len(kept) else None
        book = DG.TRIGGERS.get(name, {}).get("صور")
        rows.append(dict(
            صفّ=name, شواهدُ_في_الحدّ=len(inside), مرشّحون=len(shared),
            متعلَّمة=best, Δ=by_form[best]["Δ"], رتبة=by_form[best]["رتبة"],
            آياتٌ_معزولة=len(held),
            Δ_بعد_العزل=round(delta_held, 1) if delta_held is not None else None,
            صمدت_بعد_العزل=bool(delta_held is not None and verdict(delta_held) == ACCEPT),
            صورةُ_الكتاب=list(book) if book else None,
            أعادت_صورةَ_الكتاب=bool(book and best in book),
            حال="تعلُّمٌ باختيار" if len(inside) >= 2 else "تعلُّمٌ بلا اختيار"))
    return rows


# ═══ ⑤ محاولاتُ التكذيب — تُشغَّل ولا تُقرَأ ═════════════════════════════════════════
def falsify(stream, candidates, ranking, rules):
    """كلُّ محاولةٍ تُرَدُّ بـ(اسمٍ · أنجحت). ونجاحُ واحدةٍ يُسقِط المحطّة."""
    T = []
    rng = random.Random(CONTROL_SEED)

    # ① الفاتورةُ تقبل الرشَّ: مواضعُ عشوائيةٌ بأحجام قواعد الكتاب تُودَع.
    sprayed = []
    for r in rules:
        fire = set(rng.sample(range(len(stream)), r["إطلاق"]))
        sprayed.append(verdict(split_bill(stream, fire, tuple(r["صور"]))) == ACCEPT)
    T.append(("رشٌّ عشوائيٌّ بحجم قاعدةٍ أُودِع بالفاتورة", any(sprayed)))

    # ② حارسُ الانحلال يحرس الخواء: «كلُّ موضعٍ يُطلِق» تمرُّ بالفاتورة، فلو لم
    #    يُسقِطها الحارسُ لكان مكتوبًا لا مُجرًى.
    everywhere = set(range(len(stream) - 1))
    d_all = split_bill(stream, everywhere, ("",))
    caught = round(len(everywhere) / len(stream), 4) >= COVER_CEILING
    T.append(("«كلُّ موضعٍ يُطلِق» مرَّت بالفاتورة ولم يُسقِطها الحارس",
              verdict(d_all) == ACCEPT and not caught))
    T.append(("«كلُّ موضعٍ يُطلِق» رُدَّت بالفاتورة — فالحارسُ يحرس خواء",
              verdict(d_all) == REJECT))

    # ③ المكيالُ لا يميّز: لو تساوت قيمُ Δ لكان الترتيبُ صدفةً لا قياسًا.
    T.append(("الفاتورةُ لا تميّز بين المرشّحين",
              len({r["Δ"] for r in ranking}) < len(candidates)))

    # ④ الرتبةُ ليست الحجمَ بقناع: لو كان ترتيبُ Δ هو ترتيبَ الإطلاق حرفًا بحرف
    #    لكانت «الفاتورةُ» عدّادَ تكرارٍ مموَّهًا.
    by_delta = [r["صورة"] for r in ranking]
    by_size = [r["صورة"] for r in sorted(ranking, key=lambda r: -r["إطلاق"])]
    T.append(("ترتيبُ الفاتورة هو ترتيبُ الحجم بعينه", by_delta == by_size))

    # ⑤ صورةٌ مصنوعةٌ لا تقع في المقام: يجب أن يُصرَخ، لا أن تُسعَّر بفاتورةِ فراغ.
    try:
        split_bill(stream, fire_of(stream, forms=(FABRICATED_FORM,)), (FABRICATED_FORM,))
        screamed = False
    except Ta3allumError:
        screamed = True
    T.append(("صورةٌ مصنوعةٌ سُعِّرت ولم يُصرَخ بها", not screamed))

    # ⑥ الفضاءُ ليس مفصَّلًا على قواعد الكتاب: صورُ الكتاب المفردةُ كلُّها فيه،
    #    ومع ذلك ليس رأسُه واحدةً منها — ولو كان لكان الفضاءُ مصنوعًا لتصدِّقَ دعوى.
    book_forms = {f for t in DG.TRIGGERS.values() for f in (t["صور"] or ())}
    T.append(("رأسُ الميدان صورةٌ من صور الكتاب — فضاءٌ مفصَّلٌ على دعوى",
              ranking[0]["صورة"] in book_forms))

    return [dict(محاولة=n, نجحت=bool(ok)) for n, ok in T]


# ═══ ⑥ التشغيل ═════════════════════════════════════════════════════════════════════
def run():
    verses, stream, verse_texts = corpus_surfaces()
    candidates, counts = hypothesis_space(stream)
    ranking = arena(stream, candidates)
    rules = book_rules(stream, random.Random(CONTROL_SEED))
    learned = learn_by_witnesses(verses, stream, verse_texts, ranking)
    trials = falsify(stream, candidates, ranking, rules)

    in_arena = {r["صفّ"] for r in rules}
    chosen = [r for r in learned if r["حال"] == "تعلُّمٌ باختيار"]
    measured = {
        "مرشّحون": len(candidates),
        "صفوفٌ في الميدان": len(rules),
        "صفوفٌ خارجَ الميدان": len(DG.ROWS) - len(in_arena),
        "مُودَعةٌ بالبرهان": sum(1 for r in rules if r["حكم"] == "مُودَعةٌ بالبرهان"),
        "مردودةٌ بالبرهان": sum(1 for r in rules if r["حكم"] != "مُودَعةٌ بالبرهان"),
        "مردودٌ من الفضاء": sum(1 for r in ranking if verdict(r["Δ"]) == REJECT),
        "تعلَّمت بالشواهد": sum(1 for r in learned if r["متعلَّمة"]),
        "تعلُّمٌ باختيار": len(chosen),
        "أعادت صورةَ الكتاب": sum(1 for r in learned if r.get("أعادت_صورةَ_الكتاب")),
        "محاولاتُ_تكذيب": len(trials),
    }
    for key, sealed in SEALED_TA3ALLUM.items():
        if measured[key] != sealed:
            raise Ta3allumError(E_SEAL, f"«{key}» = {measured[key]} ≠ المختوم {sealed}")
    if any(t["نجحت"] for t in trials):
        raise Ta3allumError(E_SEAL, "محاولةُ تكذيبٍ نجحت — المحطّةُ ساقطة")

    return {"التعلُّم_v0": {
        "المقام": dict(آيات=len(verses), كلمات=len(stream),
                       صورٌ_مميَّزة=len(counts),
                       **{"L₀": round(price(stream, 0)["كلفة"], 1)}),
        "فضاءُ_الفرضيات": dict(**{k: v for k, v in SPACE.items()}, عدد=len(candidates)),
        "الحَكَم": dict(مكيال="deposit_law.price (رتبة ٠)", حكم="deposit_law.verdict",
                        ضابط=f"عشوائيٌّ بحجم الإطلاق · بذرة {CONTROL_SEED}",
                        سقفُ_الانحلال=COVER_CEILING,
                        بلا_عتبة="لا n₀ ولا فاصلَ ذوبانٍ في الحكم — الفاتورةُ وحدَها"),
        "قواعدُ_الكتاب": rules,
        "رأسُ_الميدان": ranking[:5],
        "ذيلُ_الميدان": ranking[-3:],
        "التعلُّمُ_بالشواهد": learned,
        "محاولاتُ_التكذيب": trials,
        "مقيس": measured,
    }}


def show(R):
    T = R["التعلُّم_v0"]
    m, q = T["مقيس"], T["المقام"]
    print("╔═══ محطّةُ التعلُّم: قواعدُ النبهانيِّ يُعاد بناؤها، والحَكَمُ الفاتورة ═══╗")
    print(f"  المقام: {q['آيات']} آيةً · {q['كلمات']} كلمةً · {q['صورٌ_مميَّزة']} صورةً "
          f"مميَّزةً · L₀ = {q['L₀']:,.1f} بتًّا")
    print(f"  فضاءُ الفرضيات: {m['مرشّحون']} مرشّحًا (طولٌ ≤ {SPACE['أقصى_طول']} · "
          f"تكرارٌ ≥ {SPACE['أدنى_تكرار']})")

    print("\n  قواعدُ الكتاب في الميدان — بلا عتبةٍ ولا سلّم:")
    for r in T["قواعدُ_الكتاب"]:
        mark = "✓" if r["حكم"] == "مُودَعةٌ بالبرهان" else "✗"
        print(f"    {mark} {r['صفّ']:9} ({r['صنف']}) إطلاق {r['إطلاق']:5} · "
              f"Δ = {r['Δ']:+10.1f} · ضابط {r['ضابط']:+9.1f} — {r['حكم']}")
    print(f"    مُودَعةٌ {m['مُودَعةٌ بالبرهان']} · مردودةٌ {m['مردودةٌ بالبرهان']} — "
          f"وستّةُ صفوفٍ بلا صورةٍ تُطلِقها لا تدخل الميدان أصلًا")

    print("\n  رأسُ الميدان المتعلَّم (وليس فيه بابٌ من أبواب النبهاني):")
    for r in T["رأسُ_الميدان"]:
        print(f"    {r['رتبة']:3}. «{r['صورة']}» إطلاق {r['إطلاق']:5} · Δ = {r['Δ']:+10.1f}")

    print("\n  التعلُّمُ بالشواهد — الشواهدُ تختار، والفاتورةُ تحكم بعد العزل:")
    for r in T["التعلُّمُ_بالشواهد"]:
        if r["متعلَّمة"] is None:
            print(f"    —  {r['صفّ']:9} {r['حال']}")
            continue
        same = " ⟵ صورةُ الكتاب نفسُها" if r["أعادت_صورةَ_الكتاب"] else ""
        held = "صمدت" if r["صمدت_بعد_العزل"] else "سقطت"
        print(f"    •  {r['صفّ']:9} شواهد {r['شواهدُ_في_الحدّ']} · مرشّحون "
              f"{r['مرشّحون']:3} ⟶ «{r['متعلَّمة']}» رتبة {r['رتبة']:3} · "
              f"بعد عزل {r['آياتٌ_معزولة']} آيةً: {held}{same}  [{r['حال']}]")
    print(f"    تعلَّمت {m['تعلَّمت بالشواهد']} · منها باختيارٍ {m['تعلُّمٌ باختيار']} · "
          f"أعادت صورةَ الكتاب {m['أعادت صورةَ الكتاب']}")

    print(f"\n  الحدُّ المُعلَن: مردودٌ من الفضاء {m['مردودٌ من الفضاء']} من {m['مرشّحون']} "
          f"— فالقبولُ شهادةُ سياقٍ لا شهادةُ بابٍ شرعيّ، والمميِّزُ الرتبةُ والضابطُ والعزل")
    print(f"  محاولاتُ التكذيب: {m['محاولاتُ_تكذيب']} — لم تنجح واحدةٌ منها ✓")


def main(argv=None):
    ap = argparse.ArgumentParser(description="محطّةُ التعلُّم: الحَكَمُ الفاتورة")
    ap.add_argument("--json", metavar="ملفّ", help="وديعةُ المحطّة إلى ملفّ")
    args = ap.parse_args(argv)
    try:
        R = run()
    except Ta3allumError as e:
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
