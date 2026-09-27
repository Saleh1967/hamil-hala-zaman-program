# field112_laws.py — دخولُ دفعةِ الحركات الحقلَ 112: قوانينُها مقيسةً بتقسيمنا نحن.
# الحقل: 28 حرفًا أساسيًّا × 4 حركات (فتحة/ضمة/كسرة/سكون) = 112 خلية — من algebra_engine بعينه،
# لا نسخةَ ثانية. والتفكيك بقاعدتين معلنتين موروثتين من parse_stream:
#   R5 الشدّة  ⟼ (حرفٌ ساكن) + (حرفٌ متحرّك)      · R4 التنوين ⟼ (حركة) + (نونٌ ساكنة)
#   والخنجرية (ٰ) فتحةٌ باتفاقٍ معلن (DAGGER في algebra_engine).
# **هامشُ الحقل مسمًّى لا مبتلَع**: ما خرج عن 112 يُعَدّ باسمه في موضعين اثنين لا غير —
#   ١) حرفٌ خارج الثمانية والعشرين: ى · ة · آ · ء · والهمزاتُ المحمولة أ · إ · ؤ · ئ.
#   ٢) عُرْيٌ: حالةٌ خارج الحركات الأربع — الحرفُ الرسميُّ غير المشكول، نعدّه عريًا حتى يُثبت حرفُه.
# والفرقُ عن parse_stream مسمًّى بعدده: تقاطعُ الشدّة والتنوين (R5 ثم R4 عندنا، وparse_stream
# يقف عند الشدّة) — يُعَدّ ولا يُدمَج بالكلام، ويُصادَم ما سواه بفارق صفر.
# القوانينُ الخمسة المقيسة: ص-بداية · ص-تصاق · هـ-كسرة⟵ضمة (حدُّ الاشتقاق iu) ·
#   د-وقف/وصل **داخل الحقل** (الهيئةُ الواحدة تسكن خليتين: سكونَ الوقف وحركةَ الوصل) ·
#   ح-حاكم بشرطيه المعلنين (كلُّ الصفوف ⟷ الهيئاتُ متبدّلةُ الخاتمة وحدها).
# ⚑ والمعجمُ والكلفةُ السابقة لا تُمسّ: هذا قياسُ قوانينَ داخل حقلٍ مرخَّصٍ سلفًا، لا تصنيفُ كلمات.
from collections import Counter, defaultdict
import argparse, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "induction"))
from algebra_engine import LETTERS, STATES, CP, DAGGER, parse_stream   # إطارُ 112 بعينه
from induction_engine import JARR, JPRE, AR                            # الجارُّ موروثٌ لا مسعَّرٌ ثانيةً
from harakat_layer import NASB, H, heldout_ce                          # سياسةُ القياس نفسُها (α=1، تناوب)

CORPUS = os.path.join(ROOT, "mujammad.txt")
SEAL = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"

BASE28 = LETTERS[:28]                       # الحروفُ الأساسية — بُعدُ الحقل الأول
HARAKAT4 = [s[0] for s in STATES[:4]]       # فتحة · ضمة · كسرة · سكون — بُعدُه الثاني
BARE = "عُرْي"                                # هامشُ الحالة المسمّى
FIELD5 = tuple(HARAKAT4) + (BARE,)          # حقلُ الخاتمة المغلق المعلن — m=5
M5 = len(FIELD5)
VOWELS3 = ("فتحة", "ضمة", "كسرة")
VOWM = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TANM = {0x064B: "فتحة", 0x064C: "ضمة", 0x064D: "كسرة"}   # R4: الحركةُ ثم النونُ الساكنة
SHADDA = 0x0651
LAM_AMR = ("ليقطع", "ليقضوا")               # استثناءُ ص-بداية، مسمًّى بعينه (موروثٌ بالاسم)

skel = lambda units: "".join(u[0] for u in units)


# ---------- ١) التفكيك إلى الحقل: وحداتٌ (حرف، حالة) بقاعدتين معلنتين ----------
def units(word):
    """كلمةٌ خامٌ ⟼ وحداتُ الحقل، كلُّ وحدةٍ (حرف، حالة، **منشأ**). R5 ثم R4 بهذا الترتيب المعلن،
    والخنجريةُ فتحة. والمنشأُ مرافقٌ لا زينة: به يُفصَل سكونُ الرسم عن سكونِ التوسيع، فلا يُحاسَب
    أحدُهما بحكم الآخر. ولا خلطَ بين التفكيك والتصنيف: الخلايا تُسنَد، والهامشُ يُسمّى، ولا موضعَ يُبتلَع."""
    out, i, n, shadda_tanwin = [], 0, len(word), 0
    while i < n:
        ch = word[i]
        if not AR(ch):
            i += 1
            continue
        marks = []
        while i + 1 < n and (0x064B <= ord(word[i + 1]) <= 0x0652 or ord(word[i + 1]) == DAGGER):
            i += 1
            marks.append(ord(word[i]))
        tan = next((m for m in marks if m in TANM), None)
        vow = next((m for m in marks if m in VOWM), None)
        st = VOWM[vow] if vow else TANM[tan] if tan else "فتحة" if DAGGER in marks else BARE
        if SHADDA in marks:                       # R5: ساكنٌ ثم متحرّك — الحرفُ نفسُه مرّتين
            out.append((ch, "سكون", "R5"))
            if tan:
                shadda_tanwin += 1
        out.append((ch, st, "R4" if tan and not vow else "رسم"))
        if tan:                                   # R4: النونُ الساكنة موضعٌ ثانٍ معدود
            out.append(("ن", "سكون", "R4"))
        i += 1
    return out, shadda_tanwin


def read_words(path):
    """المجمَّد بختمه ⟼ آياتٌ ⟼ كلماتٌ خام. العدُّ يُصالَح بـassert: 6,236 آيةً و77,801 كلمة."""
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == SEAL, "ليس المجمَّد — البصمة خُالفت"
    verses = []
    for ln in blob.decode("utf-8-sig").splitlines():
        if not ln.strip() or not any(AR(c) for c in ln):
            continue
        ws = [w for w in ln.split(" ") if any(AR(c) for c in w)]
        if ws:
            verses.append(ws)
    assert len(verses) == 6236, "بصمةُ الآيات خُالفت"
    assert sum(len(v) for v in verses) == 77801, "مصالحةُ الكلمات خُولفت — صريخ"
    return verses


def decompose(verses):
    """التفكيك مرّةً واحدة، ومعه مصادمةُ parse_stream على ما يسعه — بفارق صفرٍ محروس."""
    out, collided, differed = [], 0, 0
    for ws in verses:
        row = []
        for w in ws:
            u, st = units(w)
            row.append(u)
            if st:                                        # تقاطعُ الشدّة والتنوين: فرقٌ مسمًّى
                differed += 1
                continue
            if all(c in CP for c in w if AR(c)) and DAGGER not in [ord(c) for c in w]:
                ref = [(LETTERS[li], STATES[si][0]) for li, si in
                       parse_stream("".join(c for c in w if AR(c) or 0x064B <= ord(c) <= 0x0652))]
                ref = [(ch, BARE if st_ == "عُرْي" else st_) for ch, st_ in ref]
                assert ref == [(ch, st_) for ch, st_, _ in u], \
                    f"التفكيكُ خالف parse_stream على «{w}» — صريخ"
                collided += 1
        out.append(row)
    return out, collided, differed


def field_margin(verses112):
    """كلُّ وحدةٍ إمّا خليةٌ من 112 وإمّا هامشٌ مسمًّى — والمجموعُ يُصالَح بـassert."""
    inside, out_letter, out_state, both = 0, Counter(), Counter(), 0
    total = 0
    by_src = Counter()
    for row in verses112:
        for u in row:
            for ch, st, src in u:
                total += 1
                by_src[src] += 1
                lo, so = ch not in BASE28, st not in HARAKAT4
                if lo:
                    out_letter[ch] += 1
                if so:
                    out_state[st] += 1
                if lo and so:
                    both += 1
                if not lo and not so:
                    inside += 1
    assert inside + sum(out_letter.values()) + sum(out_state.values()) - both == total, \
        "مفقودٌ بين الحقل وهامشه — ابتلاع"
    return dict(units=total, inside_112=inside,
                by_origin={k: by_src[k] for k in ("رسم", "R5", "R4") if by_src[k]},
                margin_letter=dict(total=sum(out_letter.values()), by_letter=dict(out_letter.most_common()),
                                   name="حرفٌ خارج الثمانية والعشرين (منه الهمزاتُ المحمولة)"),
                margin_state=dict(total=sum(out_state.values()), name="عُرْي — حالةٌ خارج الحركات الأربع"),
                margin_both=both,
                verdict="الهامشُ مسمًّى ومعدود، والمجموعُ مصالَحٌ بـassert — لا ابتلاع")


# ---------- ٢) الحارسان الصوتيان داخل الحقل ----------
def guards(verses112):
    """ص-بداية · ص-تصاق: انتهاكاتٌ تُعَدّ بأعيانها، **وبمنشأ سكونها** لا بجنسه وحده.
    فالسكونُ هنا سكونُ الحقل بعد R5/R4، ولا يُحاسَب سكونُ التوسيع بحكم سكون الرسم."""
    init_rasm, init_r5, adjacent = Counter(), Counter(), Counter()
    for row in verses112:
        for u in row:
            if u[0][1] == "سكون":
                (init_r5 if u[0][2] == "R5" else init_rasm)[skel(u)] += 1
            for a, b in zip(u, u[1:]):
                if a[1] == "سكون" and b[1] == "سكون":
                    adjacent[f"{skel(u)} ({a[2]}+{b[2]})"] += 1
    return init_rasm, init_r5, adjacent


# ---------- ٣) حدُّ الاشتقاق iu: كسرة ⟵ ضمة داخل الكلمة ----------
def iu_boundary(verses112):
    """الانتقالُ (كسرة ⟵ ضمة) موضعًا موضعًا، مبوَّبًا بحامل الضمّة: و · ه (ضميرُ الغائب) · أخرى.
    حدُّ ترخيصٍ مقترحٌ لا حكمٌ اشتقاقيّ: الموضعُ معدود، والاسمُ مؤجَّلٌ إلى مرحلة الحدود."""
    total, by_carrier, by_pair, at_end = 0, Counter(), Counter(), 0
    for row in verses112:
        for u in row:
            for j, (a, b) in enumerate(zip(u, u[1:])):
                if a[1] == "كسرة" and b[1] == "ضمة":
                    total += 1
                    by_carrier[b[0]] += 1
                    by_pair[f"{a[0]}ِ{b[0]}ُ"] += 1
                    if j + 2 == len(u):
                        at_end += 1
    return dict(total=total, damma_is_ending=at_end,
                by_damma_carrier=[f"{k}×{v:,}" for k, v in by_carrier.most_common(8)],
                top_pairs=[f"{k}×{v:,}" for k, v in by_pair.most_common(10)],
                condition="وحدتان متجاورتان داخل الكلمة الواحدة: الأولى كسرةٌ والثانية ضمّة",
                verdict="موضعُ ترخيصٍ مقترحٌ لمرحلة الحدود — معدودٌ بشرطه، لا اسمَ اشتقاقيًّا عليه")


# ---------- ٤) «ق-وقف/وصل» داخل الحقل: الهيئةُ الواحدة في خليتين ----------
def is_wasl_head(u):
    """رأسُ الوصل: ألفٌ عاريةٌ في أوّل الكلمة — شرطٌ رسميٌّ معلن (موروثٌ بقاعدته لا برقمه)."""
    return u[0][0] == "ا" and u[0][1] == BARE


def waqf_wasl(verses112):
    """خاتمةُ الكلمة خليةً من الـ112 أو هامشًا مسمًّى. وسكونُ الخاتمة يُفصَل بمنشئه:
    سكونُ الرسم ⟷ نونُ R4 — وبه تُصالَح خانةُ التنوين عند مَن لا يوسّعها، بفارق صفر."""
    sukun, haraka, bare = Counter(), Counter(), Counter()
    by_state = defaultdict(Counter)
    end_src, states_all = Counter(), Counter()
    before_alef_all = 0
    before_alef_both = Counter()
    for row in verses112:
        for i, u in enumerate(row):
            s, e = skel(u), u[-1][1]
            nxt_wasl = i + 1 < len(row) and is_wasl_head(row[i + 1])
            if e == "سكون":
                sukun[s] += 1
                end_src[u[-1][2]] += 1
            elif e in VOWELS3:
                haraka[s] += 1
                states_all[e] += 1
                by_state[s][e] += 1
                if nxt_wasl:
                    before_alef_all += 1
                    before_alef_both[s] += 1
            else:
                bare[s] += 1
    both = sorted(set(sukun) & set(haraka), key=lambda s: (-(sukun[s] + haraka[s]), s))
    states_both = Counter()
    for s in both:
        states_both.update(by_state[s])
    return dict(
        forms_two_cells=len(both),
        sukun_sites=sum(sukun[s] for s in both),
        haraka_sites=sum(haraka[s] for s in both),
        haraka_states={k: states_both[k] for k in VOWELS3},
        wasl_context_before_bare_alef=sum(before_alef_both[s] for s in both),
        all_endings=dict(sukun=sum(sukun.values()), haraka=sum(haraka.values()),
                         bare=sum(bare.values()),
                         sukun_by_origin={k: end_src[k] for k in ("رسم", "R4") if end_src[k]},
                         haraka_states={k: states_all[k] for k in VOWELS3},
                         before_bare_alef=before_alef_all),
        top=[f"{s}: سكون {sukun[s]:,} · حركة {haraka[s]:,}" for s in both[:20]],
        condition="خليةُ الوقف = (حرف، سكون) · خليةُ الوصل = (حرف، حركة) — كلتاهما من الـ112 · "
                  "وسياقُ الوصل: تاليتُها تبدأ بألفٍ عارية",
        verdict="ثنائيةُ الوقف/الوصل داخليةُ الحقل: الهيئةُ الواحدة تسكن خليتين، لا خليةً وخارجًا",
    )


# ---------- ٥) ح-حاكم بشرطيه المعلنين ----------
def governor(u):
    s = skel(u)
    if s in JARR or (u[0][0] in JPRE and u[0][1] == "كسرة"):
        return "جار"
    if s in NASB:
        return "إنّ/أنّ"
    return "أخرى"


def governor_bridge(verses112):
    """شرطان لا يُدمجان: (أ) كلُّ الصفوف — متوسطُ القدرة على العموم؛
    (ب) الهيئاتُ متبدّلةُ الخاتمة وحدها — القدرةُ على الحالات الصعبة. والقياسُ خارج العيّنة m=5."""
    sup = defaultdict(set)
    for row in verses112:
        for u in row:
            sup[skel(u)].add(u[-1][1])
    rows, hard = [], []
    dist = defaultdict(Counter)
    for row in verses112:
        for i, u in enumerate(row):
            if i == 0:
                continue
            g, e = governor(row[i - 1]), u[-1][1]
            rows.append((g, e))
            dist[g][e] += 1
            if len(sup[skel(u)]) >= 2:
                hard.append((g, e))
    base = H(Counter(e for _, e in rows))
    a0, a1 = heldout_ce(rows, None, M5), heldout_ce(rows, 0, M5)
    b0, b1 = heldout_ce(hard, None, M5), heldout_ce(hard, 0, M5)
    return dict(
        field=list(FIELD5), m=M5, H_end=round(base, 4),
        condition_a=dict(name="كلُّ الصفوف — متوسطُ القدرة على العموم", n=len(rows),
                         heldout_no_cond=round(a0, 4), heldout_cond=round(a1, 4),
                         heldout_gain=round(a0 - a1, 4), gain_bits_total=round((a0 - a1) * len(rows), 1)),
        condition_b=dict(name="الهيئاتُ متبدّلةُ الخاتمة وحدها — القدرةُ على الحالات الصعبة", n=len(hard),
                         heldout_no_cond=round(b0, 4), heldout_cond=round(b1, 4),
                         heldout_gain=round(b0 - b1, 4), gain_bits_total=round((b0 - b1) * len(hard), 1)),
        distribution={g: {k: c[k] for k in FIELD5 if c[k]} for g, c in sorted(dist.items())},
        verdict="شرطان مختلفان واتجاهٌ واحد — لا يُنقَل رقمٌ بلا وسم شرطه",
    )


# ---------- التشغيل ----------
def run(path=CORPUS):
    verses = read_words(path)
    v112, collided, differed = decompose(verses)
    margin = field_margin(v112)
    init_rasm, init_r5, adjacent = guards(v112)
    D = waqf_wasl(v112)
    IU = iu_boundary(v112)
    G = governor_bridge(v112)
    named = ["R5 الشدّة", "R4 التنوين", "الخنجرية فتحة", "هامش الحرف", "هامش الحالة (عُرْي)",
             "ص-بداية", "ص-تصاق", "استثناء لام الأمر", "إدغامٌ عابرٌ للحدّ", "خلية الوقف (سكون)",
             "خلية الوصل (حركة)", "رأس الوصل (ألف عارية)", "حدّ الاشتقاق iu"]
    R = dict(
        seals=dict(mujammad_sha256_prefix="8b387ea8", verses=len(verses),
                   words=sum(len(v) for v in verses),
                   field=dict(letters=len(BASE28), states=len(HARAKAT4),
                              cells=len(BASE28) * len(HARAKAT4))),
        decomposition=dict(collided_with_parse_stream=collided,
                           shadda_tanwin_words=differed,
                           note="تقاطعُ الشدّة والتنوين: R5 ثم R4 عندنا وparse_stream يقف عند الشدّة — "
                                "فرقٌ مسمًّى معدود، وما سواه مصادَمٌ بفارق صفر",
                           **margin),
        guards=dict(initial_sukun_rasm=dict(total=sum(init_rasm.values()), by_form=dict(init_rasm),
                                            exception="لام الأمر — مسمّاةٌ بعينها، لا تعميم"),
                    initial_sukun_r5=dict(total=sum(init_r5.values()), forms=len(init_r5),
                                          top=[f"{k}×{v:,}" for k, v in init_r5.most_common(8)],
                                          name="إدغامٌ عابرٌ للحدّ: شدّةٌ في أوّل الكلمة",
                                          verdict="ساكنُ R5 هنا **خاتمةُ الكلمة السابقة رسمًا** لا بدايةُ "
                                                  "هذه — الحارسُ يقوم بفصل المنشأ، ولا يُبتلَع ولا يُلغى"),
                    adjacent_sukun=dict(total=sum(adjacent.values()), forms=len(adjacent),
                                        top=[f"{k}×{v:,}" for k, v in adjacent.most_common(10)]),
                    verdict="assertان مقترحان لأيّ محرّكٍ قادم — الانتهاكُ يُسمّى بمنشئه أو يصرخ"),
        waqf_wasl_in_field=D,
        iu_boundary=IU,
        governor_bridge=G,
        cost_bits=len(named) * 8 * 4,   # المسمَّى وحده يُسعَّر؛ الجارُّ وإنّ/أنّ موروثان فلا يُسعَّران ثانيةً
    )
    assert set(init_rasm) == set(LAM_AMR) and sum(init_rasm.values()) == 2, \
        f"ص-بداية (سكونُ الرسم) خُولف خارج لام الأمر: {dict(init_rasm)} — صريخ"
    assert sum(adjacent.values()) == 0, f"ص-تصاق خُولف داخل الحقل: {dict(adjacent)} — صريخ"
    assert margin["inside_112"] + margin["margin_state"]["total"] \
        + margin["margin_letter"]["total"] - margin["margin_both"] == margin["units"], \
        "مصالحةُ الحقل وهامشه خُولفت — صريخ"
    E = D["all_endings"]
    assert E["sukun"] + E["haraka"] + E["bare"] == R["seals"]["words"], \
        "مصالحةُ الخواتم خُولفت — صريخ"
    return R


def main(argv=None):
    ap = argparse.ArgumentParser(description="قوانينُ دفعة الحركات مقيسةً داخل الحقل 112")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    R = run()
    S, C, g, D, IU, G = (R["seals"], R["decomposition"], R["guards"],
                         R["waqf_wasl_in_field"], R["iu_boundary"], R["governor_bridge"])
    print(f"الحقل {S['field']['cells']} = {S['field']['letters']}×{S['field']['states']} على "
          f"{S['words']:,} كلمةً في {S['verses']:,} آية · وحداتٌ {C['units']:,} منها داخل الحقل "
          f"{C['inside_112']:,} · هامشُ الحرف {C['margin_letter']['total']:,} "
          f"({' · '.join(f'{k}×{v:,}' for k, v in list(C['margin_letter']['by_letter'].items())[:4])}…) · "
          f"هامشُ الحالة (عُرْي) {C['margin_state']['total']:,} — {C['verdict']}")
    print(f"مصادمةُ التفكيك: {C['collided_with_parse_stream']:,} كلمةً بفارق صفرٍ مع parse_stream · "
          f"تقاطعُ الشدّة والتنوين {C['shadda_tanwin_words']:,} كلمةً — فرقٌ مسمًّى لا مدموج")
    print(f"الحارسان داخل الحقل: ص-بداية بسكونِ الرسم {g['initial_sukun_rasm']['total']} "
          f"({' · '.join(g['initial_sukun_rasm']['by_form'])} — لام الأمر بالاسم) · "
          f"وبسكونِ R5 {g['initial_sukun_r5']['total']:,} في {g['initial_sukun_r5']['forms']:,} هيئة "
          f"({' · '.join(g['initial_sukun_r5']['top'][:4])}…) — {g['initial_sukun_r5']['verdict']}")
    print(f"    ص-تصاق: {g['adjacent_sukun']['total']:,} موضعًا في "
          f"{g['adjacent_sukun']['forms']:,} هيئة"
          + (f" ({' · '.join(g['adjacent_sukun']['top'][:3])}…)"
             if g["adjacent_sukun"]["total"] else "") + f" — {g['verdict']}")
    print(f"ق-وقف/وصل داخل الحقل: {D['forms_two_cells']:,} هيئةً في خليتين · سكونُ الوقف "
          f"{D['sukun_sites']:,} · حركةُ الوصل {D['haraka_sites']:,} ("
          + " · ".join(f"{k}={D['haraka_states'][k]:,}" for k in D["haraka_states"])
          + f") · منها قبل ألفٍ عارية {D['wasl_context_before_bare_alef']:,} — {D['verdict']}")
    print(f"    خواتمُ الكلمات كلِّها: سكون {D['all_endings']['sukun']:,} (رسمًا "
          f"{D['all_endings']['sukun_by_origin'].get('رسم', 0):,} · نونُ R4 "
          f"{D['all_endings']['sukun_by_origin'].get('R4', 0):,}) · حركة "
          f"{D['all_endings']['haraka']:,} · عُرْي {D['all_endings']['bare']:,} — "
          f"الحرفُ غير المشكول عريٌّ عندنا حتى يُثبت حرفُه، ولا يُدمَج بسكونٍ صرفيّ")
    print(f"حدُّ الاشتقاق iu (كسرة ⟵ ضمة): {IU['total']:,} موضعًا — منها الضمّةُ خاتمةُ الكلمة "
          f"{IU['damma_is_ending']:,} · حاملُ الضمّة: " + " · ".join(IU["by_damma_carrier"][:5])
          + f" — {IU['verdict']}")
    A, B = G["condition_a"], G["condition_b"]
    print(f"ح-حاكم على حقلٍ مغلقٍ m={G['m']} (H={G['H_end']}): (أ) {A['name']} = "
          f"{A['heldout_no_cond']} ⟵ {A['heldout_cond']} = ربحٌ {A['heldout_gain']} بت/كلمة "
          f"({A['gain_bits_total']:,.0f} بتًّا على {A['n']:,}) · (ب) {B['name']} = "
          f"{B['heldout_no_cond']} ⟵ {B['heldout_cond']} = ربحٌ {B['heldout_gain']} بت/كلمة "
          f"({B['gain_bits_total']:,.0f} بتًّا على {B['n']:,}) — {G['verdict']}")
    jar, inna = G["distribution"].get("جار", {}), G["distribution"].get("إنّ/أنّ", {})
    print(f"    الاتجاهُ معدودٌ لا مستعار: بعد الجارّ كسرة {jar.get('كسرة', 0):,} · "
          f"بعد إنّ/أنّ فتحة {inna.get('فتحة', 0):,} (ضمة {inna.get('ضمة', 0):,})")
    print(f"كلفةُ الطبقة معلنة: {R['cost_bits']} بت — ⚑ والمعجمُ والكلفةُ السابقة لم تُمسّ")
    if a.json:
        json.dump({"الحقل112_قوانين_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
