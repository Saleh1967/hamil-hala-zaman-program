# jumla_links.py — محرّكُ الربط الاثني عشر: كلُّ حدِّ جملةٍ بسببه وشاهدِه الإعرابيِّ ومقامِه.
# ═══════════ التسجيلُ المسبق — موقَّعٌ قبل أيّ سطر، ونسختُه تدخل الالتزام ═══════════════════
# ▸ **تعريفُ الجملة** (حدٌّ واحدٌ معلن، من البايتات وحدَها): صدرُها
#     ① فعلٌ (ماضٍ/مضارع/أمر) **ظاهرُ الإعراب** — صنفُه «فعل» عند `jar_gate.word_class`
#        وخاتمةٌ محرَّكةٌ أو ساكنة، لا هيكلٌ عارٍ يُظَنّ فعلًا؛ أو
#     ② اسمٌ معرَّفٌ باللام **مرفوعٌ بضمّةٍ ظاهرة** لم يسبقه فعلٌ ولا جارٌّ — أي مبتدأ.
#   و**العاطفُ يبدأ جملةً جديدة**: الملتصقُ (و/ف مفتوحةً على جذعٍ غيرِ خالٍ) والمنفصلُ
#   المسمّى (ثم · أو · أم · بل) — وهذا **حدُّ تقطيعٍ لا تصنيفَ واوٍ** (انظر حدَّ السقوط أدناه).
#
# ▸ **الأسبابُ الاثنا عشر بأولوية الإعراب المعلنة** (أوّلُها الحاكم، والباقي يُعَدّ مستقلًّا
#   كما عُدَّت أبوابُ الجرّ): خبر ← حال ← جواب شرط ← صلة موصول ← نعت ← بدل ← مفعول ←
#   مضاف إليه ← جواب قسم ← تعليل ← مفسرة ← مؤكدة.
#   وما لم يُحسَم ⟵ **«مستقلٌّ بمناسبة»** معلَّقًا على باب التفسير، **لا يُخمَّن**.
#
# ▸ **المقامان معلنان ولا يُخلط مقامٌ بمقام**:
#     (أ) أزواجٌ **داخل الآية**: كلُّ صدرَين متجاورَين في آيةٍ واحدة — N يُطبع قبل العدّ.
#     (ب) أزواجُ **العبور**: آخرُ جملةٍ في الآية ⟷ أوّلُ جملةٍ في التالية — **6,235** حدًّا.
#   ولكلِّ مقامٍ تغطيتُه ومتبقّيه على حدةٍ؛ ولا يُجمَع رقمُ مقامٍ إلى رقم الآخر.
#
# ▸ **الشروطُ المختومة بفواصل إسقاطها**:
#     ① تغطيةُ الحدود المُصنَّفة **≥ 90%** في كلِّ مقامٍ على حدة.
#     ② المتبقّي **غير المسمّى = 0** داخل الأسباب — وكلُّ موضعٍ خارجَها يُبوَّب بجنسٍ مسمًّى،
#        و«غيرُ ذلك» صفرٌ أو سقط الشرط.
#   وإن ظهر موضعٌ **سقط التسجيل وسُمّي بعينه** (على سنّة جولات `jar_gate`): الحكمُ يُودَع
#   بنصِّه ساقطًا، ولا يُرفَع بجولةٍ تالية ولا بمقامٍ أُعلن بعده.
#
# ▸ **حدُّ السقوط الأهمّ**: العطفُ بالواو/الفاء **ليس سببًا من الاثني عشر**. فحين يبدأ صدرٌ
#   بعاطفٍ يُقلَع الملتصقُ ويُبحَث عن السبب **فيما بعده**؛ فإن لم يُوجَد عُلِّق الموضعُ
#   بـ**«بمناسبة عطفٍ معلنة»** — وهو **تعليقٌ لا تصنيف**: لا يُحتسَب تغطيةً ولا يُدَّعى فيه
#   أنّ الواوَ عاطفةٌ. و**الوثيقةُ مرجعُ الوسوم لا مُلزِمُ التغطية**: أسماءُ الأسباب منها،
#   وأرقامُ التغطية من البايتات وحدَها.
#
# ▸ **حدودي المعلنة**: لا واوَ تُصنَّف عاطفةً بقائمة — بشاهدِ إعرابٍ (فتحةُ الملتصق على جذعٍ
#   غيرِ خالٍ) أو بعلَّاقةٍ معلنة · ولا رقمَ في README إلّا بعمودَي [الصنف]/[الدالّة] ·
#   والبوّابةُ `python induction/seals.py` exit 0 قبل الدفع.
#
# ▸ **والمصادمةُ الخارجية لاحقة**: عند وصول تفسيرٍ مختوم (`QAC-fork-v0.4` · الطبري) تُقارَن
#   مقاطعُه بالأسباب — الاتفاقُ شاهدٌ والخلافُ **جنسٌ مسمّى**. ولا رقمَ يُنقَل من تقريرٍ
#   سابق: كلُّ عددٍ هنا يخرج من المجمَّد بختمه 8b387ea8… عبر `parse_verses` بعينها.
# ⚑ ولا تُمَسّ كلفةُ طبقةٍ سابقةٍ ولا معجمُها: هذه طبقةُ حدودٍ فوق الكلمة، لا تصنيفُ كلمات.
from collections import Counter
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
assert os.path.isfile(os.path.join(ROOT, "induction", "induction_engine.py")), \
    "محرّك الاستقراء غائبٌ عن induction/ — لا استيراد صامت"
sys.path.insert(0, os.path.join(ROOT, "induction"))
from induction_engine import parse_verses                 # المجمَّد بختمه — لا نسخةَ ثانية
# الوسومُ الإعرابيةُ تُورَث من بوّابة الجرّ بعينها، فلا مصنِّفَ ثانٍ يتخالف معها صامتًا:
from jar_gate import word_class, verb_template, is_definite, _body, QAWL

CORPUS = os.path.join(ROOT, "mujammad.txt")

# ــــــ قوائمُ الوسوم: منتهيةٌ مسمّاةٌ، ومرجعُها الوثيقةُ لا العدّ ــــــ
ATF_ATTACHED = ("و", "ف")                     # الملتصقُ — بفتحةٍ على جذعٍ غيرِ خالٍ
ATF_SEPARATE = ("ثم", "أو", "أم", "بل")        # المنفصلُ المسمّى
SHART = ("إن", "ان", "إذا", "اذا", "لو", "لولا", "لئن", "كلما", "مهما", "أينما", "حيثما",
         "إذما", "لوما")
MAWSUL = ("الذي", "التي", "الذين", "اللذان", "اللذين", "اللتان", "اللتين", "اللاتي",
          "اللائي", "اللواتي", "الذى")
ZARF_MUDAF = ("إذ", "اذ", "إذا", "اذا", "يوم", "حين", "حيث", "لما", "بعد", "قبل", "مثل",
              "عند", "يومئذ")
QASAM = ("تالله", "أقسم", "اقسم", "لعمرك", "والله")        # صيغُ القسم المسمّاة
TA3LIL = ("كي", "لكي", "لعل", "لعله", "لعلهم", "لعلكم", "لعلنا", "لعلي")
TAFSIR = ("أي", "اي")                                      # حرفُ التفسير المسمّى
QAWL_TAFSIR = ("أوحى", "اوحى", "نادى", "نودي", "كتب", "قضى", "أمر", "امر")

sk = lambda w: "".join(c for c, _ in w)
END = lambda w: w[-1][1]

# الأسبابُ الاثنا عشر بأولويةِ الإعراب المعلنة — الترتيبُ حاكمٌ، ولا يُعاد ترتيبُه بعد التشغيل.
REASONS = ("خبر", "حال", "جواب شرط", "صلة موصول", "نعت", "بدل", "مفعول", "مضاف إليه",
           "جواب قسم", "تعليل", "مفسرة", "مؤكدة")
SUSPENDED = "مستقلٌّ بمناسبة"                 # معلَّقٌ على باب التفسير — لا يُخمَّن
ATF_SUSPENDED = "بمناسبة عطفٍ معلنة"          # تعليقٌ لا تصنيف — العطفُ ليس سببًا


# ------------------------------------------------- ① تعريفُ الجملة وتقطيعُها
def attached_atf(w):
    """عاطفٌ ملتصقٌ **بشاهدٍ من البايتات**: و/ف مفتوحةً على جذعٍ غيرِ خالٍ — لا بقائمةِ واوات.
    وهو وسمُ تقطيعٍ لا دعوى إعراب: لا يُقال «هذه واوُ عطف»، بل «صدرٌ تحته ملتصقٌ مفتوح»."""
    return len(w) > 1 and w[0][0] in ATF_ATTACHED and w[0][1] == "فتحة"


def verb_head(w):
    """صدرٌ فعليٌّ **ظاهرُ الإعراب**: صنفُه «فعل» عند المصنِّف الموروث (`jar_gate.word_class`)
    وخاتمتُه ظاهرة. والقالبُ **المشترك** (فعل · أفعل) صنفُه «مشتبه» فلا يُدَّعى فيه صدرٌ
    فعليّ — ثمنُه معلن: «قيل» و«ريب» و«على» لا تفتح جملةً بقالبها وحدَه."""
    body = _body(w)[1]
    if len(body) < 3 or word_class(body) != "فعل":
        return None
    if END(body) not in ("فتحة", "ضمة", "سكون", "كسرة"):
        return None
    return f"صنفٌ «فعل» بقالبٍ حاسمٍ «{verb_template(body)}» وخاتمةٌ {END(body)} ظاهرة"


def noun_head(w, prev):
    """صدرٌ اسميٌّ: معرَّفٌ باللام **مرفوعٌ بضمّةٍ ظاهرة**، ولا فعلَ قبله ولا جارَّ — مبتدأ."""
    body = _body(w)[1]
    if not is_definite(w) or END(body) != "ضمة":
        return None
    if prev is not None and (word_class(_body(prev)[1]) in ("فعل", "حرف")
                             or word_class(prev) == "حرف"):
        return None
    return "معرَّفٌ باللام مرفوعٌ بضمّةٍ ظاهرة، لا فعلَ قبله ولا حرف"


def head_of(w, prev):
    """صنفُ الصدر وشاهدُه الإعرابيّ، أو None — والعاطفُ يبدأ جملةً بنصّ التسجيل."""
    if attached_atf(w):
        return "صدرٌ بعاطفٍ ملتصق", "ملتصقٌ مفتوحٌ (و/ف) على جذعٍ غيرِ خالٍ"
    if sk(w) in ATF_SEPARATE:
        return "صدرٌ بعاطفٍ منفصل", f"عاطفٌ منفصلٌ مسمًّى: {sk(w)}"
    v = verb_head(w)
    if v:
        return "صدرٌ فعليّ", v
    n = noun_head(w, prev)
    if n:
        return "صدرٌ اسميّ", n
    return None


def segment(verse):
    """الآيةُ ⟼ جملٌ، كلٌّ (موضعُ صدرها · صنفُه · شاهدُه). وأوّلُ الآية صدرٌ بحدِّ التلاوة."""
    heads = []
    for i, w in enumerate(verse):
        h = head_of(w, verse[i - 1] if i else None)
        if i == 0:
            heads.append((0, h[0] if h else "صدرُ آيةٍ بحدّ التلاوة",
                          h[1] if h else "أوّلُ الآية — حدُّ تلاوةٍ لا حدُّ إعراب"))
        elif h:
            heads.append((i, h[0], h[1]))
    return heads


# ------------------------------------------------- ② الأسبابُ الاثنا عشر بشواهدها
def _prev_sentence(verse, heads, k):
    """جملةُ ما قبل الصدر رقم k في الآية نفسها: [صدرُها … ما قبل الصدر الحاليّ]."""
    start = heads[k - 1][0]
    return verse[start:heads[k][0]]


def reasons_of(head_w, prev_w, prev_sent):
    """كلُّ الأسباب المنطبقة على الحدّ، **بترتيب الأولوية المعلن** (أوّلُها الحاكم).

    وكلُّ سببٍ بشاهدٍ إعرابيٍّ من البايتات — ولا سببَ بقرينةٍ مظنونة. والبحثُ يجري على
    الصدر **بعد قلع الملتصق المفتوح**، وفاءً بحدِّ السقوط: العطفُ ليس سببًا، فيُبحَث عن
    سبب الجملة فيما بعده.
    """
    core = _body(head_w)[1]
    out = []
    prev_sk = sk(prev_w) if prev_w is not None else ""
    prev_core = sk(_body(prev_w)[1]) if prev_w is not None else ""
    sent_sks = [sk(x) for x in prev_sent]
    sent_heads = sent_sks[:1]

    # ① خبر — المبتدأ المعرَّفُ المرفوعُ صدرَ السابقة، ولا فعلَ فيها يشغل الخبر.
    if prev_sent and is_definite(prev_sent[0]) and END(_body(prev_sent[0])[1]) == "ضمة" \
       and not any(word_class(_body(x)[1]) == "فعل" for x in prev_sent[1:]):
        out.append(("خبر", "مبتدأٌ معرَّفٌ مرفوعٌ بضمّةٍ ظاهرة صدرَ السابقة بلا فعلٍ بعده"))
    # ② حال — صاحبُ حالٍ معرفةٌ منصوبةٌ بفتحةٍ ظاهرة، والصدرُ فعليّ.
    if prev_w is not None and is_definite(prev_w) and END(prev_w) == "فتحة" \
       and word_class(core) == "فعل":
        out.append(("حال", "معرفةٌ منصوبةٌ بفتحةٍ ظاهرة قبل صدرٍ فعليّ"))
    # ③ جواب شرط — أداةُ شرطٍ مسمّاةٌ صدرَ الجملة السابقة.
    shart = [s for s in sent_heads
             if s in SHART or (s[:1] in ATF_ATTACHED and s[1:] in SHART)]
    if shart:
        out.append(("جواب شرط", f"أداةُ شرطٍ مسمّاةٌ صدرَ السابقة: {shart[0]}"))
    # ④ صلة موصول — موصولٌ مسمًّى قبل الصدر مباشرة.
    if prev_sk in MAWSUL or prev_core in MAWSUL:
        out.append(("صلة موصول", f"موصولٌ مسمًّى قبل الصدر: {prev_sk}"))
    # ⑤ نعت — نكرةٌ منوَّنةٌ قبل الصدر: الجملُ بعد النكرات صفاتٌ بالوسم المعلن.
    if prev_w is not None and END(prev_w).startswith("تنوين"):
        out.append(("نعت", f"نكرةٌ منوَّنةٌ قبل الصدر ({END(prev_w)})"))
    # ⑥ بدل — معرفتان متواليتان تتّفقان في الخاتمة الإعرابية ويختلف هيكلاهما.
    if prev_w is not None and is_definite(prev_w) and is_definite(head_w) \
       and END(prev_w) == END(core) and END(prev_w) in ("ضمة", "فتحة", "كسرة") \
       and sk(prev_w) != sk(core):
        out.append(("بدل", f"معرفتان متواليتان بخاتمةٍ واحدة ({END(prev_w)}) واختلافِ هيكل"))
    # ⑦ مفعول — فعلُ قولٍ مسمًّى قبل الصدر: الجملةُ مقولُ القول.
    if prev_sk in QAWL or prev_core in QAWL:
        out.append(("مفعول", f"فعلُ قولٍ مسمًّى قبل الصدر: {prev_sk}"))
    # ⑧ مضاف إليه — ظرفٌ مضافٌ مسمًّى قبل الصدر.
    if prev_sk in ZARF_MUDAF or prev_core in ZARF_MUDAF:
        out.append(("مضاف إليه", f"ظرفٌ مضافٌ مسمًّى قبل الصدر: {prev_sk}"))
    # ⑨ جواب قسم — صيغةُ قسمٍ مسمّاةٌ في السابقة.
    qasam = [s for s in sent_sks if s in QASAM]
    if qasam:
        out.append(("جواب قسم", f"صيغةُ قسمٍ مسمّاةٌ في السابقة: {qasam[0]}"))
    # ⑩ تعليل — لامٌ مكسورةٌ على صدرٍ فعليّ، أو أداةُ تعليلٍ مسمّاة.
    if (core[0][0] == "ل" and core[0][1] == "كسرة" and len(core) > 1) or sk(core) in TA3LIL:
        out.append(("تعليل", "لامٌ مكسورةٌ على الصدر أو أداةُ تعليلٍ مسمّاة"))
    # ⑪ مفسرة — حرفُ تفسيرٍ مسمًّى، أو فعلٌ فيه معنى القول لا صريحُه.
    if prev_sk in TAFSIR or prev_core in TAFSIR or prev_core in QAWL_TAFSIR:
        out.append(("مفسرة", f"حرفُ تفسيرٍ أو فعلُ قولٍ غيرُ صريحٍ قبل الصدر: {prev_sk}"))
    # ⑫ مؤكدة — تكرارٌ حرفيٌّ للجملة السابقة بهيكلها.
    if sent_sks and sk(core) == sent_sks[0] and len(sent_sks) == 1:
        out.append(("مؤكدة", "تكرارٌ حرفيٌّ لهيكل الجملة السابقة"))
    order = {r: i for i, r in enumerate(REASONS)}
    return sorted(out, key=lambda x: order[x[0]])


def classify(head_w, prev_w, prev_sent, head_kind):
    """السببُ الحاكمُ وشاهدُه ومقامُه — أو تعليقٌ **مسمًّى** لا تخمين."""
    rs = reasons_of(head_w, prev_w, prev_sent)
    if rs:
        return rs[0][0], rs[0][1], [r for r, _ in rs]
    if head_kind in ("صدرٌ بعاطفٍ ملتصق", "صدرٌ بعاطفٍ منفصل"):
        return ATF_SUSPENDED, "صدرٌ بعاطفٍ ولا سببَ فيما بعده — تعليقٌ لا تصنيف", []
    return SUSPENDED, "لا قرينةَ إعرابيةً من البايتات — معلَّقٌ على باب التفسير", []


# ------------------------------------------------- ③ المقامان: داخلُ الآية ثمّ العبور
def _residue_kind(head_kind):
    """جنسُ المتبقّي **بالاسم**: لا موضعَ بلا جنس، و«غيرُ ذلك» صفرٌ أو سقط الشرط."""
    return {"صدرٌ بعاطفٍ ملتصق": "صدرٌ بعاطفٍ ملتصق",
            "صدرٌ بعاطفٍ منفصل": "صدرٌ بعاطفٍ منفصل",
            "صدرٌ فعليّ": "صدرٌ فعليٌّ بلا قرينة",
            "صدرٌ اسميّ": "صدرٌ اسميٌّ بلا قرينة",
            "صدرُ آيةٍ بحدّ التلاوة": "صدرُ آيةٍ بلا قرينة"}.get(head_kind, "غيرُ ذلك")


def _tally(links):
    """عدُّ مقامٍ واحد — لا يُجمَع إلى غيره ولا يُجسَر به."""
    causes = Counter(l["سبب"] for l in links if l["سبب"] in REASONS)
    residue = [l for l in links if l["سبب"] not in REASONS]
    kinds = Counter(_residue_kind(l["صنفُ الصدر"]) for l in residue)
    n = len(links)
    return dict(
        حدود=n, مصنَّف=sum(causes.values()), معلَّق=len(residue),
        أسباب={r: causes[r] for r in REASONS},
        أسبابٌ_مستقلّة={r: sum(1 for l in links if r in l["أسبابٌ منطبقة"]) for r in REASONS},
        تعليقات=dict(Counter(l["سبب"] for l in residue).most_common()),
        أجناسُ_المتبقّي=dict(kinds.most_common()),
        غيرُ_المسمّى=kinds["غيرُ ذلك"],
        تغطية=round(sum(causes.values()) / n, 4) if n else 0.0)


def links_within(verses):
    """المقامُ (أ): أزواجٌ **داخل الآية** — N يُطبع قبل العدّ، ولا يُخلط بالعبور."""
    out = []
    for vi, verse in enumerate(verses):
        heads = segment(verse)
        for k in range(1, len(heads)):
            i, kind, witness = heads[k]
            sbb, shahid, all_r = classify(verse[i], verse[i - 1],
                                          _prev_sentence(verse, heads, k), kind)
            out.append({"مقام": "داخل الآية", "آية": vi + 1, "موضع": i,
                        "هيكل": sk(verse[i]), "صنفُ الصدر": kind, "شاهدُ الصدر": witness,
                        "سبب": sbb, "شاهدٌ إعرابيّ": shahid, "أسبابٌ منطبقة": all_r})
    return out


def links_crossing(verses):
    """المقامُ (ب): أزواجُ **العبور** — 6,235 حدًّا، حدُّ الآية يُعبَر معلنًا لا صامتًا."""
    out = []
    for vi in range(1, len(verses)):
        prev_verse, verse = verses[vi - 1], verses[vi]
        heads = segment(verse)
        i = 0
        kind, witness = heads[0][1], heads[0][2]
        prev_heads = segment(prev_verse)
        prev_sent = prev_verse[prev_heads[-1][0]:]
        sbb, shahid, all_r = classify(verse[i], prev_verse[-1], prev_sent, kind)
        out.append({"مقام": "العبور", "آية": vi + 1, "موضع": i, "هيكل": sk(verse[i]),
                    "صنفُ الصدر": kind, "شاهدُ الصدر": witness, "سبب": sbb,
                    "شاهدٌ إعرابيّ": shahid, "أسبابٌ منطبقة": all_r})
    return out


def _sample(links, kind, n=6):
    """عيّناتٌ **مسمّاةٌ بعينها** من المتبقّي — فالسقوطُ يُسمّى ولا يُعَدّ وحسب."""
    return [f"{l['آية']}:{l['موضع']} {l['هيكل']}"
            for l in links if _residue_kind(l["صنفُ الصدر"]) == kind][:n]


def preregistration_verdict(within, crossing):
    """حكمُ التسجيل المسبق بنصِّه — يُودَع ساقطًا إن سقط، ولا يُرفَع بجولةٍ تالية."""
    fails = []
    for name, t in (("داخل الآية", within), ("العبور", crossing)):
        if t["تغطية"] < 0.90:
            fails.append(f"تغطيةُ «{name}» {t['تغطية']:.4f} < 0.90 "
                         f"({t['مصنَّف']:,} من {t['حدود']:,})")
        if t["غيرُ_المسمّى"]:
            fails.append(f"متبقٍّ غيرُ مسمًّى في «{name}»: {t['غيرُ_المسمّى']}")
    if not fails:
        return "صمد: الشرطان محقَّقان في المقامين — تغطيةٌ ≥ 90% ومتبقٍّ مسمًّى كلُّه"
    return "سقط التسجيل بفواصله المعلنة: " + " · ".join(fails)


def run(path=CORPUS):
    verses = parse_verses(path)
    within, crossing = links_within(verses), links_crossing(verses)
    W, C = _tally(within), _tally(crossing)
    R = dict(
        seals=dict(mujammad_sha256_prefix="8b387ea8", verses=len(verses),
                   words=sum(len(w) for w in verses)),
        جمل=dict(داخل_الآية=sum(len(segment(v)) for v in verses)),
        مقامات=dict(داخل_الآية=W, العبور=C),
        أسبابٌ_معلنة=list(REASONS),
        تعليق=dict(مستقل=SUSPENDED, عطف=ATF_SUSPENDED),
        عيّنات={name: {j: _sample(links, j) for j in t["أجناسُ_المتبقّي"]}
                for name, links, t in (("داخل الآية", within, W), ("العبور", crossing, C))},
        preregistration=preregistration_verdict(W, C),
        atf_clause="العطفُ بالواو/الفاء ليس سببًا من الاثني عشر: يُقلَع الملتصقُ ويُبحَث عن "
                   "السبب فيما بعده، وإلّا عُلِّق الموضعُ بـ«بمناسبة عطفٍ معلنة» — تعليقٌ "
                   "لا تصنيف، ولا يُحتسَب تغطيةً.",
        stations_clause="المقامان لا يُجمَعان: أزواجُ داخل الآية مقامٌ، وأزواجُ العبور "
                        "(6,235) مقامٌ آخر — لكلٍّ تغطيتُه ومتبقّيه، ولا يُنقَل رقمٌ بينهما.",
        collision_clause="المصادمةُ الخارجيةُ لاحقة: عند وصول تفسيرٍ مختوم تُقارَن مقاطعُه "
                         "بالأسباب — الاتفاقُ شاهدٌ والخلافُ جنسٌ مسمّى (طابورُ الختم في "
                         "AUDIT-188.md).",
        doc_clause="الوثيقةُ مرجعُ الوسوم لا مُلزِمُ التغطية: أسماءُ الأسباب الاثني عشر "
                   "منها، وكلُّ رقمٍ هنا من البايتات عبر parse_verses بعينها.",
        cost_bits=(len(REASONS) + 2) * 8 * 4,
    )
    # ---------- أَسِرَّةُ الصريخ ----------
    assert R["seals"]["verses"] == 6236 and R["seals"]["words"] == 77801, \
        "مصالحةُ العدّ خُولفت — صريخ"
    assert C["حدود"] == 6235, f"أزواجُ العبور ليست 6,235 بل {C['حدود']} — صريخ"
    for name, t in (("داخل الآية", W), ("العبور", C)):
        assert t["مصنَّف"] + t["معلَّق"] == t["حدود"], f"مصالحةُ «{name}» خُولفت — صريخ"
        assert sum(t["أجناسُ_المتبقّي"].values()) == t["معلَّق"], \
            f"أجناسُ متبقّي «{name}» لا تُصالِح عدَّه — صريخ"
    assert R["جمل"]["داخل_الآية"] == W["حدود"] + len(verses), \
        "عدُّ الجمل لا يُصالِح حدودَ داخل الآية — صريخ"
    return R


def main(argv=None):
    ap = argparse.ArgumentParser(description="محرّكُ الربط الاثني عشر — سببٌ وشاهدٌ ومقام")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    R = run()
    W, C = R["مقامات"]["داخل_الآية"], R["مقامات"]["العبور"]
    print(f"الجملُ المقطوعةُ بالتعريف المعلن: {R['جمل']['داخل_الآية']:,} في "
          f"{R['seals']['verses']:,} آية")
    for name, t in (("داخل الآية", W), ("العبور", C)):
        print(f"المقامُ «{name}» — N = {t['حدود']:,} حدًّا (يُطبع قبل العدّ):")
        print("    الأسبابُ الحاكمة: " +
              " · ".join(f"{r}={t['أسباب'][r]:,}" for r in R["أسبابٌ_معلنة"] if t["أسباب"][r]))
        print("    مستقلّةً (بلا أولوية): " +
              " · ".join(f"{r}={n:,}" for r, n in t["أسبابٌ_مستقلّة"].items() if n))
        print(f"    التغطية: {t['مصنَّف']:,}/{t['حدود']:,} = {t['تغطية']:.4f} · "
              f"المعلَّق {t['معلَّق']:,}")
        print("    أجناسُ المتبقّي بالاسم: " +
              " · ".join(f"{k}={n:,}" for k, n in t["أجناسُ_المتبقّي"].items()))
        for k, s in R["عيّنات"][name].items():
            if s:
                print(f"      {k}: " + " · ".join(s))
    print(f"    {R['stations_clause']}")
    print(f"    {R['atf_clause']}")
    print(f"    {R['doc_clause']}")
    print(f"    {R['collision_clause']}")
    print(f"حكمُ التسجيل المسبق: {R['preregistration']}")
    print(f"كلفةُ الطبقة معلنة: {R['cost_bits']} بت — ⚑ ولا كلفةَ سابقةً مُسَّت")
    if a.json:
        json.dump({"الربط_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
