# burhan/cert_sukun.py — شهادةُ اللقاء: فصلُ «839» عن «صفر» بأساسَيهما المسمَّيين.
#
# العطبُ أنّ عددين متخالفين نُسِبا إلى أساسٍ واحد («الخام»)، وهما في الحقيقة عددان لأساسين.
# والعلاجُ أن يُقاس كلُّ واحدٍ بأساسه معلنًا، ويُعرَضا صفًّا إلى صفّ — فيسقط التخالفُ لا بالترجيح
# بل بالتسمية. ولا تستورد هذه الشهادةُ شيئًا من الشجرة.
#
# ثلاثةُ أسسٍ معلنةٌ قبل العدّ، ورابعٌ محاولةُ تكذيب:
#   ① الخام كما رُسِم      — تيارُ حروف الكلمة بعلاماتها الصريحة، لا حذفَ ولا توسيع.
#   ② الفلترُ الميدانيّ     — يُسقِط ما خرج عن الثمانيةِ والعشرين (الهمزاتُ · ى · ة)،
#                            فيُلاصِق ما فصلَه حرفٌ محذوف: هذا هو **الجوارُ المصنوع**.
#   ③ المطبوع             — بعد فكِّ الشدّة وتفكيك التنوين وتصريح العُري داخلَ الكلمة.
#   ④ [تكذيب] عبورُ الكلمات — حلقةٌ لا تُصفَّر عند حدِّ الكلمة، فتعدّ لقاءً لم يقع في كلمة.
#
# والحكمُ على Φ لا يُنقَل من أساسٍ إلى أساس: صفرُ الخامِ لا يُحتجُّ به على المطبوع، و839
# المصنوعةُ لا يُحتجُّ بها على الخام.
import argparse, collections, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(HERE), "mujammad.txt")
SEAL_SHA256 = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"

BASE28 = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")   # تعدادٌ واحدٌ يُصادَم عبر الشهادات
VOWELS = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TANWIN = {0x064B: "فتحة", 0x064C: "ضمة", 0x064D: "كسرة"}
SHADDA = 0x0651
DAGGER = 0x0670
BARE = "عُري"
SUKUN = "سكون"
AR_RANGES = ((0x0621, 0x064A), (0x064B, 0x0652), (0x0670, 0x0670), (0x06D6, 0x06ED))


def is_ar(ch):
    o = ord(ch)
    return any(lo <= o <= hi for lo, hi in AR_RANGES)


def is_letter(ch):
    return 0x0621 <= ord(ch) <= 0x064A


def read_sealed():
    with open(CORPUS, "rb") as fh:
        blob = fh.read()
    got = hashlib.sha256(blob).hexdigest()
    if got != SEAL_SHA256:
        raise SystemExit(f"::error::ليس المجمَّد — sha256 أعطى {got}")
    return blob


def verses_of(blob):
    verses = []
    for ln in blob.decode("utf-8-sig").splitlines():
        if not ln.strip() or not any(is_ar(c) for c in ln):
            continue
        words = [w for w in ln.split(" ") if any(is_letter(c) for c in w)]
        if words:
            verses.append(words)
    return verses


def stream(word, basis):
    """كلمةٌ ⟼ تيارُ (حرف، حالة) على الأساس المسمّى — ولا أساسَ ضمنيّ."""
    out, i, n = [], 0, len(word)
    while i < n:
        ch = word[i]
        if not is_letter(ch):
            i += 1
            continue
        ms = []
        while i + 1 < n and (0x064B <= ord(word[i + 1]) <= 0x0652
                             or ord(word[i + 1]) == DAGGER):
            i += 1
            ms.append(ord(word[i]))
        tan = next((m for m in ms if m in TANWIN), None)
        vow = next((m for m in ms if m in VOWELS), None)
        state = (VOWELS[vow] if vow else TANWIN[tan] if tan else
                 "فتحة" if DAGGER in ms else BARE)
        if basis == "الفلترُ الميدانيّ" and ch not in BASE28:
            i += 1                                # الحرفُ يُحذَف — فيُلاصَق جاراه
            continue
        if basis == "المطبوع":
            if SHADDA in ms:
                out.append((ch, SUKUN))
            out.append((ch, state))
            if tan:
                out.append(("ن", SUKUN))
        else:
            out.append((ch, state))
        i += 1
    if basis == "المطبوع":                        # تصريحُ العُري داخلَ الكلمة وحدَه
        out = [(ch, SUKUN if st == BARE and k < len(out) - 1 else st)
               for k, (ch, st) in enumerate(out)]
    return out


def contacts(verses, basis):
    """لقاءاتُ ساكنَين متجاورين — والحلقةُ **تُصفَّر عند كلِّ كلمة** فلا تعبر حدًّا."""
    total, forms = 0, collections.Counter()
    for verse in verses:
        for w in verse:
            us = stream(w, basis)
            hits = sum(1 for a, b in zip(us, us[1:]) if a[1] == SUKUN and b[1] == SUKUN)
            total += hits
            if hits:
                forms[w] += hits
    return total, forms


def contacts_crossing(verses, basis):
    """[تكذيب] حلقةٌ لا تُصفَّر: تصل آخرَ الكلمة بأوّلِ ما بعدها — عددُ الوهم يُقاس."""
    total = 0
    for verse in verses:
        us = [u for w in verse for u in stream(w, basis)]
        total += sum(1 for a, b in zip(us, us[1:]) if a[1] == SUKUN and b[1] == SUKUN)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    verses = verses_of(read_sealed())
    fails = []
    rows, tops = {}, {}
    for basis in ("الخام", "الفلترُ الميدانيّ", "المطبوع"):
        n, forms = contacts(verses, basis)
        rows[basis] = n
        tops[basis] = [{"صورة": w, "لقاءات": c} for w, c in forms.most_common(5)]

    crossing = {b: contacts_crossing(verses, b) for b in rows}
    inflation = {b: crossing[b] - rows[b] for b in rows}

    if rows["الخام"] != 0:
        fails.append(f"الخامُ أعطى {rows['الخام']} لقاءً — والدعوى المسجَّلةُ صفر")
    if rows["الفلترُ الميدانيّ"] <= rows["الخام"]:
        fails.append("الفلترُ لم يصنع جوارًا — الشهادةُ بلا مادّة")
    if all(v == 0 for v in inflation.values()):
        fails.append("عبورُ الكلمات بلا أثرٍ مقيس — حارسُ الحدّ بلا مادّة")

    out = {
        "الشهادة": "CERT-SUKUN",
        "الدعوى_المسجَّلةُ_قبل_العدّ": ("العددان 839 و0 لأساسين لا لأساسٍ واحد: "
                                        "صفرٌ على الخام، و839 جوارٌ صنعه حذفُ الهمزة"),
        "لقاءُ_ساكنَين_بالأساس": rows,
        "أكثرُ_الصورِ_لقاءً": tops,
        "تكذيبٌ_مقيس": {
            "عبورُ_الكلمات": crossing,
            "الوهمُ_الذي_يضيفه_العبور": inflation,
        },
        "حكمُ_Φ": {
            "على_الخام": "قائمٌ مقيسًا — صفرُ لقاءٍ داخلَ الكلمة",
            "على_الفلترِ_الميدانيّ": ("لا يُحتَجُّ به: الجوارُ مصنوعٌ بحذف الحرف الفاصل، "
                                       "فالانتهاكاتُ المعدودةُ أثرُ الآلة لا أثرُ اللغة"),
            "على_المطبوع": ("مقيسٌ لا مُرخَّص: التحويلُ هو الذي يصنع السكونَ، "
                             "فلا يُقاس به قيدٌ من طبيعته"),
        },
        "أثرُه_على_الأجيال": ("لا شيء: G1..G6 أعدادُ سلاسلَ لا يتجاور فيها ساكنان — "
                              "صحيحةٌ سواءٌ رُخِّص Φ أم لا. والمتزحزحُ توصيفُها لا قيمتُها"),
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-SUKUN: 839 ⟷ صفر، بأساسَيهما —")
    for basis, n in rows.items():
        print(f"    {basis}: {n:,} لقاءً · [تكذيب] بعبور الكلمات {crossing[basis]:,} "
              f"(وهمٌ يضيفه العبور: {inflation[basis]:,})")
    for w in tops["الفلترُ الميدانيّ"]:
        print(f"        {w['صورة']}: {w['لقاءات']}")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ العددان فُصِلا بأساسَيهما" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
