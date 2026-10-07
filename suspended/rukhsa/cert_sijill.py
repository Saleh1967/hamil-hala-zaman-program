# rukhsa/cert_sijill.py — شهادةُ السجلّ: الرخصةُ **جدولٌ بقيود**، لا فقرةُ نثرٍ مطمئنّة.
#
# العطبُ الذي تقتله: نصُّ `LICENSE` يصنّف بالامتداد (`*.py`… MIT · `*.md`… CC BY)، فيبقى
# في الشجرة ما لا يقع في صنفٍ منهما — ويُقرَأ سكوتُ النصِّ عنه إذنًا. فههنا تُعامَل
# الرخصةُ معاملةَ قاعدة بيانات: علاقةٌ ذاتُ مفتاحٍ أوّليّ، وقيودُ سلامةٍ تُفحَص، وقسمةٌ
# تنغلق **جمعًا لا طرحًا** على ملفّات الشجرة كلِّها — فلا صفَّ بلا حكمٍ ولا ملفَّ بلا صفّ.
#
# والحكمُ ثلاثيٌّ (CERT-JABR): ⊥ مُثبَتُ المنع · ⊘ محجورٌ لم يُقَس · ⊤ مُثبَتُ الإذن.
# وكلُّ حكمٍ ههنا **مُشتَقٌّ من بايتات** لا مكتوبٌ بيد: نصُّ المنحة يُفتَّش في بايتات
# `LICENSE`، والأصنافُ تُعَدُّ من `git ls-files`، والحاوياتُ تُوصَل ببيان المصادر ببصماتها.
# والحاوياتُ أُخرِجت من الرأس بصكِّ المالك، فصفوفُها تُقاس من **كائنات التاريخ**: إذ
# خروجُ البايتات لا يُخرِج الحقوق، فالاستثناءُ يبقى صفًّا معدودًا لا صفًّا محذوفًا.
#
# وثلاثُ دعاوى خارجَ هذا الصندوق تُسمّى ولا يُفتى فيها: مدوّناتُ OpenITI على GitHub ·
# مرايا Zenodo · دعوى «CC BY 4.0» الشائعةُ على نصوص OpenITI. وحجرُها **بنيويٌّ لا
# عارض**: هذه الشهادةُ لا تستورد شبكةً البتّة، ويُفحَص ذلك بـ`ast` في بايتاتها نفسِها.
#
# المنهج: بنودُ `burhan/THE-PROOF.md` السبعة — والمتوقَّعُ مسجَّلٌ قبل التشغيل في `CLAIMS`.
import argparse, ast, hashlib, json, os, subprocess, sys

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

# الوحداتُ المعجميّةُ التي تُفتَّش في بايتات LICENSE — شاهدُ المنحة لا اسمُها.
GRANT_WITNESS = {
    "MIT": "Permission is hereby granted, free of charge",
    "CC BY 4.0": "creativecommons.org/licenses/by/4.0",
}

# ما خرج عن صنفَي الامتداد يُسمّى بأعيانه ويُنسَب أصلُه — وملفٌّ يدخل الشجرةَ بلا سطرٍ
# ههنا صريخٌ، لا سكوتٌ يُقرَأ إذنًا. والنسبةُ تُصادَم بوثيقتها المودَعة في الشجرة.
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

# حكمُ كلِّ أصلٍ — تعدادٌ مغلق: أصلٌ خارجَه يُسقِط الشهادة، فلا يُخترَع صنفٌ في الطريق.
ORIGIN_VERDICT = {
    "مُنشَأُ المشروع": SUS,                 # يملكه المشروعُ ولا تسمّيه المنحتان — مسكوتٌ عنه
    "طرفٌ ثالثٌ مودَعٌ ببايتاته": BOT,
    "مشتقٌّ من طرفٍ ثالث": BOT,
    "مستخرَجٌ من حاوية": BOT,
}

# الدعاوى الخارجيّةُ — مضيفُها مسمًّى، وحكمُها محجورٌ بالبناء لا بالتورُّع.
OUTSIDE = (
    ("مدوّناتُ OpenITI على GitHub بلا بيان رخصة", "github.com/OpenITI"),
    ("مرايا Zenodo لإصدارات OpenITI (doi:10.5281/zenodo.3082463) تحمل بيانَ رخصة",
     "zenodo.org"),
    ("نصوصُ OpenITI تحت CC BY 4.0 — الدعوى الشائعة", "خارجَ هذه الشجرة"),
)

# وحداتُ الشبكة — حضورُ واحدةٍ منها يُبطِل دعوى «محجورٌ بالبناء».
NET_MODULES = ("socket", "ssl", "http", "urllib", "urllib2", "requests", "ftplib",
               "telnetlib", "asyncio", "smtplib", "xmlrpc")

# المتوقَّعُ قبل التشغيل — أحكامُ الحزم، لا أعدادَ الملفّات (فتلك تتبدّل بكلِّ إيداع).
EXPECTED_BUNDLES = {
    "ما تمنحه الرخصةُ بنصّها": TOP,
    "الحاوياتُ المستثناة": BOT,
    "مودَعٌ من طرفٍ ثالث": BOT,
    "مُنشَأُ المشروعِ خارجَ صنفَي المنحة": SUS,
    "دعاوى خارجَ هذا الصندوق": SUS,
    "الشجرةُ كلُّها وحدةً واحدة": BOT,
}


def rank(v):
    return ORDER.index(v)


def fold(verdicts):
    """حزمةٌ ⊗: أصغرُ الرتب — وتُصادَم بجمعٍ علائقيٍّ مستقلٍّ في `aggregate`."""
    out = TOP
    for v in verdicts:
        out = out if rank(out) <= rank(v) else v
    return out


def aggregate(verdicts):
    """الجمعُ العلائقيُّ: عدٌّ على الصفوف — طريقٌ ثانٍ إلى الحزمة لا نسخةٌ من الأوّل."""
    counts = {v: sum(1 for x in verdicts if x == v) for v in ORDER}
    if counts[BOT]:
        return BOT
    return SUS if counts[SUS] else TOP


def tracked():
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return sorted(p for p in out.decode("utf-8").split("\0") if p)


def size_of(path):
    return os.path.getsize(os.path.join(ROOT, path))


def manifest_shas():
    """خريطةُ sha256 ⟶ المعرِّف من بيان المصادر — للحاويات المختومة وحدَها."""
    seals = {}
    with open(os.path.join(ROOT, "sources_manifest.tsv"), encoding="utf-8") as fh:
        for line in fh:
            if line.lstrip().startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) >= 9 and f[8].strip() == "مختوم":
                seals[f[7].strip()] = f[0].strip()
    return seals


def sha256_of(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def no_network():
    """حجرُ الدعاوى الخارجيّة بنيويٌّ: لا وحدةَ شبكةٍ في بايتات هذه الشهادة.

    فـ«لم يُفحَص» ههنا خاصّةُ الآلة لا عُذرُ المشغِّل — وتُقرأ بـ`ast` لا بمشطِ نصّ
    (`NET_MODULES` نفسُها سلسلةٌ في هذا الملفّ، فالمشطُ كان سيَعُدَّها إصابة).
    """
    tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return sorted(found & set(NET_MODULES))


def classify(files):
    """قسمةُ الشجرة — كلُّ ملفٍّ في صنفٍ واحدٍ لا غير، والمجموعُ يُصادَم بالمقام."""
    classes = {"MIT": [], "CC BY 4.0": [], "حاويات": [], "خارجَ صنفَي المنحة": []}
    for path in files:
        low = path.lower()
        if low.endswith(MIT_EXT):
            classes["MIT"].append(path)
        elif low.endswith(CC_EXT):
            classes["CC BY 4.0"].append(path)
        elif low.endswith(CONTAINER_EXT):
            classes["حاويات"].append(path)
        else:
            classes["خارجَ صنفَي المنحة"].append(path)
    return classes


def container_rows(seals):
    """صفوفُ الحاويات من كائنات التاريخ — بصكِّ الإخراج لا بمشطِ شجرةِ العمل.

    ولو مُشِّطت الشجرةُ لخَلَت الحزمةُ بعد التنفيذ فانقلب طيُّها ⊤ — أي لصار
    «لا بايتةَ ههنا» قراءةً بإذن. فالمقامُ يُنقَل حيث صارت البايتاتُ ولا يُطوى.
    """
    rows = []
    for entry in ikhraj.CONTAINERS:
        got = ikhraj.retrieve(entry)
        ident = seals.get(entry["sha256"])
        rows.append({
            "المدَّعى": "حاويةٌ لا يملكها المشروعُ فلا يُرخِّصها — أُخرِجت بصكِّ المالك",
            "المحلّ": entry["المسار"],
            "المضيف": "تاريخُ هذا المستودع",
            "ملفّات": 1,
            "بايتات": entry["الطول"] if got["مستردّة"] else 0,
            "الشاهد": (f"ختمٌ في بيان المصادر: {ident} · "
                       f"كائنٌ مستردٌّ من {entry['الإيداع'][:7]}")
            if ident and got["مستردّة"] else "—",
            # الاستثناءُ لا يُقبَل دعوًى: صفٌّ بلا ختمٍ يوصله بالبيان، أو بلا
            # بايتاتٍ تُستردُّ من التاريخ، يبقى محجورًا لا مقضيًّا له.
            "الحكم": BOT if ident and got["مستردّة"] else SUS,
        })
    return rows


def rows_of(classes, license_text, seals):
    """صفوفُ العلاقة — الحكمُ مُشتَقٌّ من بايتاتٍ تُقاس، والشاهدُ مسمًّى في كلِّ صفّ."""
    rows = []
    for grant in ("MIT", "CC BY 4.0"):
        witness = GRANT_WITNESS[grant]
        present = witness in license_text
        rows.append({
            "المدَّعى": f"منحةُ {grant} على صنفها",
            "المحلّ": grant,
            "المضيف": "هذه الشجرة",
            "ملفّات": len(classes[grant]),
            # بايتاتُ صنفَي المنحة **لا تُقاس**، وذلك قيدٌ معلنٌ لا إهمال: وديعةُ هذا
            # البيت ووثيقتُه من صنف CC، فقياسُ بايتاتهما يجعل الوديعةَ تقيس نفسَها
            # فلا تستقرّ على نقطةٍ ثابتة. والمقصودُ ههنا بايتاتُ ما لا يملكه المشروع
            # وهي كلُّها خارجَ الصنفين — فالقيدُ لا يُنقِص من الغرض شيئًا.
            "بايتات": None,
            "الشاهد": f"نصُّ المنحة في LICENSE: «{witness}»",
            "الحكم": TOP if present and classes[grant] else SUS,
        })
    rows.extend(container_rows(seals))
    for path in classes["خارجَ صنفَي المنحة"]:
        origin, doc = REGISTRY.get(path, (None, None))
        ext = os.path.splitext(path)[1] or "بلا امتداد"
        # شاهدُ المسكوتِ عنه مقيسٌ لا مُدَّعًى: امتدادُه ليس في تعدادِ صنفَي المنحة.
        witness = doc or (f"امتدادٌ لا تسمّيه المنحتان: {ext}"
                          if ext not in MIT_EXT + CC_EXT else None)
        rows.append({
            "المدَّعى": f"خارجَ صنفَي المنحة — {origin or 'بلا نسبةٍ في السجلّ'}",
            "المحلّ": path,
            "المضيف": "هذه الشجرة",
            "ملفّات": 1,
            "بايتات": size_of(path),
            "الشاهد": witness or "—",
            "الحكم": ORIGIN_VERDICT.get(origin, SUS),
        })
    for claim, host in OUTSIDE:
        rows.append({
            "المدَّعى": claim,
            "المحلّ": "نصوصٌ خارجَ الشجرة",
            "المضيف": host,
            "ملفّات": 0,
            "بايتات": 0,
            "الشاهد": "لا بايتةَ منه في الشجرة — ولا مِقياسَ لها ههنا",
            "الحكم": SUS,
        })
    return rows


def integrity(rows, files, classes):
    """قيودُ السلامة — كلُّ قيدٍ عددُ مخالفاته، والصفرُ وحدَه يُقبَل."""
    keys = [(r["المدَّعى"], r["المحلّ"]) for r in rows]
    covered = [r["المحلّ"] for r in rows if r["المضيف"] == "هذه الشجرة"
               and r["المحلّ"] not in GRANT_WITNESS]
    in_class = set(classes["MIT"]) | set(classes["CC BY 4.0"])
    return {
        "مفتاحٌ أوّليٌّ مكرَّر": len(keys) - len(set(keys)),
        "حكمٌ خارجَ الحامل": sum(1 for r in rows if r["الحكم"] not in ORDER),
        "صفٌّ بلا شاهد": sum(1 for r in rows if not r["الشاهد"] or r["الشاهد"] == "—"),
        "إذنٌ بلا نصٍّ في LICENSE": sum(
            1 for r in rows if r["الحكم"] == TOP
            and GRANT_WITNESS.get(r["المحلّ"], "") not in (r["الشاهد"] or "")),
        "ملفٌّ خارجَ صنفَي المنحة بلا سطرٍ في السجلّ": sum(
            1 for p in classes["خارجَ صنفَي المنحة"] if p not in REGISTRY),
        "سطرُ سجلٍّ لملفٍّ غائبٍ عن الشجرة": sum(1 for p in REGISTRY if p not in files),
        "أصلٌ خارجَ التعداد المغلق": sum(
            1 for p, (origin, _d) in REGISTRY.items() if origin not in ORIGIN_VERDICT),
        "وثيقةُ نسبةٍ غائبةٌ عن الشجرة": sum(
            1 for _p, (_o, doc) in REGISTRY.items() if doc and doc not in files),
        "ملفٌّ في الشجرة بلا صفّ": len(set(files) - set(covered) - in_class),
        "القسمةُ لا تنغلق جمعًا": int(sum(len(v) for v in classes.values()) != len(files)),
        "وحدةُ شبكةٍ في الشهادة": len(no_network()),
    }


def bundles(rows, classes):
    """الحزمُ — كلُّ واحدةٍ محسوبةٌ بطريقين: طيُّ الشبكة وجمعُ العلاقة، ويُصادَمان."""
    groups = {
        "ما تمنحه الرخصةُ بنصّها": [r for r in rows if r["المحلّ"] in GRANT_WITNESS],
        "الحاوياتُ المستثناة": [r for r in rows
                                if r["المضيف"] == "تاريخُ هذا المستودع"],
        "مودَعٌ من طرفٍ ثالث": [
            r for r in rows if r["المحلّ"] in REGISTRY
            and ORIGIN_VERDICT[REGISTRY[r["المحلّ"]][0]] == BOT],
        "مُنشَأُ المشروعِ خارجَ صنفَي المنحة": [
            r for r in rows if r["المحلّ"] in REGISTRY
            and REGISTRY[r["المحلّ"]][0] == "مُنشَأُ المشروع"],
        "دعاوى خارجَ هذا الصندوق": [r for r in rows
                                    if r["المضيف"] not in ("هذه الشجرة",
                                                           "تاريخُ هذا المستودع")],
        "الشجرةُ كلُّها وحدةً واحدة": [r for r in rows if r["المضيف"] == "هذه الشجرة"],
    }
    out = {}
    for name, group in groups.items():
        verdicts = [r["الحكم"] for r in group]
        out[name] = {
            "صفوف": len(group),
            "طيُّ_الشبكة": fold(verdicts),
            "جمعُ_العلاقة": aggregate(verdicts),
            "بايتاتٌ مقيسة": sum(1 for r in group if r["بايتات"] is not None),
            "بايتات": sum(r["بايتات"] or 0 for r in group),
        }
    return out


# ═══ محاولاتُ التكذيب — حارسٌ لا يَعُدُّ في صورةٍ مكذِّبةٍ حارسٌ بلا مادّة ═══════════
def trials(rows, files, classes):
    ghost = dict(classes)
    ghost["خارجَ صنفَي المنحة"] = classes["خارجَ صنفَي المنحة"] + ["وهمٌ.bin"]
    counted = {
        "ملفٌّ دخل الشجرةَ بلا سطرٍ في السجلّ":
            integrity(rows, files, ghost)["ملفٌّ خارجَ صنفَي المنحة بلا سطرٍ في السجلّ"],
        "صفٌّ حُرِّف حكمُه إلى خارج الحامل":
            integrity([dict(r, **{"الحكم": "مباح"}) for r in rows], files,
                      classes)["حكمٌ خارجَ الحامل"],
        "إذنٌ ادُّعي بلا نصٍّ في LICENSE":
            integrity([dict(r, **{"الحكم": TOP, "الشاهد": "دعوى"}) for r in rows],
                      files, classes)["إذنٌ بلا نصٍّ في LICENSE"],
    }
    return counted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    files = tracked()
    classes = classify(files)
    with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as fh:
        license_text = fh.read()
    rows = rows_of(classes, license_text, manifest_shas())

    fails = []
    constraints = integrity(rows, files, classes)
    for name, broken in constraints.items():
        if broken:
            fails.append(f"قيدُ «{name}» خُولِف في {broken} موضعًا")

    got = bundles(rows, classes)
    for name, b in got.items():
        if b["طيُّ_الشبكة"] != b["جمعُ_العلاقة"]:
            fails.append(f"حزمةُ «{name}»: الطيُّ {b['طيُّ_الشبكة']} والجمعُ "
                         f"{b['جمعُ_العلاقة']} — طريقان لا يلتقيان")
        if EXPECTED_BUNDLES[name] != b["طيُّ_الشبكة"]:
            fails.append(f"حزمةُ «{name}»: المسجَّلُ قبل التشغيل "
                         f"{EXPECTED_BUNDLES[name]} والمقيسُ {b['طيُّ_الشبكة']}")

    counted = trials(rows, files, classes)
    for name, n in counted.items():
        if not n:
            fails.append(f"المحاولة «{name}» لم تُعَدَّ لها مخالفة — حارسٌ أعمى")

    census = {
        "ملفّاتُ الشجرة": len(files),
        "ممنوحٌ بنصِّ الرخصة": len(classes["MIT"]) + len(classes["CC BY 4.0"]),
        "حاوياتٌ في الرأس": len(classes["حاويات"]),
        "خارجَ صنفَي المنحة": len(classes["خارجَ صنفَي المنحة"]),
        "حاوياتٌ مخرَجةٌ مقيسةٌ من التاريخ": got["الحاوياتُ المستثناة"]["صفوف"],
        "صفوفُ العلاقة": len(rows),
        "دعاوى محجورةٌ خارجَ الصندوق": len(OUTSIDE),
        # بايتاتُ ما لا يملكه المشروعُ **في الرأس** — وبايتاتُ الحاويات خرجت منه
        # إلى التاريخ، فلا تُجمَع ههنا وتُعَدُّ في حزمتها وحدَها. والمقامان لا يُخلَطان.
        "بايتاتُ طرفٍ ثالثٍ في الرأس": got["مودَعٌ من طرفٍ ثالث"]["بايتات"],
        "بايتاتُ حاوياتٍ خرجت إلى التاريخ": got["الحاوياتُ المستثناة"]["بايتات"],
    }
    if census["ممنوحٌ بنصِّ الرخصة"] + census["حاوياتٌ في الرأس"] \
            + census["خارجَ صنفَي المنحة"] != census["ملفّاتُ الشجرة"]:
        fails.append("القسمةُ لا تنغلق جمعًا على ملفّات الشجرة")

    out = {
        "الشهادة": "CERT-SIJILL",
        "الأساس": ("بايتاتُ الشجرة وكائناتُ تاريخها — git ls-files وLICENSE "
                   "وبيانُ المصادر وصكُّ الإخراج"),
        "مقيس": census,
        "قيودُ_السلامة": constraints,
        "حزم": got,
        "متوقَّعٌ_قبل_التشغيل": EXPECTED_BUNDLES,
        "محاولاتُ_التكذيب": counted,
        "وحداتُ_شبكةٍ_في_الشهادة": no_network(),
        "صفوف": rows,
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-SIJILL: سجلُّ الدعاوى جدولًا بقيود —")
    print(f"    {census['ملفّاتُ الشجرة']} ملفًّا = {census['ممنوحٌ بنصِّ الرخصة']} ممنوحًا "
          f"+ {census['حاوياتٌ في الرأس']} حاويةً + {census['خارجَ صنفَي المنحة']} خارجَ "
          f"صنفَي المنحة · {len(rows)} صفًّا · {len(constraints)} قيدًا")
    for name, b in got.items():
        print(f"    {b['طيُّ_الشبكة']} {name} ({b['صفوف']} صفًّا · "
              + (f"{b['بايتات']:,} بايتًا)" if b["بايتاتٌ مقيسة"]
                 else "بايتاتُه غيرُ مقيسةٍ بقيدٍ معلن)"))
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ لا ملفَّ بلا صفّ، ولا إذنَ بلا نصّ، ولا دعوى خارجيّةً يُفتى فيها"
          if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
