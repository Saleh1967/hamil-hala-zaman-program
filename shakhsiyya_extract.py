# shakhsiyya_extract.py — بابُ الإيداع: من حاويةٍ مختومةٍ إلى نصٍّ مقيسٍ مختوم.
#
# العلّةُ التي يقتلها هذا الملفّ: «الشخصية الإسلامية ج٣» كانت **حاويةً مختومةً بلا نصٍّ
# مقيس**: بايتاتُ الـdocx مودَعةٌ في تاريخ المستودع (`shakhsiyya_j3` في البيان)، ولا
# أحدَ يدري ما الذي يدخل منها في القياس وما الذي لا يدخل. فكلُّ دعوى تُبنى عليها
# تُبنى على استخراجٍ مجهولِ القاعدة — وذلك بعينه عطبُ `QAC-fork-v0.4` المحجورِ T₃:
# أرقامٌ بلا FROZEN، لا يُعرَف من صحّحها ولا بأيِّ ضابط (`AUDIT-188.md` §١ صفّ ٢).
#
# فالبابُ ههنا واحدٌ لا ثانيَ له: **الحاويةُ ⟵ (المُستخرِجُ المسمّى بإصدارِه) ⟵ النصُّ
# المقيس**. ولا يعبر رقمٌ من الحاوية إلى المشروع إلا عبرَه.
#
# — قرارُ الاستخراج، موقَّعٌ قبل أيِّ قياس (خمسةُ أحكامٍ لا سادسَ لها) —
#   ① **المتنُ يدخل** — ففيه شواهدُ الدعاوى: الشعرُ والنثرُ والحديثُ المقتبسُ في المتن.
#   ② **الحواشي تُقصى عن النصِّ المقيس معدودةً بالاسم، وتُستخرَج تيارًا ثانيًا يُودَع
#      وديعةً مستقلّةً بختمِها** — مقامٌ نائمٌ لا يدخل الحكمَ ولا يُهدَر.
#   ③ **الترويساتُ والتذييلاتُ وأرقامُ الصفحات تُقصى معدودةً** — ضجيجُ إنتاجٍ لا لغةَ فيه.
#   ④ **الرسومُ والصورُ وصناديقُ النصِّ تُقصى معدودةً** — ولا OCR البتّة؛ ومن أراد نصَّها
#      فبابُ مقامٍ جديدٍ بفاتورتِه.
#   ⑤ **الجداولُ تُقصى معدودةً بالاسم والأبعاد**، ويُرفَع إلى المالك ما أظهرَ العدُّ نفسُه
#      أنّه يحمل متنًا — مراجعةٌ معلنةٌ لا حلقةُ انتظار (`tables_review`).
# وقاعدةُ الاستخراج كلُّها مجمَّدةٌ في `FROZEN` بحقلِها الرابع، ولا تُبدَّل إلا بيدٍ معلنة:
# فمن بدّلها انزاح النصُّ، ومن أزاح النصَّ سقط الختمُ صريخًا في CI قبل أيِّ دعوى.
#
# — وما لا يُبتلَع ولو لم يذكره القرار —
#   • **رموزُ الخطوط** (`w:sym`): محارفُ خطٍّ مزخرفٍ لا نقاطُ شيفرةٍ عربية، وترجمتُها
#     إلى ﴿﴾ حزرٌ لا قياس. فتُقصى من النصّ و**تُعَدُّ بخطِّها ومحرفِها** في الدفتر،
#     وتُترَك دَينًا مسمًّى لبابِ مقامٍ لاحقٍ بفاتورتِه — لا تُترجَم في الظلام.
#   • **الفقراتُ الخاوية** و**حقولُ Word** (`fldChar`/`instrText`): تُقصى معدودةً.
#
# — ولا تطبيعَ البتّة، والتخالفُ يُقاس ولا يُطوى —
# المستخرَجُ **غيرُ مطبَّعٍ NFC**، وهذا معدودٌ لا مستور: 305 أسطرٍ تنزاح تحت NFC،
# وكلُّها **ترتيبُ علامتين** (الشدّةُ قبل الحركة: 0651 ثمّ 064E وأخواتُها) — و**صفرُ
# تأليفٍ**: لا يتبدّل محرفٌ ولا يُدمَج حرفان في واحد. فالوديعةُ تُودَع كما استُخرجت،
# ويُصادَم كلُّ سطرٍ بجردِ نقاطِه: فإن غيّر NFC جردَ سطرٍ واحدٍ سقط البناءُ بالمخرج 6،
# لأنّ ذاك تبديلُ حروفٍ لا إعادةُ ترتيب. (وهذا بابُ الشدّة نفسُه الذي قِيس في
# `alama_layer.py` — يُعلَن ههنا بمقداره ولا يُسوَّى في الظلام.)
#
# — الأختامُ مصدرُ حقيقةٍ واحدٌ ههنا —
# `CONTAINER_*` ختمُ الحاوية منقولٌ عن `sources_manifest.tsv` ويُصادَم ببايتاتها، و
# `MATN_*`/`HAWASHI_*` ختما الوديعتين. وتقرؤها `SHAKHSIYYA.md` وخطوةُ CI من هذا
# الملفّ نفسِه — لا نسخةٌ ثانيةٌ تتخلّف.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 الحاويةُ خالفت ختمَها · 5 بايتةٌ لا تُفَكّ
#          · 6 المستخرَجُ يتبدّل تحت NFC تأليفًا (لا ترتيبًا) — أي أنّ حرفًا تغيّر
#          · 7 وديعةٌ خالفت ما يُنتجه المُستخرِج.
# (وهي غيرُ مخارج `fetch_source.sh` وغيرُ مخارج `normalize.py` عمدًا — ثلاثُ طبقاتٍ
#  لا تُخلَط عقودُها.)
#
# التشغيل:
#   python shakhsiyya_extract.py                 تقريرٌ معدود
#   python shakhsiyya_extract.py --json <ملفّ>   الأعدادُ نفسُها JSON
#   python shakhsiyya_extract.py --check         يصادم الوديعتين المودَعتين بفارق صفر
#   SHAKHSIYYA_EMIT_OWNER=1 python shakhsiyya_extract.py --emit   كتابةُ الوديعتين بيد المالك
import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

E_USAGE = 2
E_CONTAINER = 3
E_DECODE = 5
E_NFC = 6
E_DEPOSIT = 7

TOOL_NAME = "shakhsiyya_extract"
TOOL_VERSION = "1.0"

ROOT = os.path.dirname(os.path.abspath(__file__))

# ــ الحاوية: ختمُها منقولٌ عن البيان بحرفه، ويُصادَم ببايتاتها قبل أيِّ عدّ ــــــــــ
CONTAINER = "الشخصية الاسلامية الجزء الثالث ورد (2).docx"
CONTAINER_ID = "shakhsiyya_j3"                  # سطرُه في sources_manifest.tsv
CONTAINER_BLOB = "3529f2f21e53391e4c11caa64adf38bc86713814"
CONTAINER_BYTES = 673537
CONTAINER_SHA256 = "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd"

# الطبعةُ مقيسةٌ من بايتات الحاوية لا منقولةٌ عن دعوى: هذه شواهدُها في صفحة العنوان،
# ويُعَدُّ حضورُ كلِّ واحدٍ منها في `edition_marks` — فغيابُ واحدٍ يُعلَن ولا يُطوى.
EDITION_MARKS = ("الجـزء الثالث", "أصول الفقه", "الطبعة الثالثة", "1426",
                 "معتمدة", "حـزب التحـريـر", "دار الأمّـة")

# ــ الوديعتان: تيارُ المتن (يدخل القياس) وتيارُ الحواشي (مقامٌ نائمٌ لا يحكم) ـــــــــ
MATN = "shakhsiyya_j3_matn.txt"
MATN_BYTES = 1241712
MATN_SHA256 = "520b8e9d55135217d2c07bf521a63ed93431d46bd5cdf16f360c915d8bbfc783"

HAWASHI = "shakhsiyya_j3_hawashi.txt"
HAWASHI_BYTES = 0
HAWASHI_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# ــ أجزاءُ الحاوية: ما يُقرأ منها وما يُقصى معدودًا ـــــــــــــــــــــــــــــــــــ
PART_BODY = "word/document.xml"
PART_FOOTNOTES = "word/footnotes.xml"
PART_ENDNOTES = "word/endnotes.xml"
# الترويساتُ والتذييلاتُ (الحكم ③): تُعَدُّ بأسمائها ولا يدخل منها محرف.
PART_CHROME = ("word/header", "word/footer")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
# أشجارٌ لا يُقرأ منها محرفٌ البتّة (الحكم ④): الرسمُ والصورةُ وصندوقُ النصّ.
DRAWN = (W + "drawing", W + "pict", W + "object",
         "{http://schemas.microsoft.com/office/word/2010/wordprocessingShape}txbx",
         "{urn:schemas-microsoft-com:vml}textbox")

FROZEN = {
    "بصمة": {"الحاوية": CONTAINER_SHA256, "المتن": MATN_SHA256,
             "الحواشي": HAWASHI_SHA256},
    "طول": {"الحاوية": CONTAINER_BYTES, "المتن": MATN_BYTES,
            "الحواشي": HAWASHI_BYTES},
    "مصدر": (f"{CONTAINER} — مودَعةٌ في تاريخ هذا المستودع ومختومةٌ في "
             f"sources_manifest.tsv باسم {CONTAINER_ID} (repo=self)؛ "
             "الشخصيةُ الإسلامية ج٣ (أصول الفقه)، الطبعةُ الثالثة 1426هـ/2005م "
             "(معتمدة)، دار الأمّة — والطبعةُ مقيسةٌ من بايتات الحاوية لا منقولة"),
    "مَن استخرج وبأيِّ ضابط": (
        f"{TOOL_NAME} v{TOOL_VERSION} بالمكتبة القياسية وحدَها (zipfile + "
        "ElementTree) — لا تبعيةَ خارجيةٌ يزيحها إصدارُها في الظلام. "
        "وضابطُه الأحكامُ الخمسةُ الموقَّعةُ قبل القياس: المتنُ يدخل · الحواشي "
        "تيارٌ ثانٍ مختومٌ لا يحكم · الترويساتُ والتذييلاتُ تُقصى معدودةً · "
        "الرسومُ والصناديقُ تُقصى معدودةً بلا OCR · الجداولُ تُقصى معدودةً "
        "بأبعادها ويُرفَع إلى المالك ما أظهر العدُّ أنّه متن. "
        "ولا تطبيعَ البتّة: الوديعةُ كما استُخرجت، وتخالفُها عن NFC مقيسٌ "
        "بصنفه — ترتيبُ علامتين يُعَدّ ويُعلَن، وتأليفُ حرفٍ يُسقِط البناءَ صريخًا."),
}


class ExtractError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ــ ① الحاوية بالبصمة أوّلًا، ولا استخراجَ على بديلٍ صامت ــــــــــــــــــــــــــــ
def container_from_history():
    """بايتاتُ الحاوية من كائن تاريخ هذا المستودع — بلا شبكةٍ وبلا شجرةِ عمل.

    الحاويةُ أُخرِجت من الرأس بصكِّ المالك (`rukhsa/ikhraj.py`)، وبايتاتُها
    باقيةٌ في التاريخ. والكائنُ يُطلَب ببصمته الأربعينيّة المختومة أعلاه لا
    بمسارٍ في شجرةٍ قد تتبدّل — فالمطلوبُ بايتاتٌ بعينها لا ملفٌّ باسمه.
    """
    run = subprocess.run(["git", "-C", ROOT, "cat-file", "blob", CONTAINER_BLOB],
                         capture_output=True)
    if run.returncode != 0:
        raise ExtractError(
            E_CONTAINER,
            f"كائنُ الحاوية {CONTAINER_BLOB[:7]} غائبٌ عن التاريخ — "
            "استنساخٌ ضحلٌّ لا يحمله؛ يُجلَب بـ«git fetch --unshallow»")
    return run.stdout


def read_container(path=None):
    """البايتاتُ من موضعٍ مُعلَن: مسارٌ بيد المستعمِل، أو الرأس، أو التاريخ.

    والطرقُ الثلاثةُ تلتقي عند حارسٍ واحد: الطولُ وsha256 يُصادَمان قبل أن
    يُقرَأ منها محرف — فلا يُغني طريقٌ عن ختمٍ ولا يُرخّص أحدُها بديلًا صامتًا.
    """
    tree = os.path.join(ROOT, CONTAINER)
    if path:
        source = path
    elif os.path.exists(tree):
        source = tree
    else:
        source = f"git:{CONTAINER_BLOB}"

    if source.startswith("git:"):
        raw = container_from_history()
    else:
        try:
            raw = open(source, "rb").read()
        except OSError as exc:
            raise ExtractError(E_CONTAINER,
                               f"تعذّرت قراءةُ الحاوية «{source}»: {exc}")
    if len(raw) != CONTAINER_BYTES:
        raise ExtractError(E_CONTAINER,
                           f"ليست الحاويةَ المختومة — الطول {len(raw)} "
                           f"بإزاء {CONTAINER_BYTES}")
    got = hashlib.sha256(raw).hexdigest()
    if got != CONTAINER_SHA256:
        raise ExtractError(E_CONTAINER,
                           f"ليست الحاويةَ المختومة — البصمة {got} خالفت "
                           f"{CONTAINER_SHA256}")
    return raw, source


def _decode(part, blob):
    try:
        return blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ExtractError(E_DECODE, f"«{part}»: بايتةٌ لا تُفَكّ عند {exc.start} "
                                     f"({exc.reason}) — ولا يُرقَّع بمحرف بدل")


# ــ ② قراءةُ الفقرة: نصٌّ بقاعدةٍ معلنة، والمقصيُّ يُعَدّ ولا يُطوى ــــــــــــــــــــ
def paragraph_text(para, tally):
    """نصُّ فقرةٍ بترتيب المستند. الرسومُ والصناديقُ لا يُقرأ منها محرف (④)،
    ورموزُ الخطوط تُعَدّ بخطِّها ومحرفِها ولا تُترجَم حزرًا."""
    out = []

    def walk(node):
        for child in node:
            tag = child.tag
            if tag in DRAWN:
                tally["مقصيٌّ_رسمًا"] += 1
                tally["محارفُ_الرسوم"] += sum(len(t.text or "")
                                              for t in child.iter(W + "t"))
                continue
            if tag == W + "t":
                out.append(child.text or "")
            elif tag == W + "tab":
                out.append("\t")
            elif tag == W + "br":
                out.append("\n")
            elif tag == W + "sym":
                font = child.get(W + "font") or ""
                char = child.get(W + "char") or ""
                tally["رموزُ_الخطوط"] += 1
                tally.setdefault("رموزٌ_بخطِّها", {})
                key = f"{font}:{char}"
                tally["رموزٌ_بخطِّها"][key] = tally["رموزٌ_بخطِّها"].get(key, 0) + 1
            elif tag in (W + "fldChar", W + "instrText"):
                tally["حقولُ_وورد"] += 1
            elif tag == W + "footnoteReference":
                tally["إحالاتُ_حواشٍ"] += 1
            elif tag == W + "endnoteReference":
                tally["إحالاتُ_خواتم"] += 1
            else:
                walk(child)

    walk(para)
    return "".join(out)


def _lines(text, tally, empty_key):
    """فقرةٌ ⟵ سطورٌ مقيسة: الفاصلُ الداخليُّ سطرٌ، والخاوي يُقصى معدودًا."""
    kept = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            kept.append(line)
        else:
            tally[empty_key] += 1
    return kept


def _tally():
    return {k: 0 for k in ("فقراتُ_المتن", "أسطرُ_المتن", "فقراتٌ_خاوية",
                           "أسطرٌ_خاوية", "جداولُ_مقصاة", "خلايا_مقصاة",
                           "محارفُ_الجداول", "مقصيٌّ_رسمًا", "محارفُ_الرسوم",
                           "رموزُ_الخطوط", "حقولُ_وورد", "إحالاتُ_حواشٍ",
                           "إحالاتُ_خواتم", "أجزاءٌ_مقصاةٌ_إنتاجًا",
                           "حواشٍ_مستخرَجة", "خواتمُ_مستخرَجة")}


def extract(path=None):
    """الحاويةُ ⟵ (تيارُ المتن · تيارُ الحواشي · دفترُ المقصيِّ معدودًا)."""
    raw, source = read_container(path)
    tally = _tally()
    # الصندوقُ يُفتَح على البايتات المصادَمةِ نفسِها لا على مسارٍ يُقرَأ ثانيةً:
    # فبين القياسِ والقراءةِ لا يتسلّل ملفٌّ ثانٍ، وتستوي الطرقُ الثلاثة.
    with zipfile.ZipFile(io.BytesIO(raw)) as box:
        names = box.namelist()
        tally["أجزاءٌ_مقصاةٌ_إنتاجًا"] = sum(
            1 for n in names if n.startswith(PART_CHROME))
        chrome = sorted(n for n in names if n.startswith(PART_CHROME))
        body = ET.fromstring(_decode(PART_BODY, box.read(PART_BODY)))
        notes = {}
        for part, key in ((PART_FOOTNOTES, "حواشٍ_مستخرَجة"),
                          (PART_ENDNOTES, "خواتمُ_مستخرَجة")):
            notes[part] = (ET.fromstring(_decode(part, box.read(part)))
                           if part in names else None)

    # (أ) تيارُ المتن — والجداولُ تُقصى معدودةً بأبعادها (⑤)
    matn, tables = [], []
    for node in body.find(W + "body"):
        if node.tag == W + "tbl":
            rows = node.findall(W + "tr")
            cells = [len(r.findall(W + "tc")) for r in rows]
            text = "".join(t.text or "" for t in node.iter(W + "t"))
            tally["جداولُ_مقصاة"] += 1
            tally["خلايا_مقصاة"] += sum(cells)
            tally["محارفُ_الجداول"] += len(text)
            tables.append({"صفوف": len(rows), "خلايا": cells, "محارف": len(text),
                           "كلمات": len(text.split()),
                           "بصمة": hashlib.sha256(text.encode("utf-8")).hexdigest()})
            continue
        if node.tag != W + "p":
            continue
        kept = _lines(paragraph_text(node, tally), tally, "أسطرٌ_خاوية")
        if kept:
            tally["فقراتُ_المتن"] += 1
            matn.extend(kept)
        else:
            tally["فقراتٌ_خاوية"] += 1
    tally["أسطرُ_المتن"] = len(matn)

    # (ب) تيارُ الحواشي — الفاصلاتُ الصناعيةُ (separator) ليست حاشيةً فلا تُعَدّ منها
    hawashi = []
    for part, key in ((PART_FOOTNOTES, "حواشٍ_مستخرَجة"),
                      (PART_ENDNOTES, "خواتمُ_مستخرَجة")):
        tree = notes.get(part)
        if tree is None:
            continue
        tag = W + ("footnote" if part == PART_FOOTNOTES else "endnote")
        for note in tree.iter(tag):
            if note.get(W + "type"):          # separator · continuationSeparator
                continue
            lines = []
            for para in note.iter(W + "p"):
                lines.extend(_lines(paragraph_text(para, tally), tally,
                                    "أسطرٌ_خاوية"))
            if lines:
                tally[key] += 1
                hawashi.append(f"[{note.get(W + 'id')}] " + " ".join(lines))

    matn_text = ("\n".join(matn) + "\n") if matn else ""
    hawashi_text = ("\n".join(hawashi) + "\n") if hawashi else ""
    nfc = {name: nfc_divergence(text)
           for name, text in (("المتن", matn_text), ("الحواشي", hawashi_text))}
    return {"متن": matn_text, "حواشٍ": hawashi_text, "دفتر": tally,
            "جداول": tables, "ترويساتٌ_وتذييلات": chrome, "تخالفُ_NFC": nfc,
            "حاوية": raw}


def nfc_divergence(text):
    """تخالفُ النصِّ عن NFC مقيسًا بصنفِه — لا مطويًّا ولا مسوّى في الظلام.

    الصنفان لا ثالثَ لهما: **ترتيبٌ** (جردُ نقاط السطر لا يتغيّر، وإنّما ترتيبُ
    علامتين متجاورتين) و**تأليفٌ** (الجردُ نفسُه يتغيّر: حرفٌ تبدّل أو حرفان
    اندمجا). فالأوّلُ يُعَدُّ ويُعلَن بأزواجه، والثاني **يُسقِط البناءَ بالمخرج 6**
    لأنّه تبديلُ حروفٍ لا إعادةُ ترتيب.
    """
    lines = text.splitlines()
    pairs, diverging, composing = {}, 0, 0
    for line in lines:
        folded = unicodedata.normalize("NFC", line)
        if folded == line:
            continue
        diverging += 1
        if sorted(line) != sorted(folded):
            composing += 1
            continue
        for a, b in zip(line, line[1:]):
            ca, cb = unicodedata.combining(a), unicodedata.combining(b)
            if ca and cb and ca > cb:
                key = f"{ord(a):04X}+{ord(b):04X}"
                pairs[key] = pairs.get(key, 0) + 1
    if composing:
        raise ExtractError(E_NFC, f"{composing} سطرًا يتبدّل جردُ نقاطِه تحت NFC — "
                                  "تأليفٌ لا ترتيب، فحرفٌ تغيّر: صريخٌ لا تسوية")
    return {"أسطرٌ_مخالفة": diverging, "تأليف": composing,
            "أسطر": len(lines), "أزواجُ_الترتيب": dict(sorted(pairs.items()))}


# ــ ③ مراجعةُ الجداول: استثناءُ الحكم الخامس — إعلانٌ لا حلقةُ انتظار ـــــــــــــــ
def tables_review(tables):
    """ما أظهرَ العدُّ نفسُه أنّه يحمل متنًا يُرفَع إلى المالك مسمًّى بأبعاده.

    والعدُّ في هذه الحاوية قال: ثلاثةُ جداولَ صفًّا واحدًا وثلاثَ خلايا، فيها كلامٌ
    موزون لا فهرسَ صفحاتٍ — فهي مقصاةٌ بالحكم ⑤ ومرفوعةٌ للمراجعة بالاسم، ولا
    يُبتلَع منها محرفٌ ولا يدخل القياسَ حرفٌ قبل يدٍ معلنة.
    """
    return [t for t in tables if t["كلمات"] >= 4]


def edition_marks(box_text):
    return {mark: box_text.count(mark) for mark in EDITION_MARKS}


def deposit_seal(text):
    blob = text.encode("utf-8")
    return {"طول": len(blob), "sha256": hashlib.sha256(blob).hexdigest(),
            "أسطر": len(text.splitlines()), "كلمات": len(text.split())}


def measure(path=None):
    got = extract(path)
    matn, hawashi = got["متن"], got["حواشٍ"]
    review = tables_review(got["جداول"])
    return {
        "الشخصية_ج٣": {
            "الأداة": {"اسم": TOOL_NAME, "إصدار": TOOL_VERSION},
            "الحاوية": {"اسم": CONTAINER, "معرِّف": CONTAINER_ID,
                        "طول": CONTAINER_BYTES, "sha256": CONTAINER_SHA256,
                        "كائن_git": CONTAINER_BLOB,
                        "شواهدُ_الطبعة": edition_marks(matn)},
            "المتن": deposit_seal(matn),
            "الحواشي": deposit_seal(hawashi),
            "المقصيُّ_معدودًا": got["دفتر"],
            "تخالفُ_NFC": got["تخالفُ_NFC"],
            "الجداولُ_المقصاة": got["جداول"],
            "مراجعةٌ_للمالك": {"جداولُ_تحمل_متنًا": len(review),
                               "بيانُها": review},
            "ترويساتٌ_وتذييلات": got["ترويساتٌ_وتذييلات"],
        }
    }


# ــ ④ المصادمة: الوديعةُ المودَعةُ ⟷ ما يُنتجه المُستخرِج الآن — فارقٌ صفرٌ أو صريخ ــ
def collide(path=None):
    got = extract(path)
    problems = []
    for name, text, dep, sha, size in (
            ("المتن", got["متن"], MATN, MATN_SHA256, MATN_BYTES),
            ("الحواشي", got["حواشٍ"], HAWASHI, HAWASHI_SHA256, HAWASHI_BYTES)):
        fresh = text.encode("utf-8")
        seal = hashlib.sha256(fresh).hexdigest()
        if len(fresh) != size or seal != sha:
            problems.append(f"تيارُ {name}: المُستخرِجُ يعطي {len(fresh)} بايتًا "
                            f"ببصمة {seal} — والمُعلَنُ {size} و{sha}")
            continue
        try:
            on_disk = open(os.path.join(ROOT, dep), "rb").read()
        except OSError as exc:
            problems.append(f"وديعةُ {name} «{dep}» غائبةٌ عن الشجرة: {exc}")
            continue
        if on_disk != fresh:
            problems.append(f"وديعةُ {name} «{dep}» خالفت ما يُنتجه المُستخرِج — "
                            f"{len(on_disk)} بايتًا ببصمة "
                            f"{hashlib.sha256(on_disk).hexdigest()}")
    return problems


def emit(path=None):
    """كتابةُ الوديعتين — بيد المالك وحدَه (SHAKHSIYYA_EMIT_OWNER=1)."""
    if os.environ.get("SHAKHSIYYA_EMIT_OWNER") != "1":
        raise ExtractError(E_USAGE, "الكتابةُ بيد المالك: SHAKHSIYYA_EMIT_OWNER=1")
    got = extract(path)
    for dep, text in ((MATN, got["متن"]), (HAWASHI, got["حواشٍ"])):
        with open(os.path.join(ROOT, dep), "wb") as fh:
            fh.write(text.encode("utf-8"))
        print(f"كُتبت «{dep}»")


def report(doc):
    b = doc["الشخصية_ج٣"]
    print(f"— الشخصية الإسلامية ج٣ · {TOOL_NAME} v{TOOL_VERSION} —")
    print(f"  الحاوية: {b['الحاوية']['طول']:,} بايتًا · "
          f"{b['الحاوية']['sha256'][:8]}… ({b['الحاوية']['معرِّف']})")
    for key in ("المتن", "الحواشي"):
        s = b[key]
        print(f"  {key}: {s['طول']:,} بايتًا · {s['أسطر']:,} سطرًا · "
              f"{s['كلمات']:,} كلمةً · {s['sha256'][:8]}…")
    led = b["المقصيُّ_معدودًا"]
    print("  المقصيُّ معدودًا: " + " · ".join(
        f"{k}={v:,}" for k, v in led.items() if isinstance(v, int)))
    print(f"  رموزُ الخطوط بخطِّها: " + " · ".join(
        f"{k}={v}" for k, v in sorted(led.get("رموزٌ_بخطِّها", {}).items())))
    print(f"  مراجعةٌ للمالك — جداولُ تحمل متنًا: "
          f"{b['مراجعةٌ_للمالك']['جداولُ_تحمل_متنًا']}")
    print("  شواهدُ الطبعة: " + " · ".join(
        f"«{k}»={v}" for k, v in b["الحاوية"]["شواهدُ_الطبعة"].items()))


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--json", metavar="ملفّ", help="كتابةُ الأعداد JSON")
    ap.add_argument("--check", action="store_true", help="مصادمةُ الوديعتين")
    ap.add_argument("--emit", action="store_true", help="كتابةُ الوديعتين (المالك)")
    args = ap.parse_args(argv)
    try:
        if args.emit:
            emit()
            return 0
        if args.check:
            problems = collide()
            for p in problems:
                print(f"::error::{p}")
            if problems:
                return E_DEPOSIT
            print("وديعتا الشخصية ج٣ مُعادتا الاستخراج بفارق صفر ✓")
            return 0
        doc = measure()
        report(doc)
        if args.json:
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False, indent=1, sort_keys=True)
                fh.write("\n")
        return 0
    except ExtractError as exc:
        print(f"::error::{exc.message}")
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
