# awzan_engine.py — حلقة الأوزان: فكُّ المعلَّق (ث+ع) بقوالب I–XV المودَعة في algebra_engine نفسه.
# الانضباط: القوالب تُقرأ من T في algebra_engine — مصدرُ حقيقةٍ واحد، لا نسخةَ ثانيةٍ تتخلّف.
# كل مطابقةٍ بقاعدةٍ مسمّاة وطبقةٍ معلنة، وكلُّ خطأٍ معدودٌ معروضٌ لا مُقدَّرٌ بالكلام:
#   و١-حرفي     : الحروفُ والحركاتُ والشدّةُ كلُّها مطابقة — لا تحرير.
#   و٢-خاتمة    : موضعُ الخاتمة (محلُّ الإعراب) حرٌّ، وما قبله حرفيّ.
#   و٣-قلع      : قلعُ السوابق المعلنة (و/ف بفتحة · ب/ل/ك بكسرة · ال) ثم و٢.
# الخطآن المعلنان:
#   موجب الصدفة : مطابَقةٌ هيكلُها يَرِدُ في المجمَّد معرَّفًا بـ«ال» ⟹ اسمٌ على هيئة وزن (حدٌّ أعلى معدود).
#   سالب الضعف  : فرقُ المطابقات عند تسوية الهمزات والألفات المعلنة (أ/إ/آ ⟵ ا · ى ⟵ ا) — معدودٌ لا مقدَّر.
from collections import Counter, defaultdict
import json, os, sys, argparse

_INDUCTION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "induction")
assert os.path.isfile(os.path.join(_INDUCTION, "induction_engine.py")), \
    "محرّك الاستقراء غائبٌ عن induction/ — لا استيراد صامت"
sys.path.insert(0, _INDUCTION)
from induction_engine import parse_verses, VOW, TAN, AR       # التحليل الموروث بعينه
from algebra_engine import T                                   # القوالب I–XV بلا نسخ

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
SHADDA = 0x0651
SLOTS = set("فعل")                                # مواضع الجذر في القالب
HAMZ = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ا"}   # تسوية معلنة تُقاس ولا تُفرض
PREFIX = {("و", "فتحة"), ("ف", "فتحة"), ("ب", "كسرة"), ("ل", "كسرة"), ("ك", "كسرة"), ("ل", "فتحة")}
LAYERS = ("و١-حرفي", "و٢-خاتمة", "و٣-قلع")
ORDER = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
assert sorted(ORDER) == sorted(T), "قوالب algebra_engine خُولفت — صريخ"


def tokenize_word(w):
    """كتحليل induction بعينه، والشدّةُ محفوظةٌ زيادةً: (حرف، حالة، مشدّد)."""
    pos, i, n = [], 0, len(w)
    while i < n:
        if AR(w[i]):
            ch, marks = w[i], []
            while i + 1 < n and (0x064B <= ord(w[i + 1]) <= 0x0652 or ord(w[i + 1]) == 0x0670):
                i += 1
                marks.append(ord(w[i]))
            vs = [m for m in marks if m in VOW]
            ts = [m for m in marks if m in TAN]
            st = TAN[ts[0]] if ts else VOW[vs[0]] if vs else "فتحة" if 0x0670 in marks else "عري"
            pos.append((ch, st, SHADDA in marks))
        i += 1
    return pos


def tokenize_rich(path=CORPUS, verses=None):
    """التحليل الغنيّ + البوّابة: نزعُ الشدّة يعيد مخرَج parse_verses بفارق صفر أو صريخ."""
    blob = open(path, "rb").read().decode("utf-8-sig")
    rich = []
    for ln in blob.splitlines():
        if not ln.strip() or not any(AR(c) for c in ln):
            continue
        ws = [p for p in (tokenize_word(w) for w in ln.split(" ")) if p]
        if ws:
            rich.append(ws)
    base = parse_verses(path) if verses is None else verses
    assert len(base) == len(rich), "عدد الآيات اختلف بين التحليلين — صريخ"
    for va, vb in zip(base, rich):
        assert len(va) == len(vb) and all(wa == [(c, s) for c, s, _ in wb] for wa, wb in zip(va, vb)), \
            "التحليل الغنيّ خالف parse_verses — لا مطابقة على بايتاتٍ متخلّفة"
    return rich


TMPL = {n: tokenize_word(t) for n, t in T.items()}
assert [c for c, _, _ in TMPL["II"]] == ["ف", "ع", "ل"] and TMPL["II"][1][2], "قالب II فقد شدّته — صريخ"


def _eq(a, b, nz):
    return (HAMZ.get(a, a) if nz else a) == (HAMZ.get(b, b) if nz else b)


def match(word, tmpl, free_end=False, nz=False):
    """مطابقةٌ موضعًا بموضع؛ المخرَج الجذرُ المستخرج أو None. الشدّةُ شرطٌ في كل الطبقات."""
    if len(word) != len(tmpl):
        return None
    root = []
    last = len(tmpl) - 1
    for i, ((wc, ws, wd), (tc, ts, td)) in enumerate(zip(word, tmpl)):
        if wd != td:
            return None
        if not (free_end and i == last) and ws != ts:
            return None
        if tc in SLOTS:
            root.append(wc)
        elif not _eq(wc, tc, nz):
            return None
    return "".join(root)


def peel(word):
    """قلعُ السوابق المعلنة — تُعرَض كلُّ حالةٍ وسيطة، ولا يُقلع ما ينزل بالكلمة دون ثلاثة أحرف."""
    out, cur = [word], word
    while len(cur) > 3:
        if (cur[0][0], cur[0][1]) in PREFIX:
            cur = cur[1:]
            out.append(cur)
            continue
        if len(cur) > 4 and cur[0][0] == "ا" and cur[1][0] == "ل":
            cur = cur[2:]
            out.append(cur)
            continue
        break
    return out


def hit(word, layer, nz=False):
    """أوّلُ مطابقٍ بترتيب I→XV المعلن؛ المخرَج (الوزن، الجذر، عددُ المطابقات) أو None."""
    cands = peel(word) if layer == "و٣-قلع" else [word]
    free_end = layer != "و١-حرفي"
    first, k = None, 0
    for c in cands:
        for n in ORDER:
            r = match(c, TMPL[n], free_end, nz)
            if r is not None:
                k += 1
                if first is None:
                    first = (n, r)
    return (first[0], first[1], k) if first else None


# ---------- الطبقتان المسحوبتان: تشخيصٌ معدود، لا تغطيةٌ تُحتسب ----------
# لا تدخلان ⚑ ولا الكلفة. غايتُهما وحدَها إعادةُ إنتاج ميكانيزم التقدير المسحوب (55.72%):
#   س١-حر   : الحركاتُ مُهمَلة، والشدّةُ تُفكّ حرفين (R5 الموروث)، وف/ع/ل بدائلُ حرّةٌ مستقلّة
#             ⟹ II يصير «أيَّ رباعيّ»، وI «أيَّ ثلاثيّ» — وهمُ التغطية.
#   س٢-مربوط: س١ نفسُها بقيدٍ واحد: تكرارُ الموضع يُلزم تكرارَ الحرف (ع=ع · ل=ل).
# الفارقُ بينهما هو الأشباحُ المقتلَعة بالربط وحده — معدودةً لا مرويّة.
DIAG = ("س١-حر", "س٢-مربوط")


def expand_shadda(word):
    """فكُّ الشدّة حرفين — R5 الموروث بعينه، مطبَّقًا على الكلمة والقالب سواء."""
    out = []
    for ch, _, dbl in word:
        out.append(ch)
        if dbl:
            out.append(ch)
    return out


TMPL_FREE = {n: expand_shadda(t) for n, t in TMPL.items()}
assert "".join(TMPL_FREE["II"]) == "فععل" and len(TMPL_FREE["II"]) == 4, \
    "فكُّ شدّة القالب II خُولف — صريخ"


def diag_match(letters, tmpl, link):
    if len(letters) != len(tmpl):
        return False
    bind = {}
    for a, t in zip(letters, tmpl):
        if t in SLOTS:
            if link:
                if bind.setdefault(t, a) != a:
                    return False
        elif a != t:
            return False
    return True


def diag(word, link):
    """المخرَج (الوزن الأول، عددُ القوالب المطابِقة) أو None — الجمعُ والوحدةُ كلاهما معروض."""
    s = expand_shadda(word)
    hits = [n for n in ORDER if diag_match(s, TMPL_FREE[n], link)]
    return (hits[0], len(hits)) if hits else None


def run(path=CORPUS):
    from dictionary_engine import classify_word, skel_of      # استيرادٌ متأخّر: لا حلقةَ استيراد
    verses = parse_verses(path)
    rich = tokenize_rich(path, verses)
    sup = defaultdict(Counter)
    definite = set()                                          # هياكلُ وردت معرَّفةً بـ«ال» — مادّةُ موجب الصدفة
    for words in verses:
        for w in words:
            sup[skel_of(w)][w[-1][1]] += 1
            s = skel_of(w)
            if len(s) > 3 and s[0] == "ا" and s[1] == "ل":
                definite.add(s[2:])
    pending = 0
    cov = {L: 0 for L in LAYERS}
    weights = {L: Counter() for L in LAYERS}
    roots = {L: Counter() for L in LAYERS}
    ambiguous = {L: 0 for L in LAYERS}
    chance = {L: 0 for L in LAYERS}                           # موجب الصدفة المعدود
    weak = {L: 0 for L in LAYERS}                             # سالب الضعف: ربحُ التسوية المعلنة
    shadda_hits = 0                                           # ما تغطّيه ح-شدة أصلًا — لا ازدواج
    dcov = {D: 0 for D in DIAG}                               # الطبقتان المسحوبتان — تشخيصٌ لا تغطية
    dsum = {D: 0 for D in DIAG}                               # مجموعُ المطابقات لا الكلمات (قوالبُ تتزاحم)
    dw = {D: Counter() for D in DIAG}
    for va, vb in zip(verses, rich):
        for wa, wb in zip(va, vb):
            if classify_word(wa, sup)[0] not in ("ث", "ع"):
                continue
            pending += 1
            widest = None
            for L in LAYERS:
                h = hit(wb, L)
                if h is None:
                    if hit(wb, L, nz=True) is not None:
                        weak[L] += 1
                    continue
                n, r, k = h
                cov[L] += 1
                weights[L][n] += 1
                roots[L][r] += 1
                ambiguous[L] += (k > 1)
                if skel_of(wa) in definite:
                    chance[L] += 1
                widest = L
            if widest is not None and any(d for _, _, d in wb):
                shadda_hits += 1
            for D, link in zip(DIAG, (False, True)):
                g = diag(wb, link)
                if g is not None:
                    dcov[D] += 1
                    dsum[D] += g[1]
                    dw[D][g[0]] += 1
    bits = sum(len(t) for t in T.values()) * 8 + len(PREFIX) * 8 * 4
    return dict(
        pending=pending,
        layers={L: dict(matched=cov[L], pct=round(cov[L] / pending * 100, 2),
                        roots=len(roots[L]), ambiguous=ambiguous[L],
                        chance_upper=chance[L], weak_gain=weak[L],
                        weights=dict(weights[L].most_common()))
                for L in LAYERS},
        widest=LAYERS[-1],
        matched_widest=cov[LAYERS[-1]],
        matched_widest_no_shadda=cov[LAYERS[-1]] - shadda_hits,
        shadda_overlap=shadda_hits,
        roots_widest=sorted(roots[LAYERS[-1]]),
        retracted=dict(
            note="طبقتان تشخيصيّتان مسحوبتان — لا تُحتسبان تغطيةً ولا تمسّان ⚑ ولا الكلفة",
            layers={D: dict(words=dcov[D], pct=round(dcov[D] / pending * 100, 2),
                            template_hits=dsum[D], weights=dict(dw[D].most_common()))
                    for D in DIAG},
            ghosts_killed_by_binding=dsum[DIAG[0]] - dsum[DIAG[1]]),
        table_cost_bits=bits)


def main(argv=None):
    ap = argparse.ArgumentParser(description="حلقة الأوزان — مطابقة المعلَّق بقوالب I–XV")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    R = run()
    W = R["layers"]
    print(f"المعلَّق (ث+ع) = {R['pending']:,} كلمة · القوالب {len(T)} من T في algebra_engine")
    for L in LAYERS:
        d = W[L]
        print(f"  {L}: مطابقة {d['matched']:,} ({d['pct']}%) · جذور {d['roots']:,} · "
              f"ملتبسة {d['ambiguous']:,} | ⊕ موجب الصدفة ≤ {d['chance_upper']:,} · "
              f"⊖ سالب الضعف {d['weak_gain']:,}")
        print("    الأوزان المطعِمة: " + " · ".join(f"{k}={v:,}" for k, v in list(d["weights"].items())[:6]))
    print(f"الأوسع ({R['widest']}): {R['matched_widest']:,} — منها {R['shadda_overlap']:,} تغطّيها ح-شدة، "
          f"فالربح الصافي على ⚑ = {R['matched_widest_no_shadda']:,}")
    print(f"كلفة جدول الأوزان معلنة: {R['table_cost_bits']} بت — تُخصم من أي ربحٍ يُبنى عليها")
    RT = R["retracted"]
    print("الطبقتان المسحوبتان (تشخيصٌ معدود — لا تغطية):")
    for D in DIAG:
        d = RT["layers"][D]
        print(f"  {D}: كلمات {d['words']:,} ({d['pct']}%) · مطابقاتُ قوالبَ {d['template_hits']:,} | "
              + " · ".join(f"{k}={v:,}" for k, v in list(d["weights"].items())[:4]))
    print(f"  أشباحٌ يقتلعها ربطُ التضاعف وحده: {RT['ghosts_killed_by_binding']:,} مطابقة")
    if a.json:
        json.dump({"الأوزان_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")


if __name__ == "__main__":
    main()
