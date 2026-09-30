# burhan/cert_boundary.py — CERT-W2: فحصُ مبرهنات الحدود الثلاث — تحقُّقٌ لا اكتشاف.
#
# التفسيرُ مُشتقٌّ من الجبر قبل هذا الفحص، وتوقُّعاتُه **مكتوبةٌ في بايتات هذا الملفّ**
# في `CLAIMS` أدناه قبل أن يُشغَّل — فما وافقها فتحقُّق، وما خالفها **سقوطُ قيدٍ يُسجَّل
# بعدده ولا يُصحَّح خُفيةً**، ويُعاد إعلانُه بندًا جديدًا إن أُريد.
#
# «السكونُ الذرّيّ» معرَّفٌ حدًّا واحدًا: علامةُ سكونٍ (0652) **مرسومةٌ في الخام**.
# فما وُلِّد بفكِّ الشدّة (R5) أو بنونِ التنوين (R4) أو بتصريح العُري ليس ذرّيًّا — والخلطُ
# بينهما هو بعينه ما صنع وهمَ 839.
#
# الأساسُ معلن: **الخام**. ولا يدخل تحويلٌ تطبيعيٌّ شاهدًا هنا.
import argparse, collections, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(os.path.dirname(HERE), "mujammad.txt")
SEAL_SHA256 = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"

AR_RANGES = ((0x0621, 0x064A), (0x064B, 0x0652), (0x0670, 0x0670), (0x06D6, 0x06ED))
VOWELS = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TANWIN = {0x064B: "فتحة", 0x064C: "ضمة", 0x064D: "كسرة"}
SHADDA = 0x0651
DAGGER = 0x0670
SUKUN_MARK = 0x0652   # علامةُ السكون المرسومة — وSUKUN في سائر الشهادات اسمُ الحال «سكون»

# المبنيُّ المسمّى بعينه: لامُ الأمر — قائمةٌ **مغلقةٌ موروثةٌ بالاسم** لا تُوسَّع عند السقوط.
# وشرطُ البند أن تُستنفَد استنفادًا: لا موضعَ خارجَها، ولا عضوَ فيها بلا موضع.
LAM_AMR = ("لْيَقْطَعْ", "لْيَقْضُوا")

# حدُّ «الصغير» موروثٌ لا مُنتقًى للحظة: 1,000 هو حدُّ المقام في `ihala_gate.MIN_N`
# الذي يُسعَّر به كلُّ ميدانٍ في هذه الشجرة. ويُصادَم معه حدٌّ ثانٍ (عُشرُ المواضع)
# حتّى لا يكون الحكمُ رهنَ اختيارِ عتبةٍ واحدة.
SMALL_CEILING = 1000
SMALL_FRACTION = 0.10

# ═══ التوقُّعاتُ المشدودةُ — مكتوبةٌ قبل التشغيل، وكلُّ بندٍ يُحكَم عليه وحدَه ═══
CLAIMS = {
    "① الابتداء": {
        "البيان": "لا تُبتدأ كلمةٌ بسكونٍ ذرّيّ",
        "المتوقَّع": "مبتدآتٌ بالسكون الذرّيّ بعد فرز المبنيّات (لامُ الأمر) = 0",
        "الأساس": "الخام",
    },
    "② الوصل": {
        "البيان": "لا يلتقي ساكنان عند الوصلة — استتباعًا لا استقلالًا",
        "المتوقَّع": "لقاءُ الوصلة = 0، وعلّتُه خلوُّ الطرف الثاني وحدَه لا خلوُّ الطرفين",
        "الأساس": "الخام",
    },
    "③ الخاتمة": {
        "البيان": "السكونُ الذرّيُّ في الخاتمة صنفٌ شاذٌّ مسجَّلٌ باسمه",
        "المتوقَّع": f"مواضعُه أقلُّ من {SMALL_CEILING:,} **و** دون {SMALL_FRACTION:.0%} من الكلمات",
        "الأساس": "الخام",
    },
    "④ الوقفُ على مشتقّ": {
        "البيان": "خاتمةُ الآية تقف على مشتقٍّ (تنوين) في نحو ألفٍ من الستة آلاف",
        "المتوقَّع": "آياتٌ خاتمتُها منوَّنةٌ بين 800 و1,300",
        "الأساس": "الخام",
    },
}

# بندٌ خامسٌ **معلَّقٌ لا يُحكَم به**: مواصفتُه وخاصّيتُه قائمتان، ولا «متوقَّعَ» أُعلِن قبل
# تشغيله — فيبقى معلَّقًا بنصِّ المادة الثالثة، ويُعرَض رقمُه ولا يُعَدُّ برهانًا.
SUSPENDED = {
    "⑤ فصلُ الخاتمة عن موضع الإعراب": {
        "المواصفة": "هياكلُ الخاتمةِ الساكنةِ ⟷ هياكلُ الخاتمةِ المنوَّنة",
        "الخاصّية": "حجمُ تقاطعهما",
        "الحال": "معلَّق — لا بندَ متوقَّعٍ سابقًا للتشغيل، فلا يُحتَجُّ برقمه",
    },
}


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


def marked(word):
    """الكلمةُ ⟼ [(حرف، علاماتُه كلُّها)] — والعلاماتُ كلُّها لا أوّلُها، فلا تُبتلَع ثانيةٌ."""
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
        out.append((ch, ms))
        i += 1
    return out


def atomic_sukun(marks):
    """سكونٌ ذرّيٌّ: علامةُ 0652 مرسومةٌ في الخام — لا مولَّدةٌ بشدّةٍ ولا بتنوينٍ ولا بعُري."""
    return SUKUN_MARK in marks


def skeleton(word):
    return "".join(c for c in word if is_letter(c))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    verses = verses_of(read_sealed())
    fails, rows = [], {}

    initial = collections.Counter()
    final = collections.Counter()
    verse_final_tanwin = 0
    fin_skel, tan_skel = set(), set()
    words_total = 0

    for verse in verses:
        for w in verse:
            us = marked(w)
            if not us:
                continue
            words_total += 1
            if atomic_sukun(us[0][1]):
                initial[w] += 1
            if atomic_sukun(us[-1][1]):
                final[w] += 1
                fin_skel.add(skeleton(w))
            if any(m in TANWIN for m in us[-1][1]):
                tan_skel.add(skeleton(w))
        last = marked(verse[-1])
        if last and any(m in TANWIN for m in last[-1][1]):
            verse_final_tanwin += 1

    # ── ① الابتداء: الاستثناءُ يُستنفَد استنفادًا، فلا بقيّةَ ولا عضوٌ بلا موضع ──
    built = {w: c for w, c in initial.items() if w in LAM_AMR}
    residue = {w: c for w, c in initial.items() if w not in LAM_AMR}
    unused = [w for w in LAM_AMR if w not in initial]
    rows["① الابتداء"] = {
        "مبتدآتٌ_بسكونٍ_ذرّيّ": sum(initial.values()),
        "منها_مبنيٌّ_مسمًّى": sum(built.values()),
        "بقيّةٌ_بعد_الفرز": sum(residue.values()),
        "صورُ_البقيّة": sorted(residue),
        "أعضاءُ_القائمةِ_بلا_موضع": unused,
        "حكم": "تحقَّق" if not residue and not unused else "سقط",
    }
    if residue:
        fails.append(f"① بقيَ {sum(residue.values())} مبتدأً ذرّيًّا خارجَ المبنيّات: "
                     f"{sorted(residue)}")
    if unused:
        fails.append(f"① عضوٌ في قائمة المبنيّات بلا موضعٍ في المدوّنة: {unused} — "
                     f"استثناءٌ يُعفي نفسَه")

    # ── ② الوصل: صفرٌ مقيسٌ، **وعلّتُه مفصولةٌ** — وإلّا كان الصفرُ خلوَّ الطرفين ──
    contact = 0
    for verse in verses:
        for a, b in zip(verse, verse[1:]):
            ua, ub = marked(a), marked(b)
            if ua and ub and atomic_sukun(ua[-1][1]) and atomic_sukun(ub[0][1]):
                contact += 1
    # الطرفُ الأوّلُ غيرُ خالٍ قطعًا، فالصفرُ ثمرةُ المبرهنة الأولى لا خواءِ الحدَّين.
    left_factor = sum(final.values())
    right_factor = sum(initial.values()) - sum(built.values())
    # [تكذيب] الآلةُ تعدّ غيرَ الصفر: لو وُسِّع الحدُّ إلى السكون المولَّد بالعُري لظهر لقاء.
    widened = 0
    for verse in verses:
        for a, b in zip(verse, verse[1:]):
            ua, ub = marked(a), marked(b)
            if not ua or not ub:
                continue
            la = atomic_sukun(ua[-1][1])
            rb = not ub[0][1] or atomic_sukun(ub[0][1])      # عُريٌ أو سكونٌ — حدٌّ موسَّع
            widened += la and rb
    rows["② الوصل"] = {
        "لقاءُ_الوصلةِ_الذرّيّ": contact,
        "الطرفُ_الأوّل_(خاتمةٌ_ساكنة)": left_factor,
        "الطرفُ_الثاني_(ابتداءٌ_ساكنٌ_ذرّيّ_بعد_الفرز)": right_factor,
        "الصفرُ_من_الطرفِ_الثاني_وحدَه": "نعم" if (contact == 0 and left_factor > 0
                                                   and right_factor == 0) else "لا",
        "تكذيبٌ_بحدٍّ_موسَّع_(عُريٌ_كسكون)": widened,
        "حكم": "تحقَّق استتباعًا" if (contact == 0 and left_factor > 0
                                       and right_factor == 0) else "سقط",
    }
    if contact:
        fails.append(f"② لقاءُ الوصلة {contact} لا صفر")
    if left_factor == 0:
        fails.append("② الصفرُ خواءُ الطرفين لا استتباع — البرهانُ تحصيلُ حاصل")
    if widened == 0:
        fails.append("② الآلةُ لا تعدّ غيرَ الصفر ولو وُسِّع الحدّ — حارسٌ بلا مادّة")

    # ── ③ الخاتمة: التوقُّعُ المشدودُ يُقاس بحدَّين، فلا يكون الحكمُ رهنَ عتبةٍ واحدة ──
    fin_n = sum(final.values())
    frac = fin_n / words_total
    small = fin_n < SMALL_CEILING and frac < SMALL_FRACTION
    rows["③ الخاتمة"] = {
        "خاتمةٌ_بسكونٍ_ذرّيّ": fin_n,
        "صورُها": len(final),
        "هياكلُها": len(fin_skel),
        "نسبتُها_من_الكلمات": round(frac, 4),
        "حدُّ_الصغر_الموروث": SMALL_CEILING,
        "حدُّ_الكسر": SMALL_FRACTION,
        "أكثرُها_ورودًا": [{"صورة": w, "مواضع": c} for w, c in final.most_common(8)],
        "حكم": "تحقَّق" if small else "سقط",
        "أثرُ_السقوط": None if small else (
            "القيدُ «شاذٌّ صغيرٌ» ساقطٌ بعدده — والخاتمةُ الساكنةُ صنفٌ عامرٌ لا شاذّ. "
            "ولا يُصحَّح القيدُ ههنا: يُعاد إعلانُه بندًا متوقَّعًا جديدًا إن أُريد."),
    }

    # ── ④ الوقفُ على مشتقّ ────────────────────────────────────────────────────
    band = 800 <= verse_final_tanwin <= 1300
    rows["④ الوقفُ على مشتقّ"] = {
        "آياتٌ_خاتمتُها_منوَّنة": verse_final_tanwin,
        "الآيات": len(verses),
        "النطاقُ_المعلن": [800, 1300],
        "حكم": "تحقَّق" if band else "سقط",
    }

    # ── ⑤ المعلَّق: يُعرَض رقمُه ولا يُحتَجُّ به ────────────────────────────────
    suspended = dict(SUSPENDED["⑤ فصلُ الخاتمة عن موضع الإعراب"])
    suspended.update({
        "هياكلُ_الخاتمةِ_الساكنة": len(fin_skel),
        "هياكلُ_الخاتمةِ_المنوَّنة": len(tan_skel),
        "التقاطع": len(fin_skel & tan_skel),
        "صورُ_التقاطع": sorted(fin_skel & tan_skel)[:10],
    })

    # الحَكَمُ على الشهادة **آلتُها لا نتيجتُها**: بندٌ ساقطٌ يُسجَّل بعدده ولا يُسقِطها،
    # وإنّما يُسقِطها أن تعجز عن الحكم أو أن يصير حارسٌ بلا مادّة.
    broken = [k for k, v in rows.items() if v["حكم"] == "سقط"]
    if not rows["③ الخاتمة"]["حكم"]:
        fails.append("بندٌ بلا حكم")

    out = {
        "الشهادة": "CERT-W2",
        "الأساس": "الخام — والسكونُ الذرّيُّ علامةٌ مرسومةٌ لا مولَّدة",
        "دعاوى_مسجَّلةٌ_قبل_التشغيل": CLAIMS,
        "بنود": rows,
        "معلَّق": suspended,
        "مقيس": {
            "بنودٌ_محكومة": len(rows),
            "بنودٌ_تحقَّقت": len(rows) - len(broken),
            "بنودٌ_ساقطة": len(broken),
            "أسماءُ_الساقطة": broken,
            "بنودٌ_معلَّقة": 1,
        },
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-W2: مبرهنات الحدود الثلاث —")
    for name, r in rows.items():
        print(f"    {name}: {r['حكم']}")
        for k, v in r.items():
            if k in ("حكم", "أكثرُها_ورودًا", "أثرُ_السقوط") or v in (None, [], {}):
                continue
            print(f"        {k}: {v:,}" if isinstance(v, int) else f"        {k}: {v}")
        if r.get("أثرُ_السقوط"):
            print(f"        ⚑ {r['أثرُ_السقوط']}")
    print(f"    ⑤ [معلَّق] تقاطعُ هياكلِ الخاتمتين: {suspended['التقاطع']} "
          f"من {suspended['هياكلُ_الخاتمةِ_الساكنة']} — يُعرَض ولا يُحتَجُّ به")
    for f in fails:
        print(f"::error::{f}")
    print(f"    {'✓' if not fails else '✗'} بنودٌ تحقَّقت "
          f"{out['مقيس']['بنودٌ_تحقَّقت']}/{len(rows)} · ساقطةٌ مسجَّلةٌ بعددها {len(broken)}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
