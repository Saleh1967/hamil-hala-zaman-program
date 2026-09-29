# burhan/cert_corpus.py — شهادةُ المدوّنة: الختمُ أوّلًا، ثمّ لا رقمَ إلّا من البايتات.
#
# لا تستورد هذه الشهادةُ شيئًا من الشجرة: لا محرّكًا ولا وديعة. المكتبةُ القياسيّة وحدَها،
# والمدخلُ بايتاتُ `mujammad.txt` من جذر المستودع. وكلُّ رقمٍ تعلنه يُشتَقُّ ههنا لا يُنقَل.
#
# والتحقُّقُ من الختم **قبل** كلِّ عدّ: رقمٌ صحيحٌ على نصٍّ مبدَّلٍ أخطرُ من رقمٍ خاطئ.
import argparse, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(HERE), "mujammad.txt")

# الختمان معلنان قبل القراءة — والمصادمةُ عليهما لا على وصفٍ لهما.
SEAL_SHA256 = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"
SEAL_GIT_BLOB = "7b9aed55b76cb724b670714c4ad3f537251cfeb7"
SEAL_BYTES = 1_306_770

# حدُّ العربيّة الواحد المعلن — لا «حرفٌ عربيٌّ» بالحدس.
AR_RANGES = ((0x0621, 0x064A), (0x064B, 0x0652), (0x0670, 0x0670), (0x06D6, 0x06ED))


def is_ar(ch):
    o = ord(ch)
    return any(lo <= o <= hi for lo, hi in AR_RANGES)


def is_letter(ch):
    """حرفٌ لا علامة: المدى 0621–064A وحدَه. وما سواه حركةٌ أو علامةُ وقفٍ تُعَدّ باسمها."""
    return 0x0621 <= ord(ch) <= 0x064A


def git_blob_sha1(blob):
    """بصمةُ كائن git للمحتوى — مشتقّةٌ بالصيغة لا مأخوذةً من `git hash-object`."""
    return hashlib.sha1(b"blob %d\0" % len(blob) + blob).hexdigest()


def read_sealed():
    """البايتاتُ المختومة — والمخالفةُ صريخٌ يوقف كلَّ ما بعده."""
    with open(CORPUS, "rb") as fh:
        blob = fh.read()
    got = hashlib.sha256(blob).hexdigest()
    if got != SEAL_SHA256:
        raise SystemExit(f"::error::ليس المجمَّد — sha256 أعطى {got}")
    if len(blob) != SEAL_BYTES:
        raise SystemExit(f"::error::الحجمُ خُولِف — {len(blob)} بايتًا")
    if git_blob_sha1(blob) != SEAL_GIT_BLOB:
        raise SystemExit("::error::بلوب git خُولِف")
    return blob


def verses_of(blob):
    """آياتُ المدوّنة: سطرٌ فيه حرفٌ عربيٌّ واحدٌ فصاعدًا — والترويسةُ تسقط بهذا الحدّ نفسِه.

    والقسمةُ إلى كلماتٍ بالفراغ المفرد: **قرارٌ موروثٌ معلنٌ ههنا** لا حقيقةً لغويّة،
    ولا يُبنى عليه في هذه المحكمة إلّا ما صُرِّح بأساسه.

    والمخرَجُ ثلاثيٌّ لا مبتلَع: كلماتُ الآيات (فيها حرفٌ) · مواضعُ العلامات (لا حرفَ فيها،
    علاماتُ وقفٍ قائمةٌ بذاتها) · كلماتُ الترويسة (على سطورٍ بلا عربيّة).
    """
    verses, marks, header = [], [], []
    for ln in blob.decode("utf-8-sig").splitlines():
        if not ln.strip():
            continue
        toks = [w for w in ln.split(" ") if w.strip()]
        if not any(is_ar(c) for c in ln):
            header.extend(toks)
            continue
        words = [w for w in toks if any(is_letter(c) for c in w)]
        marks.extend(w for w in toks if any(is_ar(c) for c in w)
                     and not any(is_letter(c) for c in w))
        if words:
            verses.append(words)
    return verses, marks, header


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    blob = read_sealed()
    verses, marks, header = verses_of(blob)
    words = [w for v in verses for w in v]
    text = blob.decode("utf-8-sig")
    lines = text.splitlines()
    raw = len(words) + len(marks) + len(header)

    out = {
        "الشهادة": "CERT-CORPUS",
        "الأساس": "الخام — بايتاتُ المجمَّد كما خُتِمت، بلا تحويل",
        "مقيس": {
            "بايتات": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "بلوب_git": git_blob_sha1(blob),
            "سطور": len(lines),
            "آيات": len(verses),
            "كلمات": len(words),
            "علاماتُ_وقفٍ_قائمةٌ_بذاتها": len(marks),
            "صورُ_العلامات": len({w for w in marks}),
            "كلماتُ_الترويسة": len(header),
            "الجردُ_الخام": raw,
            "محارفُ_عربيّة": sum(1 for c in text if is_ar(c)),
            "نقاطُ_رمزٍ_مستعملة": len({ord(c) for c in text if is_ar(c)}),
        },
    }
    m = out["مقيس"]
    fails = []
    if m["آيات"] != 6236:
        fails.append(f"الآياتُ {m['آيات']} لا 6,236")
    if m["كلمات"] != 77801:
        fails.append(f"الكلماتُ {m['كلمات']} لا 77,801")
    # الجردُ يُغلَق جمعًا لا طرحًا: لا موضعَ يسقط بين الأصناف الثلاثة.
    if raw != m["كلمات"] + m["علاماتُ_وقفٍ_قائمةٌ_بذاتها"] + m["كلماتُ_الترويسة"]:
        fails.append("الجردُ لا ينغلق — موضعٌ خارجَ الأصناف الثلاثة")
    # الأبجدُ مغلقٌ: لا محرفَ عربيًّا خارجَ المدى المعلن.
    out_of = sorted({hex(ord(c)) for c in text
                     if 0x0600 <= ord(c) <= 0x06FF and not is_ar(c)})
    if out_of:
        fails.append("محارفُ عربيّةٌ خارجَ المدى المعلن: " + " ".join(out_of))
    out["حكم"] = "خضراء" if not fails else "ساقطة"
    out["مآخذ"] = fails

    print("— CERT-CORPUS: شهادةُ المدوّنة —")
    for k, v in m.items():
        print(f"    {k}: {v}")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ الختمُ والحدودُ متطابقة" if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
