# burhan/cert_partition.py — شهادةُ القسمة: العطبُ أنّ ثلاثةَ أعدادٍ كُتِبت بأيدٍ ثلاثة فتخالفت،
# والعلاجُ ألّا يُكتَب إلّا **مدخلٌ واحد** ويُشتَقَّ الباقي. فههنا لا رقمَ مكتوبٌ إلّا:
#   ١) الثمانيةُ والعشرون حرفًا (تعدادًا لا عددًا)   ٢) الحالاتُ الثمانيةُ (تعدادًا لا عددًا)
#   ٣) الزائدون على الثمانيةِ والعشرين (تعدادًا)     — وكلُّ ما سواها مُشتَقّ.
#
# الحقلُ المرخَّص H = A28 × الحالاتِ الأربعِ الأُوَل. والفضاءُ الكامل C = A × الحالاتِ الثماني.
# فقيدُ القسمة:            28·4 + k·8 = |C \ H|          حيث k = |A| − 28
# وهو قيدٌ **يُحَلّ ولا يُختار**: لكلِّ |C\H| جذرٌ صحيحٌ واحدٌ أو لا جذر.
#
# والاختيارُ بين الأساسين (أيُّ صور الهمزة ذرّةٌ أوّليّة) لسانيٌّ خارجَ الجبر — فلا تختار
# هذه الشهادةُ، بل تُخرِج الأساسين متّسقَين وتُحيل خمولَهما إلى `cert_inertness.py`.
import argparse, json, sys

BASE28 = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")        # تعدادٌ — والعددُ مشتقٌّ منه
STATES8 = ["فتحة", "ضمة", "كسرة", "سكون",              # الأربعُ المرخَّصةُ في H
           "تنوينُ فتح", "تنوينُ ضمّ", "تنوينُ كسر", "عُري"]   # والأربعُ خارجَه
LICENSED = 4                                            # عددُ الحالات المرخَّصة — مشتقٌّ بالقطع أدناه

# الأساسان المعلنان — تعدادًا لا عددًا. ولا ثالثَ إلّا بإعلانٍ جديد.
BASES = {
    "أ — الزائدون أربعة": ["ى", "ة", "آ", "ء"],
    "ب — الزائدون سبعة": ["أ", "إ", "آ", "ؤ", "ئ", "ء", "ى"],
}


def solve_k(unlicensed):
    """جذورُ القيد 28·4 + k·8 = |C\\H| الصحيحةُ غيرُ السالبة — قائمةً لا رقمًا مُدَّعًى."""
    base = len(BASE28) * (len(STATES8) - LICENSED)      # غيرُ المرخَّص على A28 نفسِها
    rest = unlicensed - base
    if rest < 0 or rest % len(STATES8):
        return []
    return [rest // len(STATES8)]


def derive(extras):
    """من التعداد وحدَه: كلُّ عددٍ في القسمة — ولا عددَ مكتوبٌ بيدٍ ثانية."""
    alphabet = BASE28 + [c for c in extras if c not in BASE28]
    if len(set(alphabet)) != len(alphabet):
        raise SystemExit("::error::الأبجدُ فيه تكرار — التعدادُ لا ينغلق")
    cells = len(alphabet) * len(STATES8)
    field = len(BASE28) * LICENSED
    unlicensed_on_28 = len(BASE28) * (len(STATES8) - LICENSED)
    unlicensed_on_extras = (len(alphabet) - len(BASE28)) * len(STATES8)
    return {
        "الأبجد": len(alphabet),
        "الزائدون": len(alphabet) - len(BASE28),
        "|C|": cells,
        "|H|": field,
        "|C\\H|": cells - field,
        "غيرُ_المرخَّصِ_على_A28": unlicensed_on_28,
        "غيرُ_المرخَّصِ_على_الزائدين": unlicensed_on_extras,
        "الجمعُ_يطابقُ_الطرح": unlicensed_on_28 + unlicensed_on_extras == cells - field,
        "جذرُ_القيد": solve_k(cells - field),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    # ① القطعُ الأوّل: الحالاتُ المرخَّصةُ مشتقّةٌ من موضعها في التعداد لا مكتوبةٌ رقمًا.
    licensed = [s for s in STATES8[:LICENSED]]
    fails = []
    if licensed != ["فتحة", "ضمة", "كسرة", "سكون"]:
        fails.append("الحالاتُ المرخَّصةُ ليست الأربعَ المعلنة")
    if len(BASE28) != 28:
        fails.append(f"التعدادُ الأساسُ {len(BASE28)} حرفًا لا 28")

    rows = {name: derive(extras) for name, extras in BASES.items()}
    for name, r in rows.items():
        if not r["الجمعُ_يطابقُ_الطرح"]:
            fails.append(f"{name}: المُعادُ جمعًا خالف الطرح")
        if r["|H|"] != 112:
            fails.append(f"{name}: الحقلُ {r['|H|']} لا 112 — والحقلُ لا يتحرّك بالأبجد")
        if r["جذرُ_القيد"] != [r["الزائدون"]]:
            fails.append(f"{name}: القيدُ لا يُرجِع زائديه — {r['جذرُ_القيد']}")

    # ② العطبُ نفسُه معروضًا مقيسًا: |C\H| = 144 له جذرٌ واحدٌ، وهو 4 لا 7.
    fault = {
        "المكتوبُ_في_الفصل_الأوّل": {"|C|": 256, "|C\\H|": 144, "تعدادُ_الزائدين": 7},
        "جذرُ_144": solve_k(144),
        "جذرُ_168": solve_k(168),
        "الجذرُ_وحيدٌ_لكلِّ_مدخل": all(len(solve_k(d)) <= 1 for d in range(0, 4096)),
    }
    if fault["جذرُ_144"] != [4]:
        fails.append("القيدُ لا يُعطي 4 على 144")
    if fault["جذرُ_168"] != [7]:
        fails.append("القيدُ لا يُعطي 7 على 168")
    # التخالفُ مُثبَتٌ لا مُدَّعًى: المكتوبُ 144 مع تعدادٍ سباعيٍّ لا يجتمعان.
    fault["التخالفُ_مُثبَت"] = fault["جذرُ_144"] != [fault["المكتوبُ_في_الفصل_الأوّل"]
                                                     ["تعدادُ_الزائدين"]]
    if not fault["التخالفُ_مُثبَت"]:
        fails.append("العطبُ المعلنُ لم يظهر — الشهادةُ بلا مادّة")

    out = {
        "الشهادة": "CERT-PARTITION",
        "الأساس": "صوريٌّ محض — لا مدوّنةَ ولا قياسَ على نصّ",
        "القيد": "28·4 + k·8 = |C\\H| — يُحَلّ ولا يُختار",
        "العطب": fault,
        "الأساسان": rows,
        "الاختيار": "معلَّق — لسانيٌّ خارجَ الجبر، وخمولُه على الأجيال في CERT-INERTNESS",
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-PARTITION: قيدُ القسمة —")
    print(f"    جذرُ 144 = {fault['جذرُ_144']} · جذرُ 168 = {fault['جذرُ_168']} · "
          f"الجذرُ وحيدٌ لكلِّ مدخل: {fault['الجذرُ_وحيدٌ_لكلِّ_مدخل']}")
    for name, r in rows.items():
        print(f"    {name}: |A|={r['الأبجد']} · |C|={r['|C|']} · |H|={r['|H|']} · "
              f"|C\\H|={r['|C\\H|']} = {r['غيرُ_المرخَّصِ_على_A28']} + "
              f"{r['غيرُ_المرخَّصِ_على_الزائدين']} ✓")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ كلُّ عددٍ مشتقٌّ من تعدادٍ واحد" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
