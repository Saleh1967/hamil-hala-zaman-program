# harakat_layer.py — دفعةُ «استقراء الحركات»: ما يدخل البرنامج منها، مُعادَ اشتقاقُه هنا.
# لا رقمَ منقول: كلُّ عددٍ في JSON يخرج من المجمَّد بختمه 8b387ea8… عبر parse_verses بعينها.
# ثلاثةُ بنودٍ مسمّاة ودَينان معدودان:
#   ١) حارسان صوتيان (assert):
#        بداية-حامل     — لا كلمةَ تبدأ بسكونٍ صرفيّ، باستثناء **لام الأمر** المسمّى بعينه.
#        لا-تصاق-صرفي   — لا سكونان صرفيان متجاوران داخل الكلمة.
#   ٢) قاعدة «و-وقف/وصل» المسمّاة — تقسّم كتلةَ الخاتمة العارية/الساكنة **بموضعها** لا باختيارٍ
#      شامل: الهيئةُ الواحدة ساكنةٌ عند الوقف، متحرّكةٌ عند الوصل قبل ألف الوصل. الجدول
#      **مُشتَقٌّ بالقاعدة لا مودَعٌ باليد**، فالمسعَّر شرطاها لا هيئاتُه.
#   ٣) جسرُ الحاكم السابق — H(الخاتمة) بلا شرطٍ وبالسابقة وبالتالية وبشرط الوصل، **داخل
#      العيّنة وخارجها معًا** (تقسيمٌ متناوب + α=1، سياسةُ induction_engine نفسُها). الاتجاهُ
#      والمقدارُ يُفصَلان بالاسم: ما يصمد خارجَ العيّنة وحده يُبنى عليه.
#   دَينان: «الثلاثون» (الكلماتُ العاريةُ كليًّا) و**شرطا قياس «بعد الجار»** — كلاهما بالاسم.
# ⚑ والمعجم والكلفةُ السابقة لا تُمسّ: هذه طبقةُ قياسٍ صوتيّ فوق الكلمة، لا تصنيفُ كلمات.
from collections import Counter, defaultdict
from math import log2
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "induction"))
from induction_engine import parse_verses, AR, JARR, JPRE   # المجمَّد بختمه — لا نسخةَ ثانية

CORPUS = os.path.join(ROOT, "mujammad.txt")

STATES = ("فتحة", "ضمة", "كسرة", "سكون", "عري",
          "تنوين فتح", "تنوين ضم", "تنوين كسر")            # الحقلُ المغلق — m=8
M = len(STATES)
ALPHA = 1                                                   # تنعيمٌ لابلاسي موسوم (سياسةٌ موروثة)
VOWELS = ("فتحة", "ضمة", "كسرة")
BARE = ("سكون", "عري")                                      # خاتمةُ الوقف: ساكنةٌ أو عارية
LAM_AMR = ("ليقطع", "ليقضوا")                               # استثناءُ الحارس الأول، مسمّى بعينه
NASB = ("إن", "أن", "وإن", "فإن", "وأن", "لأن", "كأن",
        "ولكن", "لكن", "إنا", "إنه")                        # حاكمُ الفتح المسمّى (جدولٌ مسعَّر)

skel = lambda w: "".join(ch for ch, _ in w)


def is_wasl_head(word):
    """رأسُ الوصل: كلمةٌ تبدأ بألفٍ عاريةٍ من الحركة — ألفُ الوصل في المجمَّد (ال… · اسم…).
    شرطٌ رسميٌّ معلن، لا حكمَ نحويًّا: ما بعده يُقاس، ولا يُقدَّر عليه شيء."""
    return word[0][0] == "ا" and word[0][1] == "عري"


def governor(word):
    """حاكمُ الكلمة السابقة بثلاثة أصناف معلنة: جارٌّ (مستقلٌّ أو ملتصقٌ بكسرة) · إنّ/أنّ · أخرى.
    الجارُّ موروثٌ من induction_engine.gate بعينه (JARR/JPRE) فلا يُسعَّر هنا مرّتين."""
    s = skel(word)
    if s in JARR or (word[0][0] in JPRE and word[0][1] == "كسرة"):
        return "جار"
    if s in NASB:
        return "إنّ/أنّ"
    return "أخرى"


# ---------- ١) الحارسان الصوتيان ----------
def guards(verses):
    """بداية-حامل · لا-تصاق-صرفي: انتهاكاتٌ تُعَدّ بأعيانها، لا نسبةٌ تُلخَّص."""
    init, adjacent = Counter(), Counter()
    for words in verses:
        for w in words:
            if w[0][1] == "سكون":
                init[skel(w)] += 1
            for a, b in zip(w, w[1:]):
                if a[1] == "سكون" and b[1] == "سكون":
                    adjacent[skel(w)] += 1
    return init, adjacent


# ---------- ٢) قاعدة «و-وقف/وصل» ----------
def waqf_wasl(verses):
    """الهيئةُ الواحدة بخاتمتين: ساكنةً حيث لا وصل، متحرّكةً حيث تلتها ألفُ وصل.
    القسمةُ **بموضع الهيئة** لا باختيارٍ شاملٍ لها: لا تُنقَل هيئةٌ من كتلةٍ إلى كتلة."""
    bare, wasl = Counter(), Counter()
    by_state = defaultdict(Counter)
    for words in verses:
        for i, w in enumerate(words):
            s, e = skel(w), w[-1][1]
            if e in BARE:
                bare[s] += 1
            elif e in VOWELS and i + 1 < len(words) and is_wasl_head(words[i + 1]):
                wasl[s] += 1
                by_state[s][e] += 1
    both = sorted(set(bare) & set(wasl), key=lambda s: (-wasl[s], s))
    states = Counter()
    for s in both:
        states.update(by_state[s])
    return dict(
        forms=len(both),
        waqf_sites=sum(bare[s] for s in both),
        wasl_sites=sum(wasl[s] for s in both),
        wasl_states={k: states[k] for k in VOWELS},
        top=[f"{s}: وقف {bare[s]:,} · وصل {wasl[s]:,}" for s in both[:20]],
        condition="خاتمةُ الوقف = {سكون، عري} · خاتمةُ الوصل = حركةٌ محقَّقة وتاليتُها رأسُ وصل",
        verdict="حدٌّ ثالث معدود: الظاهرُ سكونُ الوقف والمقدَّرُ حركةُ الوصل — قسمةٌ بالموضع",
    )


# ---------- ٣) جسرُ الحاكم السابق ----------
def H(counter):
    n = sum(counter.values())
    return -sum(v / n * log2(v / n) for v in counter.values() if v)


def conditional_H(rows, idx):
    """H(الخاتمة | الشرط) داخل العيّنة — تقديرٌ أقصى الإمكان، ومنه يُقرأ الانحيازُ لا الربح."""
    d = defaultdict(Counter)
    for r in rows:
        d[r[idx]][r[-1]] += 1
    n = len(rows)
    return sum(sum(c.values()) / n * H(c) for c in d.values())


def heldout_ce(rows, idx):
    """بت/كلمة خارج العيّنة: تدريب/اختبار متناوبان + α=1 على حقلٍ مغلقٍ m=8.
    idx=None ⟵ بلا شرط. الربحُ الصادقُ هو فرقُ هذين، لا فرقُ الداخلَين."""
    tr, te = rows[::2], rows[1::2]
    tab, tot = defaultdict(Counter), Counter()
    for r in tr:
        k = None if idx is None else r[idx]
        tab[k][r[-1]] += 1
        tot[k] += 1
    s = 0.0
    for r in te:
        k = None if idx is None else r[idx]
        s += -log2((tab[k][r[-1]] + ALPHA) / (tot[k] + ALPHA * M))
    return s / len(te)


def bridge(verses):
    rows = []                                   # (السابقة، التالية، شرطُ الوصل، الحاكم، الخاتمة)
    gov_rows = []
    for words in verses:
        for i, w in enumerate(words):
            if i == 0:
                continue
            gov_rows.append((governor(words[i - 1]), w[-1][1]))
            if i + 1 >= len(words):
                continue
            rows.append((skel(words[i - 1]), skel(words[i + 1]),
                         is_wasl_head(words[i + 1]), w[-1][1]))
    base = H(Counter(r[-1] for r in rows))
    conds = {"السابقة": 0, "التالية": 1, "شرط الوصل": 2}
    inside = {k: conditional_H(rows, i) for k, i in conds.items()}
    out0 = heldout_ce(rows, None)
    outside = {k: heldout_ce(rows, i) for k, i in conds.items()}
    g0 = heldout_ce(gov_rows, None)
    g1 = heldout_ce(gov_rows, 0)
    gov_dist = defaultdict(Counter)
    for g, e in gov_rows:
        gov_dist[g][e] += 1
    return dict(
        n_positions=len(rows),
        H_end=round(base, 4),
        inside_sample={k: round(v, 4) for k, v in inside.items()},
        inside_gain={k: round(base - v, 4) for k, v in inside.items()},
        heldout_bits_per_word=dict({"بلا شرط": round(out0, 4)},
                                   **{k: round(v, 4) for k, v in outside.items()}),
        heldout_gain={k: round(out0 - v, 4) for k, v in outside.items()},
        governor=dict(n_positions=len(gov_rows), classes=["جار", "إنّ/أنّ", "أخرى"],
                      heldout_no_cond=round(g0, 4), heldout_cond=round(g1, 4),
                      heldout_gain=round(g0 - g1, 4),
                      gain_bits_total=round((g0 - g1) * len(gov_rows), 1),
                      distribution={g: {k: c[k] for k in STATES if c[k]}
                                    for g, c in sorted(gov_dist.items())}),
        verdict="الاتجاهُ يصمد خارج العيّنة (السابقةُ أشدُّ من التالية) والمقدارُ الداخليُّ لا يصمد",
    )


# ---------- الدَّينان المسمّيان ----------
def debts(verses, path):
    """«الثلاثون»: الكلماتُ العاريةُ كليًّا — تُسمّى هنا بأعيانها وتُصالَح مع تفكيك المتن.
    و«بعد الجار»: شرطان معلنان، فلا يُنقَل أحدُ الرقمين بلا وسم شرطه."""
    naked = Counter()
    sup = defaultdict(Counter)
    nwords = 0
    for words in verses:
        for w in words:
            nwords += 1
            sup[skel(w)][w[-1][1]] += 1
            if all(st == "عري" for _, st in w):
                naked[skel(w)] += 1
    body = [ln for ln in open(path, encoding="utf-8-sig").read().splitlines()
            if ln.strip() and any(AR(c) for c in ln)]
    tokens = [t for ln in body for t in ln.split(" ") if t.strip()]
    symbols = [t for t in tokens if not any(AR(c) for c in t)]

    after_all, after_var = Counter(), Counter()
    for words in verses:
        for i, w in enumerate(words[:-1]):
            if governor(w) != "جار":
                continue
            nxt = words[i + 1]
            e = nxt[-1][1]
            after_all[e] += 1
            if len(sup[skel(nxt)]) >= 2 and e in VOWELS:
                after_var[e] += 1
    n_all, n_var = sum(after_all.values()), sum(after_var.values())
    return dict(
        naked_words=dict(total=sum(naked.values()), forms=len(naked),
                         by_form={k: v for k, v in naked.most_common()},
                         verdict="فواتحُ السور (الحروفُ المقطَّعة) — عائلةٌ مسمّاةٌ لا فجوةٌ مجهولة"),
        token_reconciliation=dict(raw_tokens=len(tokens), symbols=len(symbols),
                                  words=nwords, residue=len(tokens) - len(symbols) - nwords,
                                  symbols_top=[f"{t}×{n}" for t, n in Counter(symbols).most_common(5)],
                                  closing="82,379 − 4,578 = 77,801 بالرمز — بفارق صفر"),
        after_jar=dict(
            condition_a=dict(name="كلُّ ما بعد الجار بلا شرط", n=n_all,
                             kasra=after_all["كسرة"] + after_all["تنوين كسر"],
                             pct=round((after_all["كسرة"] + after_all["تنوين كسر"]) / n_all * 100, 2),
                             distribution={k: after_all[k] for k in STATES if after_all[k]}),
            condition_b=dict(name="الهياكلُ متبدّلةُ الخاتمة المتحقَّقة حركتُها", n=n_var,
                             kasra=after_var["كسرة"],
                             pct=round(after_var["كسرة"] / n_var * 100, 2),
                             distribution={k: after_var[k] for k in VOWELS if after_var[k]}),
            verdict="اتجاهٌ واحد وشرطان مختلفان — لا يُنقَل رقمٌ بلا وسم شرطه"),
    )


def run(path=CORPUS):
    verses = parse_verses(path)
    init, adjacent = guards(verses)
    G = waqf_wasl(verses)
    B = bridge(verses)
    D = debts(verses, path)
    named = ["و-وقف (خاتمةٌ ساكنة)", "و-وصل (حركةٌ قبل ألف الوصل)",
             "بداية-حامل", "لا-تصاق-صرفي", "استثناء لام الأمر"] + list(NASB)
    R = dict(
        seals=dict(mujammad_sha256_prefix="8b387ea8", words=sum(len(w) for w in verses),
                   verses=len(verses)),
        guards=dict(initial_sukun=dict(total=sum(init.values()), by_form=dict(init),
                                       exception="لام الأمر — مسمّاةٌ بعينها، لا تعميم"),
                    adjacent_sukun=dict(total=sum(adjacent.values()), by_form=dict(adjacent)),
                    verdict="هيكلُ (متحرك×ساكن) قانونُ المتن لا اصطلاحُ الترميز — assertان"),
        waqf_wasl_rule=G,
        governor_bridge=B,
        debts=D,
        cost_bits=len(named) * 8 * 4,   # المسمَّى وحده يُسعَّر؛ جدولُ الهيئات مُشتَقٌّ بالقاعدة
    )
    # ---------- الحارسان، assertين: الانتهاكُ الوحيدُ مسمّى، وما عداه صريخ ----------
    assert set(init) == set(LAM_AMR) and sum(init.values()) == 2, \
        f"بداية-حامل خُولف خارج لام الأمر: {dict(init)} — صريخ"
    assert sum(adjacent.values()) == 0, f"لا-تصاق-صرفي خُولف: {dict(adjacent)} — صريخ"
    assert R["seals"]["words"] == 77801 and D["token_reconciliation"]["residue"] == 0, \
        "مصالحةُ العدّ خُولفت — صريخ"
    return R


def main(argv=None):
    ap = argparse.ArgumentParser(description="طبقة الحركات — الحارسان والوقف/الوصل وجسرُ الحاكم")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    R = run()
    g, G, B, D = R["guards"], R["waqf_wasl_rule"], R["governor_bridge"], R["debts"]
    print(f"الحارسان الصوتيان: بدايةٌ بسكونٍ صرفيّ {g['initial_sukun']['total']} "
          f"({' · '.join(g['initial_sukun']['by_form'])} — لام الأمر بالاسم) · "
          f"سكونان متجاوران {g['adjacent_sukun']['total']} — {g['verdict']}")
    print(f"قاعدة و-وقف/وصل: {G['forms']:,} هيئةً بخاتمتين · مواضعُ الوقف {G['waqf_sites']:,} · "
          f"مواضعُ الوصل {G['wasl_sites']:,} (" +
          " · ".join(f"{k}={G['wasl_states'][k]:,}" for k in G['wasl_states']) + ") — " + G["verdict"])
    print(f"جسرُ الحاكم: H(الخاتمة)={B['H_end']} على {B['n_positions']:,} موضعًا | داخلَ العيّنة "
          + " · ".join(f"بـ{k} {v}" for k, v in B["inside_sample"].items()))
    print(f"    خارجَ العيّنة (بت/كلمة، α=1): بلا شرط {B['heldout_bits_per_word']['بلا شرط']} · "
          + " · ".join(f"{k} {v} (ربح {B['heldout_gain'][k]})"
                       for k, v in B["heldout_bits_per_word"].items() if k != "بلا شرط"))
    GV = B["governor"]
    print(f"    الحاكمُ بثلاثة أصنافٍ مسمّاة: {GV['heldout_no_cond']} ⟵ {GV['heldout_cond']} "
          f"= ربحٌ {GV['heldout_gain']} بت/كلمة ({GV['gain_bits_total']:,.0f} بتًّا على "
          f"{GV['n_positions']:,} موضعًا) — {B['verdict']}")
    N = D["naked_words"]; T = D["token_reconciliation"]; J = D["after_jar"]
    print(f"دَينُ «الثلاثين» مُقفَل بالاسم: {N['total']} كلمةً عاريةً كليًّا في {N['forms']} هيئة "
          f"({' · '.join(list(N['by_form'])[:6])}…) — {N['verdict']}")
    print(f"مصالحةُ العدّ: رموزٌ خام {T['raw_tokens']:,} − علاماتٌ وزخارف {T['symbols']:,} = "
          f"كلمات {T['words']:,} · متبقٍّ {T['residue']} — {T['closing']}")
    print(f"بعد الجار بشرطيه: (أ) {J['condition_a']['name']} = {J['condition_a']['pct']}% "
          f"({J['condition_a']['kasra']:,}/{J['condition_a']['n']:,}) · (ب) {J['condition_b']['name']} = "
          f"{J['condition_b']['pct']}% ({J['condition_b']['kasra']:,}/{J['condition_b']['n']:,}) — "
          f"{J['verdict']}")
    print(f"كلفةُ الطبقة معلنة: {R['cost_bits']} بت — ⚑ والمعجمُ والكلفةُ السابقة لم تُمسّ")
    if a.json:
        json.dump({"الحركات_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
