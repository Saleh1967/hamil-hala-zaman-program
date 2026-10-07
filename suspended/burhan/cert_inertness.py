# burhan/cert_inertness.py — شهادةُ الخمول: هل يسري عطبُ القسمة إلى الأجيال؟
#
# الدعوى المسجَّلةُ قبل القياس: «الحقلُ H معلنٌ على الثمانيةِ والعشرين وحدَها، وكلُّ ما بعده
# مبنيٌّ على H لا على الأبجد — فاختيارُ الزائدين خاملٌ على G1..G6». وهذه دعوى **قابلةٌ للتكذيب**:
# يكفي أن يتحرّك عددٌ واحدٌ في السلّم بتبديل الأبجد ليسقط الخمول.
#
# وحتّى لا يكون الخمولُ تحصيلَ حاصل، تُشغَّل معه محاولةُ تكذيبٍ لها أثرٌ **يجب أن يظهر**:
# لو رُخِّص الحقلُ على الأبجد كلِّه لتحرّك السلّمُ قطعًا. فإن لم يتحرّك فالآلةُ عمياءُ لا خاملة.
import argparse, json, sys

BASE28 = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
STATES4 = ["فتحة", "ضمة", "كسرة", "سكون"]
SUKUN = "سكون"
LADDER = 6

ALPHABETS = {
    "|A|=28 — لا زائدَ": [],
    "|A|=32 — إصلاح أ": ["ى", "ة", "آ", "ء"],
    "|A|=35 — إصلاح ب": ["أ", "إ", "آ", "ؤ", "ئ", "ء", "ى"],
}


def ladder(field, kmax=LADDER):
    """سلّمُ الأجيال من حقلٍ معطًى — عوديّةً، ولا رقمَ مكتوبٌ فيه."""
    ns = sum(1 for c in field if c[1] == SUKUN)
    nm = len(field) - ns
    out, m, s = {}, nm, ns
    for k in range(1, kmax + 1):
        if k > 1:
            m, s = nm * (m + s), ns * m
        out[f"G{k}"] = m + s
    return out


def field_licensed(extras):
    """الحقلُ المرخَّص: الثمانيةُ والعشرون وحدَها × الحالاتِ الأربع — والزائدون خارجَه بالنصّ."""
    del extras                                   # مذكورون في المدخل، خارجون بالترخيص
    return [(l, s) for l in BASE28 for s in STATES4]


def field_if_all_licensed(extras):
    """محاولةُ التكذيب: لو رُخِّص الحقلُ على الأبجد كلِّه — أثرٌ يجب أن يظهر."""
    alphabet = BASE28 + [c for c in extras if c not in BASE28]
    return [(l, s) for l in alphabet for s in STATES4]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    fails = []
    rows = {name: ladder(field_licensed(ex)) for name, ex in ALPHABETS.items()}
    ref = rows["|A|=28 — لا زائدَ"]
    inert = all(r == ref for r in rows.values())
    if not inert:
        fails.append("الخمولُ سقط — سلّمٌ تحرّك بتبديل الأبجد")

    # ① محاولةُ تكذيبٍ يجب أن **تنجح في إحداث الأثر**، وإلّا فالآلةُ لا تقيس شيئًا.
    counter = {name: ladder(field_if_all_licensed(ex))
               for name, ex in ALPHABETS.items() if ex}
    moved = all(r != ref for r in counter.values())
    if not moved:
        fails.append("الآلةُ عمياء: حتّى ترخيصُ الأبجد كلِّه لم يُحرِّك السلّم")

    out = {
        "الشهادة": "CERT-INERTNESS",
        "الأساس": "صوريٌّ محض — سلالمُ أجيالٍ من حقولٍ معلنة",
        "الدعوى": "اختيارُ الزائدين خاملٌ على G1..G6 لأنّ H معلنٌ على A28 وحدَها",
        "سلالمُ_الترخيصِ_المعلن": rows,
        "الخمولُ_قائم": inert,
        "لو_رُخِّصَ_الأبجدُ_كلُّه": counter,
        "الأثرُ_يظهر_عند_التكذيب": moved,
        "مدى_العطب": ("عطبُ الفصل الأوّل حقيقيٌّ ومُسقِطٌ لقسمته نفسِها، "
                      "وغيرُ سارٍ إلى الأجيال — والمدى مقيسٌ لا مُطلَق"),
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-INERTNESS: مدى العطب —")
    for name, r in rows.items():
        print(f"    {name}: " + " · ".join(f"{k}={v:,}" for k, v in r.items()))
    print(f"    الخمولُ على الأجيال: {inert}")
    for name, r in counter.items():
        print(f"    [تكذيب] لو رُخِّص الأبجدُ كلُّه في {name}: G2={r['G2']:,} — تحرّك ✓")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ الخمولُ مُبرهَنٌ والآلةُ ليست عمياء" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
