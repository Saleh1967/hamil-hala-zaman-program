# burhan/cert_generations.py — شهادةُ الأجيال: كلُّ عددٍ بأربعِ آلاتٍ لا تشترك في شيء.
#
# البناءُ قبل الاختبار: الحقلُ H يُبنى **تعدادًا** (28 حرفًا × 4 حالات) لا رقمًا مكتوبًا،
# ثمّ يُعَدّ الناجون من القيد Φ: «لا يتجاور ساكنان». والأعدادُ الناتجةُ رياضيّاتٌ خالصة —
# صحيحةٌ سواءٌ صحَّ Φ على المدوّنة أم بطل؛ والذي يتزحزح ببطلانه **توصيفُها** لا قيمتُها.
#
# والتوقُّعُ قبل القياس: الصيغةُ المغلقة معلنةٌ أدناه بحرفها قبل أن يُشغَّل تعدادٌ واحد —
#   G_k = Σ_j  C(k−j+1, j) · 28^j · 84^(k−j)        (اختيارُ j ساكنًا غيرِ متجاورة)
# وانكسارُها لو انكسرت خبرٌ عن القيد، لا تصحيحٌ للرقم.
import argparse, itertools, json, math, sys

BASE28 = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
STATES4 = ["فتحة", "ضمة", "كسرة", "سكون"]
SUKUN = "سكون"

FIELD = [(letter, state) for letter in BASE28 for state in STATES4]   # H تعدادًا
SAKIN = [c for c in FIELD if c[1] == SUKUN]
MUTAHARRIK = [c for c in FIELD if c[1] != SUKUN]

EXHAUSTIVE_UPTO = 3          # حدُّ التعداد الشامل — 112³ سلسلةً تُمشَّط واحدةً واحدة
LADDER = 6                   # مدى السلّم في الطرق الثلاث الأولى


# ── ① العوديّة: حالتان لا أكثر — خاتمةٌ متحرّكةٌ وخاتمةٌ ساكنة ────────────────
def by_recursion(kmax, ns, nm):
    """m_{k+1} = nm·(m_k+s_k) · s_{k+1} = ns·m_k — والساكنُ لا يَخلُف ساكنًا."""
    out, m, s = {}, nm, ns
    for k in range(1, kmax + 1):
        if k > 1:
            m, s = nm * (m + s), ns * m
        out[k] = m + s
    return out


# ── ② مصفوفةُ النقل: [[nm, nm], [ns, 0]] مرفوعةً بالضرب الصحيح لا بالفاصلة ──
def mat_mul(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def by_matrix(kmax, ns, nm):
    T = [[nm, nm], [ns, 0]]
    out, v = {}, [[nm], [ns]]                    # (m_1, s_1)
    for k in range(1, kmax + 1):
        if k > 1:
            v = mat_mul(T, v)
        out[k] = v[0][0] + v[1][0]
    return out


# ── ③ الصيغةُ المغلقة: من بابٍ آخرَ — اختيارُ مواضعِ السواكن غيرِ المتجاورة ──
def by_closed_form(kmax, ns, nm):
    out = {}
    for k in range(1, kmax + 1):
        out[k] = sum(math.comb(k - j + 1, j) * ns ** j * nm ** (k - j)
                     for j in range(0, k // 2 + 2) if k - j + 1 >= j)
    return out


# ── ④ التعدادُ الشاملُ: بلا صيغةٍ ولا ذكاء — كلُّ سلسلةٍ تُمشَّط وتُفحَص ──────
def by_exhaustive(kmax, field):
    """`itertools.product` على الحقل نفسِه. والحلقةُ **داخلَ السلسلة وحدَها** —
    لا تعبر حدًّا ولا تحمل حالةً من سلسلةٍ إلى أختها (درسُ وهم 839)."""
    out = {}
    for k in range(1, kmax + 1):
        good = 0
        for seq in itertools.product(range(len(field)), repeat=k):
            ok = True
            for i in range(1, k):
                if field[seq[i - 1]][1] == SUKUN and field[seq[i]][1] == SUKUN:
                    ok = False
                    break
            good += ok
        out[k] = good
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--exhaustive", type=int, default=EXHAUSTIVE_UPTO,
                    help="حدُّ التعداد الشامل — 0 يُعطِّله")
    args = ap.parse_args()

    fails = []
    if len(FIELD) != 112 or len(set(FIELD)) != 112:
        fails.append(f"الحقلُ {len(FIELD)} خليّةً لا 112، أو فيه تكرار")
    ns, nm = len(SAKIN), len(MUTAHARRIK)
    if (ns, nm) != (28, 84):
        fails.append(f"القسمةُ {ns}/{nm} لا 28/84")

    rec = by_recursion(LADDER, ns, nm)
    mat = by_matrix(LADDER, ns, nm)
    clo = by_closed_form(LADDER, ns, nm)
    exh = by_exhaustive(args.exhaustive, FIELD) if args.exhaustive else {}

    rows = {}
    for k in range(1, LADDER + 1):
        r = {"عوديّة": rec[k], "مصفوفةُ_نقل": mat[k], "صيغةٌ_مغلقة": clo[k]}
        if k in exh:
            r["تعدادٌ_شامل"] = exh[k]
        vals = set(r.values())
        r["متّفقة"] = len(vals) == 1
        if not r["متّفقة"]:
            fails.append(f"G{k}: الطرقُ تخالفت {r}")
        rows[f"G{k}"] = r

    # التوقُّعُ المكتوبُ يدًا في سلّم الأجيال — يُصادَم بالعوديّة ولا يُنسَخ منها.
    hand = 84 ** 3 + 3 * (84 ** 2 * 28) + (28 * 84 * 28)
    if hand != rec[3]:
        fails.append(f"الصيغةُ المكتوبةُ يدًا {hand} خالفت العوديّة {rec[3]}")
    # وحدُّ الفضاء غيرِ المقيَّد معروضٌ لا مبتلَع: كم ثلاثيّةً حذف Φ؟
    dropped3 = len(FIELD) ** 3 - rec[3]

    out = {
        "الشهادة": "CERT-GENERATIONS",
        "الأساس": "صوريٌّ محض — تعدادُ سلاسلِ الحقل، لا قياسَ على مدوّنة",
        "الحقل": {"خلايا": len(FIELD), "ساكنة": ns, "متحرّكة": nm},
        "القيد": "Φ: لا يتجاور ساكنان",
        "التوقُّعُ_المعلنُ_قبل_التعداد": "G_k = Σ_j C(k−j+1, j)·28^j·84^(k−j)",
        "سلّم": rows,
        "الصيغةُ_المكتوبةُ_يدًا_لـG3": hand,
        "ثلاثيّاتٌ_حذفها_Φ": dropped3,
        "حدُّ_التعدادِ_الشامل": args.exhaustive,
        "توصيف": ("عددُ السلاسل التي لا يتجاور فيها ساكنان — صحيحٌ سواءٌ رُخِّص Φ "
                  "على المدوّنة أم لم يُرخَّص. ورخصتُه في CERT-SUKUN."),
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-GENERATIONS: الأجيالُ بأربعِ آلات —")
    for name, r in rows.items():
        cols = " · ".join(f"{k}={v:,}" for k, v in r.items() if k != "متّفقة")
        print(f"    {name}: {cols} {'✓' if r['متّفقة'] else '✗'}")
    print(f"    الصيغةُ المكتوبةُ يدًا لـG3 = {hand:,} · تطابقُ العوديّة: {hand == rec[3]}")
    print(f"    ثلاثيّاتٌ حذفها Φ: {dropped3:,} من {len(FIELD) ** 3:,}")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ الطرقُ كلُّها متّفقة" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
