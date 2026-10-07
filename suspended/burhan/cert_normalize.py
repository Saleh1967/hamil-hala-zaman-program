# burhan/cert_normalize.py — شهادةُ التطبيع: المجازُ المطبوعُ يُبنى بترتيبٍ معلن، وأثرُ كلِّ
# تحويلٍ يُعَدّ باسمه، والناتجُ يُختَم. لا تستورد هذه الشهادةُ شيئًا من الشجرة.
#
# الأساسُ يُعلَن قبل القياس: **الخامُ مدخلًا · المطبوعُ مخرَجًا**. ولا يدخل تحويلٌ تطبيعيٌّ
# شاهدًا ضدّ قيدٍ من طبيعته — ولذلك تقف هذه الشهادةُ عند العدّ والختم، ولا تحكم على Φ.
#
# ترتيبُ التحويلات معلنٌ ومُلزِم (وثمنُ خلطه مدفوعٌ: 495 موضعًا ابتُلعت حين وُقِف عند الشدّة):
#   R5 الشدّة  ⟼ (الحرفُ ساكنًا) + (الحرفُ متحرّكًا)      ثمّ
#   R4 التنوين ⟼ (حركتُه) + (نونٌ ساكنة)     — **على النسخة الثانية** لا على الأولى، ثمّ
#   T-عُري      ⟼ عُريٌ داخلَ الكلمة سكونٌ صريح (وخاتمةُ الكلمة تبقى عاريةً: موضعُ وقفٍ لا سكون)، ثمّ
#   T1 الهمزة  ⟼ {أ إ آ} ⟵ ا · ؤ ⟵ و · ئ ⟵ ي · ء تبقى بذاتها
#   T-المعتل (ى ⟼ ا): **معلَّقٌ لا يُطبَّق** — يُعَدّ أثرُه ولا يُنفَّذ.
import argparse, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(HERE), "mujammad.txt")
SEAL_SHA256 = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"
# ختمُ الناتج معلنٌ **قبل** التشغيل: التطبيعُ دالّةٌ حتميّةٌ، فناتجُها يُتوقَّع ويُصادَم.
# وانكسارُه لو انكسر سقوطُ التحويلِ المعلن لا «تصحيحٌ» للختم — يُسجَّل ويُعاد إعلانُه.
SEAL_NORM = "614b1189cb9a5fd126f4e696c2ccb3dda57741367365333b7b449a1aef5f5f0d"

AR_RANGES = ((0x0621, 0x064A), (0x064B, 0x0652), (0x0670, 0x0670), (0x06D6, 0x06ED))
VOWELS = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TANWIN = {0x064B: "فتحة", 0x064C: "ضمة", 0x064D: "كسرة"}
SHADDA = 0x0651
DAGGER = 0x0670                                   # الخنجريّةُ فتحةٌ باتفاقٍ معلن
BARE = "عُري"
MARK = {"فتحة": "\u064E", "ضمة": "\u064F", "كسرة": "\u0650", "سكون": "\u0652", BARE: ""}
HAMZA_FOLD = {"أ": "ا", "إ": "ا", "آ": "ا", "ؤ": "و", "ئ": "ي"}
SUSPENDED_FOLD = {"ى": "ا"}                        # معلَّقٌ — يُعَدّ ولا يُطبَّق


def is_ar(ch):
    return any(lo <= o <= hi for lo, hi in AR_RANGES for o in (ord(ch),))


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


def marks_of(word, i):
    """علاماتُ الحرفِ في موضعه — كلُّها لا أوّلُها، فلا تُبتلَع ثانيةٌ بوجود أولى."""
    out = []
    while i + 1 < len(word) and (0x064B <= ord(word[i + 1]) <= 0x0652
                                 or ord(word[i + 1]) == DAGGER):
        i += 1
        out.append(ord(word[i]))
    return out, i


def units(word, stop_at_shadda=False):
    """الكلمةُ الخامُ ⟼ وحداتُ (حرف، حالة، منشأ) بالترتيب المعلن.

    و`stop_at_shadda` محاولةُ تكذيبٍ لا سياسة: تُحاكي الخطأَ المدفوعَ ثمنُه (الوقوفُ عند
    الشدّة فيسقط تنوينُها)، ليُقاس فرقُه عدًّا بدل أن يُروى حكايةً.
    """
    out, i, n = [], 0, len(word)
    stats = {"R5": 0, "R4": 0, "شدةٌ_وتنوينٌ_معًا": 0, "خنجريّة": 0}
    while i < n:
        ch = word[i]
        if not is_letter(ch):
            i += 1
            continue
        ms, i = marks_of(word, i)
        tan = next((m for m in ms if m in TANWIN), None)
        vow = next((m for m in ms if m in VOWELS), None)
        if DAGGER in ms:
            stats["خنجريّة"] += 1
        state = (VOWELS[vow] if vow else TANWIN[tan] if tan else
                 "فتحة" if DAGGER in ms else BARE)
        if SHADDA in ms:                          # R5 أوّلًا — الحرفُ نفسُه ساكنًا ثمّ متحرّكًا
            out.append((ch, "سكون", "R5"))
            stats["R5"] += 1
            if tan:
                stats["شدةٌ_وتنوينٌ_معًا"] += 1
                if stop_at_shadda:                # الخطأُ المُحاكى: يبتلع تنوينَ المشدَّد
                    out.append((ch, state, "رسم"))
                    i += 1
                    continue
        out.append((ch, state, "R4" if tan and not vow else "رسم"))
        if tan:                                   # R4 — على النسخة الثانية وحدَها
            out.append(("ن", "سكون", "R4"))
            stats["R4"] += 1
        i += 1
    return out, stats


def normalize(us):
    """العُريُ داخلَ الكلمة سكونٌ صريح، وخاتمتُها تبقى عاريةً · ثمّ طيُّ الهمزة.

    والمعتلُّ معلَّقٌ: يُعَدّ أثرُه ولا يُطبَّق — فالمعلَّقُ يُسمّى معلَّقًا ولا يُنفَّذ خُفيةً.
    """
    out = []
    counts = {"عُريٌ_صار_سكونًا": 0, "عُريٌ_باقٍ_في_الخاتمة": 0, "طيُّ_الهمزة": 0,
              "همزةٌ_قائمةٌ_بذاتها": 0, "معتلٌّ_معلَّق": 0}
    for idx, (ch, st, origin) in enumerate(us):
        if st == BARE:
            if idx < len(us) - 1:
                st = "سكون"
                counts["عُريٌ_صار_سكونًا"] += 1
            else:
                counts["عُريٌ_باقٍ_في_الخاتمة"] += 1
        if ch in HAMZA_FOLD:
            counts["طيُّ_الهمزة"] += 1
            ch = HAMZA_FOLD[ch]
        elif ch == "ء":
            counts["همزةٌ_قائمةٌ_بذاتها"] += 1
        if ch in SUSPENDED_FOLD:
            counts["معتلٌّ_معلَّق"] += 1           # يُعَدّ ولا يُطوى
        out.append((ch, st, origin))
    return out, counts


def render(us):
    return "".join(ch + MARK[st] for ch, st, _ in us)


def add(dst, src):
    for k, v in src.items():
        dst[k] = dst.get(k, 0) + v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--out", default=os.path.join(HERE, "mujammad.norm.txt"))
    args = ap.parse_args()

    blob = read_sealed()
    verses = verses_of(blob)
    fails = []

    tot, ncounts = {}, {}
    lines, raw_skeletons, norm_skeletons, all_units = [], set(), set(), 0
    for verse in verses:
        words = []
        for w in verse:
            us, st = units(w)
            add(tot, st)
            nus, nc = normalize(us)
            add(ncounts, nc)
            all_units += len(nus)
            raw_skeletons.add("".join(c for c in w if is_letter(c)))
            norm_skeletons.add("".join(ch for ch, _, _ in nus))
            words.append(render(nus))
        lines.append(" ".join(words))
    text = "\n".join(lines) + "\n"
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    norm_blob = text.encode("utf-8")

    # ① محاولةُ التكذيب المقيسة: الوقوفُ عند الشدّة يبتلع تنوينَ المشدَّد — بعدده لا بالقول.
    swallowed = 0
    for verse in verses:
        for w in verse:
            good, _ = units(w)
            bad, _ = units(w, stop_at_shadda=True)
            swallowed += len(good) - len(bad)
    if swallowed != tot["شدةٌ_وتنوينٌ_معًا"]:
        fails.append(f"فرقُ الترتيبِ {swallowed} لا يساوي المشدَّدَ المنوَّنَ "
                     f"{tot['شدةٌ_وتنوينٌ_معًا']}")
    if not swallowed:
        fails.append("الترتيبُ بلا أثرٍ مقيس — الحارسُ بلا مادّة")

    # ② الرحلةُ ذهابًا وإيابًا: البايتاتُ المكتوبةُ تُقرَأ من جديدٍ فتُعيد الوحداتِ بأعيانها.
    #    والمصادمةُ على **الوحدات** لا على نصٍّ مشكولٍ حرفيًّا — والفرقُ لو وقع يُسمّى بعدده.
    back = 0
    for verse, ln in zip(verses, lines):
        for w, nw in zip(verse, ln.split(" ")):
            us, _ = units(w)
            nus, _ = normalize(us)
            reread, j = [], 0
            while j < len(nw):
                ch = nw[j]
                j += 1
                st = BARE
                if j < len(nw) and ord(nw[j]) in VOWELS:
                    st = VOWELS[ord(nw[j])]
                    j += 1
                reread.append((ch, st))
            if reread != [(ch, st) for ch, st, _ in nus]:
                back += 1
    if back:
        fails.append(f"المطبوعُ لا يُعيد وحداتِه عند إعادة القراءة في {back} كلمة")

    norm_seal = hashlib.sha256(norm_blob).hexdigest()
    if norm_seal != SEAL_NORM:
        fails.append(f"ختمُ المطبوعِ المتوقَّعُ {SEAL_NORM[:12]}… والمقيسُ {norm_seal[:12]}… "
                     f"— التحويلُ المعلنُ تبدَّل، والختمُ لا يُصحَّح بل يُعاد إعلانُه")

    out = {
        "الشهادة": "CERT-NORMALIZE",
        "الأساس": "الخامُ مدخلًا · المطبوعُ مخرَجًا — والترتيبُ معلنٌ قبل التشغيل",
        "الترتيب": ["R5 الشدّة", "R4 التنوين على النسخة الثانية", "T-عُري داخل الكلمة",
                    "T1 طيُّ الهمزة", "T-المعتل: معلَّقٌ لا يُطبَّق"],
        "مقيس": {
            "آيات": len(verses),
            "كلمات": sum(len(v) for v in verses),
            "وحداتُ_المطبوع": all_units,
            "فكُّ_الشدّة_R5": tot["R5"],
            "تفكيكُ_التنوين_R4": tot["R4"],
            "شدةٌ_وتنوينٌ_معًا": tot["شدةٌ_وتنوينٌ_معًا"],
            "خنجريّةٌ_فتحةً": tot["خنجريّة"],
            "عُريٌ_صار_سكونًا": ncounts["عُريٌ_صار_سكونًا"],
            "عُريٌ_باقٍ_في_الخاتمة": ncounts["عُريٌ_باقٍ_في_الخاتمة"],
            "طيُّ_الهمزة": ncounts["طيُّ_الهمزة"],
            "همزةٌ_قائمةٌ_بذاتها": ncounts["همزةٌ_قائمةٌ_بذاتها"],
            "معتلٌّ_معلَّقٌ_لم_يُطوَ": ncounts["معتلٌّ_معلَّق"],
            "هياكلُ_الخام": len(raw_skeletons),
            "هياكلُ_المطبوع": len(norm_skeletons),
            "بايتاتُ_المطبوع": len(norm_blob),
            "ختمُ_المطبوع": norm_seal,
        },
        "ختمُ_المطبوعِ_المعلنُ_قبل_التشغيل": SEAL_NORM,
        "تكذيبٌ_مقيس": {
            "الوقوفُ_عند_الشدّةِ_يبتلع": swallowed,
            "الأثرُ_ظهر": swallowed == tot["شدةٌ_وتنوينٌ_معًا"] and swallowed > 0,
        },
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-NORMALIZE: التطبيعُ بترتيبٍ معلن —")
    for k, v in out["مقيس"].items():
        print(f"    {k}: {v:,}" if isinstance(v, int) else f"    {k}: {v}")
    print(f"    [تكذيب] الوقوفُ عند الشدّة يبتلع {swallowed:,} موضعًا — "
          f"وهي المشدَّدُ المنوَّنُ بعينه")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ الترتيبُ التزم والهياكلُ تصادمت" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
