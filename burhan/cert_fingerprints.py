# burhan/cert_fingerprints.py — شهادةُ البصمات: الجيلُ الصفريُّ جدولًا، وتفرُّدُه مقيسٌ لا مُدَّعًى.
#
# G0: لكلِّ خليّةٍ من الحقل 112 توكنٌ (0–111) ودورٌ = زوجُ الإسقاط (حرف، حالة) — لا لسانيّاتٍ —
# وبصمةٌ = SHA256("H|τ|حرف|حالة")[:16]. والصيغةُ معلنةٌ بحرفها فلا تُبدَّل إلّا بقضيّةٍ جديدة.
#
# وقانونُ الاستنفاد: F1 (أزواجُ G1 الناجيةُ من Φ) تُبصَم **بإعادة توظيف** بصمات G0 لا بسكٍّ
# جديد: SHA256("F|β₁|β₂"). والتفرُّدُ يُقاس عدًّا، فالازدواجُ لو وقع صريخٌ يُسقِط الشهادة.
import argparse, hashlib, json, os, sys

BASE28 = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
STATES4 = ["فتحة", "ضمة", "كسرة", "سكون"]
SUKUN = "سكون"
FPLEN = 16


def fp_cell(tau, letter, state):
    return hashlib.sha256(f"H|{tau}|{letter}|{state}".encode()).hexdigest()[:FPLEN]


def fp_pair(a, b):
    return hashlib.sha256(f"F|{a}|{b}".encode()).hexdigest()[:FPLEN]


def tokens():
    """الجدولُ مبنيٌّ بالتعداد: الترتيبُ حرفٌ ثمّ حالة، والتوكنُ موضعُه فيه."""
    out = []
    for letter in BASE28:
        for state in STATES4:
            tau = len(out)
            out.append({"توكن": tau, "حرف": letter, "حالة": state,
                        "بصمة": fp_cell(tau, letter, state)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--table", help="مسارُ جدول G0 — TOKENS-112.json")
    args = ap.parse_args()

    fails = []
    cells = tokens()
    if len(cells) != 112:
        fails.append(f"الخلايا {len(cells)} لا 112")
    fps = [c["بصمة"] for c in cells]
    if len(set(fps)) != len(fps):
        fails.append(f"بصماتُ G0 مزدوجة: {len(fps) - len(set(fps))} ازدواجًا")
    if len({(c["حرف"], c["حالة"]) for c in cells}) != len(cells):
        fails.append("أدوارٌ مزدوجة — الإسقاطُ ليس فريدًا")
    if any(len(f) != FPLEN for f in fps):
        fails.append("بصمةٌ بطولٍ غيرِ معلن")

    # F1: الأزواجُ الناجيةُ من Φ — تُعَدّ ههنا بالبناء، وتُصادَم بعددِ CERT-GENERATIONS.
    pairs, pfps = 0, set()
    for a in cells:
        for b in cells:
            if a["حالة"] == SUKUN and b["حالة"] == SUKUN:
                continue
            pairs += 1
            pfps.add(fp_pair(a["بصمة"], b["بصمة"]))
    if pairs != 11760:
        fails.append(f"أزواجُ F1 {pairs} لا 11,760")
    if len(pfps) != pairs:
        fails.append(f"بصماتُ F1 مزدوجة: {pairs - len(pfps)} ازدواجًا")

    # وقانونُ الاستنفاد مقيسٌ لا مُدَّعًى: فضاءا الاسمَين لا يتقاطعان، فلا بصمةَ طيٍّ
    # تنتحل بصمةَ خليّة — ولو تقاطعا لصار الطيُّ سكًّا جديدًا من حيث لا يُرى.
    collision = len(pfps & set(fps))
    if collision:
        fails.append(f"بصمةُ طيٍّ انتحلت بصمةَ خليّة: {collision}")

    out = {
        "الشهادة": "CERT-FINGERPRINTS",
        "الأساس": "صوريٌّ محض — جدولُ G0 وطيُّ F1، لا مدوّنة",
        "صيغةُ_بصمةِ_الخليّة": 'SHA256("H|τ|حرف|حالة")[:16]',
        "صيغةُ_طيِّ_الزوج": 'SHA256("F|β₁|β₂")[:16]',
        "مقيس": {
            "خلايا": len(cells),
            "بصماتٌ_فريدة": len(set(fps)),
            "أزواجُ_F1": pairs,
            "بصماتُ_F1_الفريدة": len(pfps),
            "تقاطعُ_فضاءَي_الاسم": len(pfps & set(fps)),
        },
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    if args.table:
        with open(args.table, "w", encoding="utf-8") as fh:
            json.dump({"G0": cells, "صيغةُ_البصمة": out["صيغةُ_بصمةِ_الخليّة"]},
                      fh, ensure_ascii=False, indent=1)

    print("— CERT-FINGERPRINTS: بصماتُ G0 وطيُّ F1 —")
    for k, v in out["مقيس"].items():
        print(f"    {k}: {v:,}" if isinstance(v, int) else f"    {k}: {v}")
    print(f"    أوّلُ الجدول: τ=0 · {cells[0]['حرف']} · {cells[0]['حالة']} · {cells[0]['بصمة']}")
    print(f"    آخرُه:      τ=111 · {cells[-1]['حرف']} · {cells[-1]['حالة']} · {cells[-1]['بصمة']}")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ لا ازدواجَ في بصمةٍ واحدة" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
