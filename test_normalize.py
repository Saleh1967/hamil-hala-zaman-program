# test_normalize.py — مصادمةُ عقد normalize.py: كلُّ حكمٍ برقمٍ لا بوصف.
#
# لا شبكةَ ولا مصدرَ مجلوبٌ في المصادمات: الشاهدُ مصنوعٌ هنا ببايتاته، يحمل
# الحالاتِ كلَّها (بوم · ترويسةٌ سليمة · ~~ · # · ‎# |‎ و‎### ||‎ · PageVxxPyy ·
# فراغٌ · نصٌّ عارٍ)، فالأعدادُ المنتظَرةُ معلومةٌ سلفًا لا تُقرأ من المخرَج.
#
# ولا يُمَسُّ في المصادمة ملفٌّ من الشجرة: البناءُ كلُّه في مجلّدٍ مؤقَّت، ويُصادَم
# ذلك في آخره بـgit status على البيان والأختام.
#
# التشغيل:  python test_normalize.py    (ولا اعتمادَ خارجيًّا فيه)
#           pytest test_normalize.py    (يعمل كذلك إن كان pytest حاضرًا)
import atexit
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import normalize as N

# ــ الشاهدُ المصنوع ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# تسعةَ عشرَ سطرًا في المتن، أصنافُها معدودةٌ هنا بالبناء:
#   عنوان 3 (عصًا واحدةٌ مرّتين · عصوان مرّةً) · فقرة 4 · وصل 5 · فراغ 4 · عارٍ 3
HEADER = "\n".join([
    "######OpenITI#",
    "",
    "#META# 000.SortField\t:: Shamela_0000000",
    "#META# Author: مؤلِّفٌ مصنوع",
    "#META# Title: شاهدُ المصادمة",
    "#META#Header#End#",
])
BODY = "\n".join([
    "### | البابُ الأوّل",
    "# فقرةٌ أولى PageV01P001",
    "~~وصلُها",
    "~~ووصلٌ ثانٍ",
    "",
    "### || فصلٌ داخلَه",
    "# فقرةٌ ثانيةٌ PageV01P002",
    "~~وصلُها",
    "",
    "نصٌّ عارٍ بلا وسم",
    "نصٌّ عارٍ آخر",
    "",
    "### | البابُ الثاني",
    "# فقرةٌ ثالثة",
    "~~وصلُها PageV02P015",
    "~~ووصلُها الثاني",
    "",
    "# فقرةٌ رابعة",
    "نصٌّ عارٍ ثالث",
])
WITNESS = HEADER + "\n" + BODY + "\n"

EXPECT = {
    "أسطر": 19,
    "أصناف": {"عنوان": 3, "فقرة": 4, "وصل": 5, "فراغ": 4, "عارٍ": 3},
    "درجاتُ العناوين": {1: 2, 2: 1},
    "ترقيم": 3,
    "أوّلُ ترقيم": "PageV01P001",
    "آخرُ ترقيم": "PageV02P015",
    "ترويسة": 3,
}

TMP = tempfile.mkdtemp(prefix="normalize-test-")
atexit.register(shutil.rmtree, TMP, True)   # لا أثرَ يبقى ولو شُغِّل بـpytest


def path_of(name, data, bom=False):
    p = os.path.join(TMP, name)
    with open(p, "wb") as fh:
        if bom:
            fh.write(b"\xef\xbb\xbf")
        fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))
    return p


def fails_with(code, path):
    """يُشغَّل ويُقاس مخرجُه؛ ودعوى «يخرج بكذا» لا تُصدَّق بقراءة الشيفرة."""
    try:
        N.measure(path)
    except N.NormalizeError as exc:
        assert exc.code == code, f"خرج {exc.code} والمنتظر {code}: {exc.message}"
        return exc
    raise AssertionError(f"لم يسقط أصلًا والمنتظر {code}")


# ــ ① القراءة ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_bom_is_eaten_not_counted():
    """البومُ يُفَكّ ولا يدخل محرفًا في المتن — والملفّان متطابقان بعدَه."""
    plain = N.measure(path_of("plain.txt", WITNESS))
    withbom = N.measure(path_of("bom.txt", WITNESS, bom=True))
    assert withbom["بوم"] is True and plain["بوم"] is False
    assert withbom["بايتات"] == plain["بايتات"] + 3
    assert withbom["محارف"] == plain["محارف"] == len(WITNESS)
    assert withbom["أصناف"] == plain["أصناف"] == EXPECT["أصناف"]


def test_undecodable_byte_falls_with_5():
    """بايتةٌ لا تُفَكّ تُسقِط بموضعها — ولا تُرقَّع بمحرف بدل."""
    raw = WITNESS.encode("utf-8")
    cut = raw.index(N.SEP.encode()) + len(N.SEP)      # حدُّ محرفٍ لا وسطُ متتالية
    exc = fails_with(N.E_DECODE, path_of("bad.txt", raw[:cut] + b"\xff" + raw[cut:]))
    assert str(cut) in exc.message, exc.message


def test_no_replacement_character_anywhere():
    """المصادمةُ على الغياب: محرفُ البدل � لا يدخل نصًّا من هذه الطبقة."""
    text = N.read_text(path_of("plain2.txt", WITNESS))
    assert "\ufffd" not in text


def test_missing_file_is_usage():
    fails_with(N.E_USAGE, os.path.join(TMP, "لا-وجودَ-له.txt"))


# ــ ② حارس NFC ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_non_nfc_falls_with_6():
    """ألفٌ مفكوكةٌ (ا + همزة مركَّبة) تُسقِط الملفَّ معلَنةً لا تُطبَّع صامتة."""
    decomposed = WITNESS.replace("الأوّل", "ا\u0644\u0627\u0654وّل")
    exc = fails_with(N.E_NFC, path_of("nfd.txt", decomposed))
    assert "NFC" in exc.message


def test_nfc_witness_passes():
    assert N.measure(path_of("plain3.txt", WITNESS))["أسطر"] == EXPECT["أسطر"]


# ــ ③ الفاصل ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_separator_absent_falls_with_7():
    fails_with(N.E_HEADER, path_of("nosep.txt", WITNESS.replace(N.SEP, "#META# لا")))


def test_separator_twice_falls_with_7():
    """متنٌ ملصوقٌ: فاصلان — ولا يُحزَر بأوّلِهما."""
    exc = fails_with(N.E_HEADER, path_of("twosep.txt", WITNESS + WITNESS))
    assert "2" in exc.message


def test_header_is_a_dict_and_body_starts_after_it():
    head, body = N.split_header(WITNESS, "شاهد")
    meta, loose = N.parse_meta(head)
    assert len(meta) == EXPECT["ترويسة"]
    assert meta["Author"] == "مؤلِّفٌ مصنوع"
    assert meta["Title"] == "شاهدُ المصادمة"
    assert meta["000.SortField"] == "Shamela_0000000"
    assert loose == ["######OpenITI#"]
    assert body.startswith("### | البابُ الأوّل")
    assert N.SEP not in body


# ــ ④ التصنيف ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_five_kinds_counted_exactly():
    m = N.measure(path_of("plain4.txt", WITNESS))
    assert m["أسطر"] == EXPECT["أسطر"]
    assert m["أصناف"] == EXPECT["أصناف"]
    assert sum(m["أصناف"].values()) == m["أسطر"]


def test_heading_beats_paragraph():
    """العنوانُ يُفحَص قبل الفقرة: لولا ذلك لابتلع ‎#‎ العناوينَ الثلاثةَ كلَّها."""
    assert N.classify("### | باب") == ("عنوان", 1)
    assert N.classify("### || فصل") == ("عنوان", 2)
    assert N.classify("# | بابٌ بعصًا") == ("عنوان", 1)
    assert N.classify("# فقرة") == ("فقرة", 0)
    assert N.classify("~~وصل") == ("وصل", 0)
    assert N.classify("   ") == ("فراغ", 0)
    assert N.classify("نصٌّ عارٍ") == ("عارٍ", 0)


def test_trailing_newline_opens_no_sixth_line():
    """سطرٌ جديدٌ في الآخر ينهي الأخيرَ ولا يفتح فراغًا مختلَقًا."""
    a = N.measure(path_of("nl.txt", WITNESS))
    b = N.measure(path_of("nonl.txt", WITNESS.rstrip("\n")))
    assert a["أسطر"] == b["أسطر"] == EXPECT["أسطر"]


# ــ ⑤ الترقيم ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_pages_extracted_not_deleted():
    """الترقيمُ يُنتزَع حقلًا مستقلًّا، والنصُّ يبقى بعدَه غيرَ منقوص."""
    m = N.measure(path_of("plain5.txt", WITNESS))
    assert m["ترقيم"] == EXPECT["ترقيم"]
    assert m["أوّلُ ترقيم"] == EXPECT["أوّلُ ترقيم"]
    assert m["آخرُ ترقيم"] == EXPECT["آخرُ ترقيم"]
    assert m["بلا ترقيم"] is False
    recs = N.read_lines(N.split_header(WITNESS, "شاهد")[1])
    first = next(r for r in recs if r["ترقيم"])
    assert first["ترقيم"] == ["PageV01P001"]
    assert first["نصّ"] == "# فقرةٌ أولى"
    assert "PageV01P001" in first["خام"]


def test_absent_numbering_is_declared_not_silent():
    """شاهدٌ بلا ترقيمٍ يُعلَن حالًا — وهو حالُ tabari_jamic_tafsir01 في البيان."""
    m = N.measure(path_of("nopage.txt", N.PAGE.sub("", WITNESS)))
    assert m["ترقيم"] == 0 and m["بلا ترقيم"] is True
    assert m["أوّلُ ترقيم"] is None


# ــ ⑥ لا تطبيعَ في هذه الطبقة ــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_letters_are_untouched():
    """العقدُ المعلَن: لا همزةَ تُطوى ولا تشكيلٌ يُجرَّد في هذا الإيداع."""
    letters = "أإآء ى ة ٱ الرَّحْمَٰنِ"
    text = WITNESS.replace("نصٌّ عارٍ ثالث", letters)
    recs = N.read_lines(N.split_header(text, "شاهد")[1])
    assert any(r["نصّ"] == letters for r in recs)
    src = open(os.path.join(ROOT, "normalize.py"), encoding="utf-8").read()
    body = src.split('"""', 1)[0]
    for banned in ("\\u0623", "replace(\"أ\"", "NFKC", "NFD"):
        assert banned not in body, f"أثرُ تطبيعٍ في طبقةٍ عهدُها ألّا تطبّع: {banned}"


# ــ ⑦ المدخل ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_main_exit_codes():
    ok = path_of("main-ok.txt", WITNESS)
    assert N.main([ok]) == 0
    assert N.main(["--json", ok]) == 0
    assert N.main(["--lines", ok]) == 0
    assert N.main([path_of("main-nosep.txt", WITNESS.replace(N.SEP, ""))]) == N.E_HEADER
    # أعلى المخارج يغلب حين تُجمَع الملفّات في نداءٍ واحد.
    assert N.main([ok, path_of("main-bad.txt", b"\xff\xfe")]) == N.E_DECODE


def test_tree_is_untouched():
    """لا وديعةَ ولا بيانَ يُمَسّ بالمصادمة — يُصادَم ذلك بـgit لا بالدعوى."""
    if not shutil.which("git") or not os.path.isdir(os.path.join(ROOT, ".git")):
        return
    out = subprocess.run(
        ["git", "-C", ROOT, "status", "--porcelain", "--",
         "sources_manifest.tsv", "AUDIT-SEALS.md", "fetch_source.sh"],
        capture_output=True, text=True,
    ).stdout.strip()
    assert out == "", f"مُسَّ ملفٌّ مختومٌ بالمصادمة:\n{out}"


# ــ ⑧ الشاهدُ المختومُ الحقيقيُّ — مشروطٌ لا صامت ـــــــــــــــــــــــــــــ
def test_sealed_witness_if_fetchable():
    """ibnhisham_qatr_matn أرخصُ شاهدٍ في البيان (40 كيلوبايت).

    يُجلَب بـfetch_source.sh فيرثَ ثقةَ الحلقة الأولى بدل أن يدّعيَها؛ وإن سقط
    الجلبُ بـ1 (حجبٌ أو شبكة) تُعلَن التخطئةُ ولا تُسقِط ولا تُسكَت عنها.
    """
    sid = "ibnhisham_qatr_matn"
    store = os.path.join(TMP, "store")
    env = dict(os.environ, SOURCES_DIR=store, SOURCES_CACHE=os.path.join(TMP, "cache"))
    got = subprocess.run(
        ["bash", os.path.join(ROOT, "fetch_source.sh"), "--fetch", sid],
        capture_output=True, text=True, env=env, timeout=600,
    )
    if got.returncode != 0:
        print(f"  ⚑ تُخطّيت مصادمةُ {sid}: الجلبُ خرج بـ{got.returncode} "
              f"({got.stderr.strip().splitlines()[-1] if got.stderr.strip() else 'بلا بيان'})")
        assert got.returncode == 1, (
            f"الجلبُ خرج بـ{got.returncode} لا بـ1 — وهذا ليس تعذُّرَ شبكةٍ:\n{got.stderr}"
        )
        return
    m = N.measure(os.path.join(store, f"{sid}.txt"))
    assert m["بايتات"] == 40168
    assert sum(m["أصناف"].values()) == m["أسطر"]
    assert m["أصناف"]["وصل"] > 0 and m["أصناف"]["فقرة"] > 0
    assert m["بلا ترقيم"] is False
    print(f"  ✓ {sid} مختومًا: " + " · ".join(
        f"{k} {m['أصناف'][k]}" for k in N.KINDS) + f" · ترقيم {m['ترقيم']}")


# ــ ⑧ سطرُ العقد — مقاديرُه تُقرأ من بايتات الوثيقة وتُصادَم بمواضعها ــــــــ
def test_contract_line_is_collided():
    """«سطرُ العقد» في SOURCES.md ليس نثرًا يشيخ: كلُّ مقدارٍ فيه يُقرأ من موضعه.

    والعلّةُ ملموسة: سطرُ عقدٍ يُكتَب مرّةً ثمّ يُزاد حقلٌ في البيان أو يُختَم شاهدٌ
    فيبقى السطرُ معروضًا صادقَ الظاهر كاذبَ المقدار. فتُنتزَع الأعدادُ من بايتاته
    هنا وتُصادَم بما تعطيه مواضعُها؛ ولا يُقرَأ مقدارٌ من الوثيقة إلى الحساب.
    """
    doc = open(os.path.join(ROOT, "SOURCES.md"), encoding="utf-8").read()
    rows = {}
    for line in doc.splitlines():
        if line.startswith("| ") and line.count("|") == 5:
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows[cells[0]] = cells[1]
    assert rows, "لا جدولَ في سطر العقد — الحارسُ بلا مادّة"

    manifest = [ln.rstrip("\n").split("\t") for ln in
                open(os.path.join(ROOT, "sources_manifest.tsv"), encoding="utf-8")
                if ln.strip() and not ln.startswith("#")]
    states = [r[8] for r in manifest]
    got = {
        "حقولُ البيان": len({len(r) for r in manifest}) == 1 and len(manifest[0]),
        "شهودٌ مختومون": states.count("مختوم"),
        "معذورون بالاسم": states.count("معذور"),
        "مصادماتُ التقشير": sum(1 for n in globals() if n.startswith("test_")),
    }
    sys.path.insert(0, os.path.join(ROOT, "induction"))
    import seals as S                                  # noqa: PLC0415 — يُحمَّل عند الحاجة
    got["أختامُ [بوّابة] المصدَّرة"] = sum(1 for s in S.SEALS if s["صنف"] == S.GATE)

    for key, value in got.items():
        assert key in rows, f"بندٌ غائبٌ عن سطر العقد: {key}"
        assert rows[key] == str(value), (
            f"سطرُ العقد يعلن «{key} = {rows[key]}» وموضعُه يعطي {value}")

    # المخارجُ المعلنةُ في السطر هي مخارجُ الطبقتين بأعيانها، لا وصفًا لها.
    assert rows["مخارجُ التقشير"] == "`0·2·5·6·7`" and (
        N.E_USAGE, N.E_DECODE, N.E_NFC, N.E_HEADER) == (2, 5, 6, 7)
    fetch = open(os.path.join(ROOT, "fetch_source.sh"), encoding="utf-8").read()
    assert rows["مخارجُ الجلب"] == "`0·1·2·3·4`"
    for name in ("E_FETCH", "E_USAGE", "E_MANIFEST", "E_SEAL"):
        assert name in fetch, f"مخرجٌ معلَنٌ في سطر العقد بلا موضعٍ في fetch_source.sh: {name}"

    # وعددُ مصادمات الجلب يُقاس بتشغيلها لا بعدِّ سطورها.
    if shutil.which("bash"):
        out = subprocess.run(["bash", os.path.join(ROOT, "test_fetch_source.sh")],
                             capture_output=True, text=True, timeout=600)
        assert out.returncode == 0, out.stdout[-400:] + out.stderr[-400:]
        passed = [w for w in out.stdout.split() if w.isdigit()]
        assert rows["مصادماتُ الجلب"] in passed, (
            f"سطرُ العقد يعلن {rows['مصادماتُ الجلب']} مصادمةً للجلب، والتشغيلُ يعطي غيرَها")


# ــ المُشغِّلُ عديمُ الاعتماد ــــــــــــــــــــــــــــــــــــــــــــــــــــ
def run():
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    good = bad = 0
    for name, fn in tests:
        try:
            fn()
        except Exception as exc:                       # noqa: BLE001 — يُعرَض لا يُبتلَع
            bad += 1
            print(f"  ✗ {name}: {exc}", file=sys.stderr)
        else:
            good += 1
            print(f"  ✓ {name}")
    print(f"\nالمطابقُ {good} · المخالفُ {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(run())
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
