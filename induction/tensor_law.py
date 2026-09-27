# tensor_law.py — دعوى T = سابقة ⊗ وزن ⊗ لاحقة، معروضةً على الحَكَم الذي أودعناه.
#
# ── الدعوى كما وردت ───────────────────────────────────────────────────────────────
#   «تحليلٌ مفردٌ منعكس = مقبول · متعددٌ = معلَّق إلى الحارس · خارج النطاق معلن»
#   وأرقامُها: مفرد-منعكس 27,533 · متنازع 931 · خارج-النطاق 49,337 ·
#              ميمٌ بلا منازع 1,164 · ميمٌ متنازع 106.
#
# ── T₁ تصديق: الأرقامُ الخمسةُ تكرّرت بفارق صفر ────────────────────────────────────
#   وأكثرُ من ذلك: فُحص احتمالُ تضخُّمٍ بتكرار التحليل الواحد (`factorize` لا تُسقط
#   المكرَّر) فكان **صفرًا** — لا كلمةَ واحدةٌ تكرّر تحليلُها. فالعدُّ نظيف.
#
# ── T₂ تفنيد: «مفردٌ منعكس» ليس قبولًا، والدعوى ترسب على الفاتورة ─────────────────
#   ① **الانعكاسُ هنا كسابقه لا يرفض**: `expand(p,t,root,s) == word` صحيحٌ بالبناء،
#      لأنّ `p` و`s` قُطعا من الكلمة و`root` التُقط بالمطابقة. فشرطُ «منعكس» تحصيلُ حاصل
#      (كما في mirror.py). والذي يفرز فعلًا هو **عددُ التحليلات** لا انعكاسُها.
#   ② **الحَكَمُ فاتورةُ قانون الوديعة** (deposit_law.py): Δ = L(D|M) + L(M) − L₀.
#      والتنسورُ **يُرفَض**: Δ = +69,037 بت. ويُرفَض في كلِّ صوره، ودون الأساس دائمًا.
#   ③ **جدولُ السوابق يضرّ لا ينفع**: إسقاطُ الميم **يُحسِّن** الفاتورة 3,211 بت،
#      وسوابقُ مختلقةٌ لا وجودَ لها (ض ظ غ ث) أرخصُ من السوابق الحقيقية.
#   ④ **59.9% من «المفرد المنعكس» بلا تنسورٍ البتّة**: 16,487 من 27,533 هيكلُها
#      (∅ · فعل · ∅) — أي جذرٌ عارٍ بلا سابقةٍ ولا لاحقة. فالرقمُ يعدّ ما لا يخصّ الدعوى.
#   ⑤ **«الميمُ بلا منازع» ليست بلا منازع**: 446 من 1,164 لها **شاهدٌ مضادٌّ من
#      البايتات** — جذعُها قبل الضمير كلمةٌ مشهودةٌ في المجمَّد نفسِه (منهم = من+هم 153 ·
#      منكم = من+كم 107 · منها = من+ها 86 · معكم · معهم…). و«بلا منازع» إنما كانت
#      كذلك لأنّ «من» و«مع» ليستا في `PREFIX` — فالسكوتُ عدمُ منازعٍ في الجدول لا في اللغة.
#      والباقي 718 فيه أعلامٌ ظاهرة (موسى 129 · مريم 33) — تُسمّى ولا يُفتَح لها باب.
#
# ── الحكم ─────────────────────────────────────────────────────────────────────────
#   الدعوى **صحيحةُ العدّ، مرفوضةُ الوديعة**. ولا تُودَع حتى تُخفّض الفاتورة، ولا يُنقَل
#   رقمُ «مفرد-منعكس» تغطيةً. وهذا ليس ردًّا للتنسور مبدأً — بل ردٌّ لهذا الجدول بهذه
#   النوى: ثلاثُ نوًى (فعل·فعلل·فاعل) لا تكفي، و«فعل» منها ثلاثةُ محارفَ حرّةٍ تطابق كلَّ ثلاثيّ.
import sys, os, json, re, random
from math import log2
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from induction_engine import parse_verses

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
PREFIX = ("است", "ان", "اف", "أ", "ت", "م", "")
SUF = ("هما", "كما", "هن", "هم", "كن", "كم", "نا", "ها", "ه", "ك", "ي")
CORES = ["فعل", "فعلل", "فاعل"]
GUARD_TA = "ة"
ALPHA = 36

SEALED_TENSOR = dict(مفرد=27533, متنازع=931, خارج=49337,
                     ميمٌ_بلا_منازع=1164, ميمٌ_متنازع=106,
                     تحليلٌ_مكرَّر=0, بلا_تنسور=16487, شاهدٌ_مضادّ=446)


def rx(t):
    lg = {}; out = ""; idx = 0
    for ch in t:
        if ch in "فعل":
            lg.setdefault(ch, []).append(idx + 1); out += "(.)"; idx += 1
        else:
            out += ch
    return re.compile("^" + out + "$"), lg


RXS = [(t, *rx(t)) for t in CORES]


def expand(p, t, root, s):
    m = {"ف": root[0], "ع": root[1], "ل": root[2]}
    return p + "".join(m[ch] if ch in "فعل" else ch for ch in t) + s


def factorize(word, prefixes=PREFIX, sufs=SUF):
    """كلُّ التحليلات المنعكسة. وشرطُ الانعكاس تحصيلُ حاصل — يُبقى للمصادمة لا للفرز."""
    out = []
    if word.endswith(GUARD_TA):
        return out
    for p in prefixes:
        if not word.startswith(p):
            continue
        mid = word[len(p):]
        for s in sufs + ("",):
            if s and (not mid.endswith(s) or len(mid) - len(s) < 2):
                continue
            core = mid[:-len(s)] if s else mid
            for t, r, lg in RXS:
                m = r.match(core)
                if m and all(len(set(m.group(g) for g in gs)) == 1 for gs in lg.values()):
                    root = "".join(m.group(lg[l][0]) for l in "فعل")
                    if expand(p, t, root, s) == word:
                        out.append((p or "∅", t, root, s or "∅"))
    return out


def tensor_bill(words, prefixes, sufs):
    """فاتورةُ قانون الوديعة مطبَّقةً على التنسور. **الحروفُ في أبجديةٍ واحدة** جذرًا
    كانت أو غيرَ محلَّلة — فلا تُشتَّت التوزيعاتُ عمدًا فتُظلَم الدعوى. والهيكلُ
    (سابقة·نواة·لاحقة) رمزٌ واحد، و«∄» رمزُ ما لم يُفرَد تحليلُه."""
    stream = Counter(); uncov = 0
    for sk in words:
        f = factorize(sk, prefixes, sufs)
        if len(f) == 1:
            p, t, root, s = f[0]
            stream[("A", (p, t, s))] += 1
            for c in root:
                stream[("ح", c)] += 1
        else:
            uncov += 1
            stream[("A", "∄")] += 1
            for c in sk:
                stream[("ح", c)] += 1
    n = sum(stream.values())
    ld = sum(-k * log2(k / n) for k in stream.values())
    tbl = tuple(p for p in prefixes if p) + tuple(sufs) + tuple(CORES)
    lm = sum((len(x) + 1) * log2(ALPHA) for x in tbl) + 3 * log2(50)
    return round(ld + lm), uncov


def baseline_bill(words):
    """الأساسُ بالصيغة نفسِها: كلُّ كلمةٍ «∄» وحروفُها — فالمقارنةُ عادلة."""
    s = Counter()
    for sk in words:
        s[("A", "∄")] += 1
        for c in sk:
            s[("ح", c)] += 1
    n = sum(s.values())
    return round(sum(-k * log2(k / n) for k in s.values()))


def main():
    verses = parse_verses(CORPUS)
    words = ["".join(c for c, _ in w) for v in verses for w in v]
    vocab = set(words)

    # ── T₁ تصديق ──
    stat = Counter(); mim = Counter(); dup = 0
    shape = Counter(); ex = []
    for sk in words:
        f = factorize(sk)
        if len(f) != len(set(f)):
            dup += 1
        if not f:
            stat["خارج-النطاق"] += 1
        elif len(f) == 1:
            stat["مفرد-منعكس"] += 1
            p, t, root, s = f[0]
            shape[(p, t, s)] += 1
            if p == "م":
                mim["ميم-بلا-منازع"] += 1
        else:
            stat["متنازع"] += 1
            if any(x[0] == "م" for x in f):
                mim["ميم-متنازع"] += 1
            if len(ex) < 6:
                ex.append((sk, f[:3]))

    # ── ④ كم من «المفرد المنعكس» لا تنسورَ فيه؟ ──
    no_tensor = sum(n for (p, t, s), n in shape.items() if p == "∅" and s == "∅")

    # ── ⑤ شاهدٌ مضادٌّ للميم من البايتات: الجذعُ قبل الضمير كلمةٌ مشهودة ──
    counter = Counter(); left = Counter()
    for sk in words:
        f = factorize(sk)
        if len(f) == 1 and f[0][0] == "م":
            w = None
            for s in SUF:
                if sk.endswith(s) and len(sk) - len(s) >= 2 and sk[:-len(s)] in vocab:
                    w = (sk[:-len(s)], s); break
            if w:
                counter[f"{sk} = {w[0]}+{w[1]}"] += 1
            else:
                left[sk] += 1

    # ── ② الحَكَم: فاتورةُ قانون الوديعة ──
    base = baseline_bill(words)
    rng = random.Random(0)
    variants = [
        ("التنسور كما هو", PREFIX, SUF),
        ("بلا سوابقَ (لواحقُ فقط)", ("",), SUF),
        ("بلا ميم", tuple(p for p in PREFIX if p != "م"), SUF),
        ("الميمُ وحدَها", ("م", ""), SUF),
        ("سوابقُ مختلقة (ض ظ غ ث)", ("ض", "ظ", "غ", "ث", ""), SUF),
        ("سوابقُ حروفٍ شائعة", ("ا", "ل", "و", "ب", "ف", "ي", ""), SUF),
    ]
    bills = {}
    for lab, p_, s_ in variants:
        tot, unc = tensor_bill(words, p_, s_)
        bills[lab] = dict(الكلّ=tot, فائدة=tot - base, غيرُ_مفرد=unc,
                          حكم="يُقبَل" if tot < base else "يُرفَض")
    mim_cost = bills["التنسور كما هو"]["الكلّ"] - bills["بلا ميم"]["الكلّ"]

    # ── المصادمةُ بفارق صفر ──
    assert stat["مفرد-منعكس"] == SEALED_TENSOR["مفرد"], stat
    assert stat["متنازع"] == SEALED_TENSOR["متنازع"], stat
    assert stat["خارج-النطاق"] == SEALED_TENSOR["خارج"], stat
    assert mim["ميم-بلا-منازع"] == SEALED_TENSOR["ميمٌ_بلا_منازع"], mim
    assert mim["ميم-متنازع"] == SEALED_TENSOR["ميمٌ_متنازع"], mim
    assert dup == SEALED_TENSOR["تحليلٌ_مكرَّر"], dup
    assert no_tensor == SEALED_TENSOR["بلا_تنسور"], no_tensor
    assert sum(counter.values()) == SEALED_TENSOR["شاهدٌ_مضادّ"], sum(counter.values())
    assert all(d["حكم"] == "يُرفَض" for d in bills.values()), bills

    R = dict(
        الدعوى="T = سابقة ⊗ وزن ⊗ لاحقة · مفردٌ منعكس = مقبول · متعددٌ = معلَّق · خارجُ النطاق معلن",
        T1_تصديق=dict(أحوال=dict(stat), الميم=dict(mim), تحليلٌ_مكرَّر=dup,
                      ملاحظة="الأرقامُ الخمسةُ تكرّرت بفارق صفر، ولا تضخُّمَ بتكرار تحليل"),
        T2_تفنيد=dict(
            الانعكاسُ_لا_يرفض=dict(
                سبب="expand(p,t,root,s) == word صحيحٌ بالبناء: p وs قُطعا من الكلمة وroot التُقط بالمطابقة",
                حكم="شرطُ «منعكس» تحصيلُ حاصل — الذي يفرز هو عددُ التحليلات لا انعكاسُها"),
            الفاتورةُ_ترفض=dict(أساس=base, جداول=bills,
                                حكم="التنسورُ يُرفَض في صوره كلِّها، ودون الأساس دائمًا"),
            جدولُ_السوابق_يضرّ=dict(
                ثمنُ_الميم=mim_cost,
                قراءة="إسقاطُ الميم يُحسِّن الفاتورة؛ وسوابقُ مختلقةٌ أرخصُ من الحقيقية"),
            المفردُ_بلا_تنسور=dict(
                عدد=no_tensor, من=stat["مفرد-منعكس"],
                نسبة=round(no_tensor / stat["مفرد-منعكس"], 4),
                هياكلُ_أعلى={f"{p}·{t}·{s}": n for (p, t, s), n in shape.most_common(6)},
                حكم="هيكلُها (∅·فعل·∅) — جذرٌ عارٍ لا تنسورَ فيه، فالرقمُ يعدّ ما لا يخصّ الدعوى"),
            الميمُ_لها_منازع=dict(
                بشاهدٍ_مضادّ=sum(counter.values()), من=mim["ميم-بلا-منازع"],
                مواضع=dict(counter.most_common(10)),
                سبب=("«من» و«مع» ليستا في PREFIX — فالسكوتُ عدمُ منازعٍ في الجدول لا في اللغة"),
                بلا_شاهد=dict(عدد=sum(left.values()), أعلى=dict(left.most_common(8)),
                              ملاحظة="فيه أعلامٌ ظاهرة (موسى · مريم) — تُسمّى ولا يُفتَح لها باب"))),
        الحكم=("صحيحةُ العدّ، مرفوضةُ الوديعة. ولا تُودَع حتى تُخفّض الفاتورة، ولا يُنقَل رقمُ "
               "«مفرد-منعكس» تغطيةً. وليس هذا ردًّا للتنسور مبدأً بل لهذا الجدول بهذه النوى: "
               "ثلاثُ نوًى لا تكفي، و«فعل» منها ثلاثةُ محارفَ حرّةٍ تطابق كلَّ ثلاثيّ"),
        أمثلة_المتنازع=ex)

    print("الدعوى:", R["الدعوى"])
    print(f"\n— T₁ تصديق —\n  {dict(stat)}\n  {dict(mim)} · تحليلٌ مكرَّر {dup} (فارقٌ صفر)")
    print("\n— T₂ تفنيد —")
    print("  ① الانعكاسُ لا يرفض: expand == word صحيحٌ بالبناء (كما في mirror.py)")
    print(f"  ② الفاتورة (الأساس {base:,}):")
    for k, d in bills.items():
        print(f"      {k:26s} الكلّ {d['الكلّ']:>11,} · Δ {d['فائدة']:>+9,} · {d['حكم']}")
    print(f"  ③ ثمنُ الميم: {mim_cost:+,} بت — إسقاطُها يُحسِّن الفاتورة")
    print(f"  ④ بلا تنسورٍ البتّة: {no_tensor:,}/{stat['مفرد-منعكس']:,} = "
          f"{no_tensor/stat['مفرد-منعكس']:.1%} هيكلُها (∅·فعل·∅)")
    print(f"  ⑤ «الميمُ بلا منازع» لها منازع: {sum(counter.values())}/{mim['ميم-بلا-منازع']} "
          f"بشاهدٍ من البايتات —", list(counter.most_common(4)))
    print(f"      والباقي {sum(left.values())} فيه أعلامٌ ظاهرة:", list(left.most_common(4)))
    print("\nالحكم:", R["الحكم"])
    return R


if __name__ == "__main__":
    R = main()
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump({"دعوى_التنسور": R}, open(p, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {p}")
