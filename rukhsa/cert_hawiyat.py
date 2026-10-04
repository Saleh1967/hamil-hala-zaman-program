# rukhsa/cert_hawiyat.py — شهادةُ الحاويات: «أتبقى الثلاثُ في الشجرة؟» كان سؤالَ مالكٍ،
# **وقد أجاب**: أُخرِجت بصكٍّ موقَّعٍ على بايتاتها (`rukhsa/ikhraj.py`، ٢٠٢٦-١٠-٠٤).
# فصارت هذه الشهادةُ تقيس فارقَ **فعلٍ وقع** لا فارقَ فرضٍ مظنون.
#
# والطريقةُ هي هي، ووجهُها انقلب: الشجرةُ اليوم T بلا حاويات، وتُبنى الشجرةُ المضادّةُ
# T⁺ = T **زائدَ** الحاويات كما كانت قبل الصكّ — فهي الفرضُ الآن، وما كان فرضًا صار
# واقعًا. ثمّ يُحسَب حكمُ كلِّ ملفٍّ في الشجرتين ويُصادَم صفًّا إلى صفّ: فالدعوى
# «خروجُها لا يُغيِّر حكمَ الرخصة» تصير **عددًا** لا طمأنينة — ويبقى قابلًا للتكذيب
# بعد التنفيذ كما كان قبله.
#
# وثلاثةُ أعدادٍ تُغلِق البابَ على الرأي:
#   ① حكمُ الملفّات الباقيةِ في T′ يطابق حكمَها في T — بعدد المطابقات لا بالقول.
#   ② حزمةُ الشجرة تبقى ⊥ بعد خروجها: فخروجُها **ليس كافيًا**، وبقاؤها ليس العلّةَ
#      الوحيدة. والطريقُ إلى ⊤ مقيسٌ بشِقَّيه: حذفُ ما لا يُملَك **وتسميةُ** ما سكتت
#      عنه المنحة — ولا يبلغه أحدُهما وحدَه.
#   ③ استردادُ البصمات لا ينكسر بخروجها: طريقُ `self` في `fetch_source.sh` يقرأ
#      البايتات من **إيداعٍ مثبَّتٍ في التاريخ** لا من شجرة العمل — ويُقاس ذلك
#      بوجود كائنات git أنفسِها، لا بالثقة بالوصف.
#
#   ④ والصكُّ نفسُه مقيسٌ ههنا: ما أُذِن فيه، وما نُفِّذ، وما بقي مستردًّا — تُقرأ
#      قيمُه من `ikhraj.py` بالاستيراد لا بالنقل، فلا يتخلّف رقمٌ عن مصدره.
#
# فالقرارُ كان للمالك، وقد مضى؛ وهذه فاتورتُه **معدودةً بعد التنفيذ** لا موعودةً قبله.
import argparse, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
import ikhraj                      # صكُّ الإخراج — يُستدعى ولا يُنسَخ (§٦)

BOT = "⊥"
SUS = "⊘"
TOP = "⊤"
ORDER = [BOT, SUS, TOP]

MIT_EXT = (".py", ".sh", ".yml")
CC_EXT = (".md", ".json", ".tsv")
CONTAINER_EXT = ".docx"

REGISTRY = {
    ".gitignore": ("مُنشَأُ المشروع", None),
    "LICENSE": ("مُنشَأُ المشروع", None),
    "requirements.txt": ("مُنشَأُ المشروع", None),
    "burhan/SHA256SUMS.txt": ("مُنشَأُ المشروع", None),
    "rukhsa/SHA256SUMS.txt": ("مُنشَأُ المشروع", None),
    "mujammad.txt": ("طرفٌ ثالثٌ مودَعٌ ببايتاته", "MUJAMMAD.md"),
    "induction/mujammad.txt": ("طرفٌ ثالثٌ مودَعٌ ببايتاته", "MUJAMMAD.md"),
    "uthmani.txt": ("طرفٌ ثالثٌ مودَعٌ ببايتاته", "UTHMANI.md"),
    "burhan/mujammad.norm.txt": ("مشتقٌّ من طرفٍ ثالث", "MUJAMMAD.md"),
    "shakhsiyya_j3_matn.txt": ("مستخرَجٌ من حاوية", "SHAKHSIYYA.md"),
    "shakhsiyya_j3_hawashi.txt": ("مستخرَجٌ من حاوية", "SHAKHSIYYA.md"),
}

ORIGIN_VERDICT = {
    "مُنشَأُ المشروع": SUS,
    "طرفٌ ثالثٌ مودَعٌ ببايتاته": BOT,
    "مشتقٌّ من طرفٍ ثالث": BOT,
    "مستخرَجٌ من حاوية": BOT,
}

# المتوقَّعُ قبل التشغيل — أحكامٌ لا أعداد، فالأعدادُ تتبدّل بكلِّ إيداعٍ والأحكامُ لا.
# وما عدا الأحكامِ ثلاثةُ أصفارٍ: صفرُ حاويةٍ في الرأس (الصكُّ منفَّذ)، وصفرُ حكمٍ
# تبدّل بخروجها (البرهانُ قائمٌ بعد التنفيذ)، وصفرُ حاويةٍ انقطع استردادُها.
EXPECTED = {
    "حكمُ الشجرة اليوم": BOT,
    "حكمُ الشجرة لو عادت الحاويات": BOT,
    "حكمُ الشجرة بعد خروج كلِّ ما لا يُملَك": SUS,
    "أحكامٌ تبدّلت بخروج الحاويات": 0,
    "حاوياتٌ في الرأس": 0,
    "حاوياتٌ في الصكِّ لم تُستردّ": 0,
}


def rank(v):
    return ORDER.index(v)


def fold(verdicts):
    out = TOP
    for v in verdicts:
        out = out if rank(out) <= rank(v) else v
    return out


def tracked():
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return sorted(p for p in out.decode("utf-8").split("\0") if p)


def verdict_of(path):
    """حكمُ ملفٍّ واحدٍ — بامتداده وسجلِّ نسبته، لا بموضعه في الشجرة.

    وهذا هو مَحزُّ البرهان: الدالّةُ **لا تقرأ T ولا T′**، فحكمُ الملفّ لا يتعلّق
    بمَن جاوره. ومنه يلزم أن خروجَ غيرِه لا يُبدِّل حكمَه — واللزومُ يُقاس أدناه
    بالمصادمة صفًّا إلى صفّ، لا يُكتفى به استنتاجًا.
    """
    low = path.lower()
    if low.endswith(MIT_EXT) or low.endswith(CC_EXT):
        return TOP
    if low.endswith(CONTAINER_EXT):
        return BOT
    origin, _doc = REGISTRY.get(path, (None, None))
    return ORIGIN_VERDICT.get(origin, SUS)


def size_of(path):
    return os.path.getsize(os.path.join(ROOT, path))


def manifest_self_rows():
    """سطورُ طريق `self` — المعرِّفُ والإيداعُ المثبَّتُ والمسارُ والبلوب والبصمة."""
    rows = []
    with open(os.path.join(ROOT, "sources_manifest.tsv"), encoding="utf-8") as fh:
        for line in fh:
            if line.lstrip().startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) >= 9 and f[1].strip() == "self":
                rows.append({"المعرِّف": f[0].strip(), "الإيداع": f[2].strip(),
                             "المسار": f[4].strip(), "البلوب": f[5].strip(),
                             "sha256": f[7].strip()})
    return rows


def object_exists(oid):
    """هل كائنُ git حاضرٌ في هذا الاستنساخ؟ — تُقاس بالكائن نفسِه لا بوصفه."""
    return subprocess.run(["git", "-C", ROOT, "cat-file", "-e", f"{oid}^{{blob}}"],
                          capture_output=True).returncode == 0


def blob_sha256(oid):
    out = subprocess.run(["git", "-C", ROOT, "cat-file", "blob", oid],
                         capture_output=True)
    if out.returncode != 0:
        return None
    return hashlib.sha256(out.stdout).hexdigest()


def retrieval(rows, containers):
    """استردادُ الحاويات من التاريخ — مقيسًا بالكائنات، لا بالوعد.

    وطريقُ `self` يقرأ من إيداعٍ مثبَّتٍ بأربعين محرفًا؛ فما دام الكائنُ في
    التاريخ بقي المصدرُ مستردًّا ولو خرج الملفُّ من شجرة العمل. والقيدُ المقابلُ
    معلَنٌ لا مطويّ: استنساخٌ ضحلٌ لا يحمل التاريخَ فلا يحمل الكائن.
    """
    measured = []
    for r in rows:
        in_worktree = r["المسار"] in containers
        exists = object_exists(r["البلوب"])
        measured.append({
            "المعرِّف": r["المعرِّف"],
            "مسارُه حاويةٌ في شجرة العمل": in_worktree,
            "كائنُه حاضرٌ في التاريخ": exists,
            "بصمةُ الكائن تطابق البيان": blob_sha256(r["البلوب"]) == r["sha256"]
            if exists else False,
        })
    return measured


def screams(fn, arg):
    """أيصرخ الحارسُ على الصورة المكذِّبة؟ — يُشغَّل ليُقاس، ولا يُفترَض جوابُه."""
    try:
        fn(arg)
    except ikhraj.Scream:
        return True
    return False


def back_in_head(census):
    """نسخةٌ من قياس الصكِّ أُعيدت فيها حاويةٌ إلى الرأس — صورةٌ لا شجرة."""
    broken = json.loads(json.dumps(census, ensure_ascii=False))
    broken["صفوف"][0]["في الرأس"] = True
    broken["خانات"]["حاوياتٌ في الرأس"] = 1
    return broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    files = tracked()
    # الحاوياتُ تُسمّى من الصكِّ لا من مشطِ الشجرة: فبعد التنفيذ لا يجدها المشطُ،
    # ولو عُدَّت بالمشط لصار البرهانُ يخفت كلّما نجح — وهذا عمًى لا نجاح.
    writ = [e["المسار"] for e in ikhraj.CONTAINERS]
    in_head = [p for p in files if p.lower().endswith(CONTAINER_EXT)]
    # الشجرةُ المضادّةُ T⁺: الرأسُ اليومَ زائدَ ما أُخرِج — أي الشجرةُ قبل الصكّ.
    restored = sorted(set(files) | set(writ))

    unowned = [p for p in files if verdict_of(p) == BOT]
    owned_only = [p for p in files if verdict_of(p) != BOT]

    fails = []

    # ① المصادمةُ صفًّا إلى صفّ: حكمُ كلِّ ملفٍّ باقٍ في T يطابق حكمَه في T⁺.
    here = {p: verdict_of(p) for p in files}
    there = {p: verdict_of(p) for p in restored}
    shifted = [p for p in files if here[p] != there[p]]
    if shifted:
        fails.append(f"حكمُ {len(shifted)} ملفًّا تبدّل بخروج الحاويات — البرهانُ ساقط")

    # ② حزمُ الشجرات الثلاث — والطريقُ إلى ⊤ مقيسٌ بشِقَّيه لا مُدَّعًى بأحدهما.
    tree_now = fold(here.values())
    tree_restored = fold(there.values())
    tree_owned = fold([here[p] for p in owned_only])
    silent = [p for p in owned_only if here[p] == SUS]

    # صكُّ الإخراج مقيسٌ بدالّته هو — لا رقمَ يُنقَل عنه ههنا.
    writ_census = ikhraj.census(files)
    unretrieved = [r["المعرِّف"] for r in writ_census["صفوف"] if not r["مستردّة"]]

    measured = {
        "ملفّاتُ الشجرة": len(files),
        "حاوياتٌ في الصكّ": len(writ),
        "حاوياتٌ في الرأس": len(in_head),
        "حاوياتٌ في الصكِّ لم تُستردّ": len(unretrieved),
        "بايتاتُ الحاويات التي خرجت": sum(e["الطول"] for e in ikhraj.CONTAINERS),
        "ملفّاتٌ لا يملكها المشروع": len(unowned),
        "بايتاتُ ما لا يملكه المشروع": sum(size_of(p) for p in unowned),
        "أحكامٌ صُودِمت بين الشجرتين": len(files),
        "أحكامٌ تبدّلت بخروج الحاويات": len(shifted),
        "ملفّاتٌ مسكوتٌ عنها في نصِّ المنحة": len(silent),
        "حكمُ الشجرة اليوم": tree_now,
        "حكمُ الشجرة لو عادت الحاويات": tree_restored,
        "حكمُ الشجرة بعد خروج كلِّ ما لا يُملَك": tree_owned,
    }
    for name, want in EXPECTED.items():
        if measured[name] != want:
            fails.append(f"المتوقَّعُ المسجَّلُ «{name}» = {want} والمقيسُ {measured[name]}")

    # ③ الاستردادُ — طريقُ `self` يقرأ من التاريخ لا من شجرة العمل.
    rows = manifest_self_rows()
    recovery = retrieval(rows, set(writ))
    present = sum(1 for r in recovery if r["كائنُه حاضرٌ في التاريخ"])
    matched = sum(1 for r in recovery if r["بصمةُ الكائن تطابق البيان"])
    if not rows:
        fails.append("لا سطرَ `self` في البيان — الشهادةُ بلا مادّة")
    shallow = subprocess.run(["git", "-C", ROOT, "rev-parse", "--is-shallow-repository"],
                             capture_output=True, text=True).stdout.strip() == "true"
    if present != len(rows) and not shallow:
        fails.append(f"استنساخٌ كاملٌ وفيه {len(rows) - present} كائنًا غائبًا عن التاريخ")
    if matched != present:
        fails.append(f"{present - matched} كائنًا حاضرًا خالفت بصمتُه البيان")

    # ⑤ محاولاتُ تكذيب — كلُّ حارسٍ يَعُدُّ غيرَ الصفر في صورةٍ مكذِّبة.
    trials = {
        "بلوبٌ مختلَقٌ لا وجودَ له في التاريخ":
            int(not object_exists("0" * 40)),
        "شجرةٌ مضادّةٌ أُعيدت إليها الحاويات":
            sum(1 for p in restored if p.lower().endswith(CONTAINER_EXT)),
        # صورةٌ مكذِّبةٌ تُبنى ولا تُدَّعى: حاويةٌ تُعاد إلى الرأس في نسخةٍ من
        # القياس، ثمّ يُسأَل حارسُ الصكِّ نفسُه — أيصرخ؟ فإن سكت فهو أعمى.
        "صكٌّ يُدَّعى منفَّذًا وحاويةٌ في الرأس":
            int(screams(ikhraj.guards, back_in_head(writ_census))),
        "حكمُ ملفٍّ لا سطرَ لنسبته في السجلّ":
            int(verdict_of("وهمٌ.bin") == SUS),
    }
    for name, n in trials.items():
        if not n:
            fails.append(f"المحاولة «{name}» لم تُعَدَّ لها مخالفة — حارسٌ أعمى")

    out = {
        "الشهادة": "CERT-HAWIYAT",
        "الأساس": "بايتاتُ الشجرة وكائناتُ تاريخها — لا شبكةَ ولا نقلَ عن وصف",
        "مقيس": measured,
        "متوقَّعٌ_قبل_التشغيل": EXPECTED,
        "صكُّ_الإخراج": {
            "المالك": ikhraj.WRIT["المالك"],
            "التاريخ": ikhraj.WRIT["التاريخ"],
            "نصُّ_الإذن": ikhraj.WRIT["نصُّ_الإذن"],
            "حدُّ_الإذن": ikhraj.WRIT["حدُّ_الإذن"],
            "خانات": writ_census["خانات"],
        },
        "استردادُ_طريقِ_self": {"سطور": len(rows), "كائناتٌ حاضرة": present,
                                "بصماتٌ طابقت البيان": matched,
                                "استنساخٌ ضحلّ": shallow, "تفصيل": recovery},
        "الطريقُ_إلى_⊤": {
            "حذفُ ما لا يُملَك": {"ملفّات": len(unowned),
                                  "بايتات": measured["بايتاتُ ما لا يملكه المشروع"],
                                  "يبلغ ⊤ وحدَه": tree_owned == TOP},
            "تسميةُ المسكوتِ عنه في نصّ المنحة": {"ملفّات": len(silent),
                                                  "أسماء": silent},
        },
        "خلاصةٌ_مقيسة": (
            "الحاوياتُ أُخرِجت بصكٍّ موقَّعٍ على بايتاتها، وبايتاتُها مستردَّةٌ من "
            "التاريخ مصادَمةً بختمها الثلاثيّ. وخروجُها لم يُبدِّل حكمَ ملفٍّ واحدٍ "
            "من الباقي ولم يبلغ بالشجرة ⊤ — فكان قرارَ مالكٍ لا يقتضيه الجبرُ ولا "
            "يمنعه، وقد مضى على فاتورةٍ معدودةٍ لا مظنونة"),
        "محاولاتُ_التكذيب": trials,
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-HAWIYAT: الحاوياتُ قياسًا مضادًّا للواقع بعد التنفيذ —")
    print(f"    T (اليوم، بلا حاويات): {len(files)} ملفًّا ⟶ {tree_now} · "
          f"T⁺ (لو عادت): {len(restored)} ملفًّا ⟶ {tree_restored} · "
          f"T″ (بلا ما لا يُملَك): {len(owned_only)} ملفًّا ⟶ {tree_owned}")
    print(f"    أحكامٌ صُودِمت: {len(files)} · تبدّل منها "
          f"{len(shifted)} — فخروجُها لم يمسّ حكمَ غيرِها")
    print(f"    صكُّ الإخراج: {measured['حاوياتٌ في الصكّ']} مأذونًا فيها · "
          f"{measured['حاوياتٌ في الرأس']} في الرأس · "
          f"{measured['بايتاتُ الحاويات التي خرجت']:,} بايتةً خرجت")
    print(f"    استردادُ self: {present}/{len(rows)} كائنًا في التاريخ · "
          f"{matched} بصمةً طابقت البيان")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ الصكُّ منفَّذٌ — والفاتورةُ معدودةٌ لا مظنونة"
          if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
