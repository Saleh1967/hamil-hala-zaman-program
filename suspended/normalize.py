# normalize.py — الطبقةُ التالية بعد البايتات المختومة: من بايتٍ إلى نصٍّ معدود.
#
# fetch_source.sh يُسلِّم البايتاتِ مختومةً (التحقُّقُ الثلاثيُّ ومخارجُه الخمسة).
# وهذا الملفُّ يأخذها فيفُكُّ ترميزَها ويقشّر ترويسةَ mARkdown ويصنّف سطورَ المتن
# ويعدّها. **ولا يطبّع حرفًا واحدًا**: لا همزةَ تُطوى ولا ألفٌ تُوحَّد ولا تشكيلٌ
# يُجرَّد. الطيُّ إيداعٌ ثانٍ مستقلٌّ، وكلُّ قاعدةٍ فيه تُعرَض على حَكَم الفاتورة
# في induction/deposit_law.py كما عُرض طيُّ الألف في hiyad.py — فلا يدخل المستودعَ
# طيٌّ «معقولٌ» بلا فاتورةٍ تقبله أو ترفضه.
#
# — أربعةُ حرّاسٍ لا يُطوى واحدٌ منها في الصمت —
#   ① الترميز: utf-8-sig دائمًا (فـBOM حاضرٌ في شاهدين من الأربعةَ عشرَ)، وأيُّ
#      بايتةٍ لا تُفَكّ تُسقِط الملفَّ بموضعها. ولا errors='replace' البتّةَ: محرفُ
#      البدل � يدخل صامتًا فيصير تالفًا يُعَدُّ نصًّا.
#   ② NFC: الملفُّ غيرُ المطبَّع يُعلَن ويسقط، فلا يُطبَّع في الظلام ولا يُقاس عليه.
#   ③ الفاصل: #META#Header#End# مرّةً واحدةً بالضبط — غيابُه يعني ملفًّا ليس على
#      هيئة OpenITI، وتكرارُه يعني متنًا ملصوقًا؛ وكلاهما صريخٌ لا حزرٌ بأوّلِ فاصل.
#   ④ الترقيم: PageVxxPyy يُنتزَع حقلًا مستقلًّا ولا يُحذَف — وغيابُه يُعلَن «بلا
#      ترقيم» حالًا. (tabari_jamic_tafsir01 بلا ترقيمٍ أصلًا، وهو شاهدٌ من أربعةَ
#      عشرَ — فمن بنى إحالةً على الترقيم فقدَه صامتًا لولا هذا الإعلان.)
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 5 بايتةٌ لا تُفَكّ · 6 غيرُ مطبَّعٍ NFC
#          · 7 فاصلُ الترويسة مخالف.
# (وهي غيرُ مخارج fetch_source.sh عمدًا: طبقتان مختلفتان لا يُخلَط عقداهما.)
#
# التشغيل:
#   python normalize.py <ملفّ…>            تقريرٌ معدودٌ لكلِّ ملفّ
#   python normalize.py --json <ملفّ…>     الأعدادُ نفسُها JSON
#   python normalize.py --lines <ملفّ…>    سطرٌ سطرٌ: رقمُه · صنفُه · درجتُه · ترقيمُه
import argparse
import json
import os
import re
import sys
import unicodedata

E_USAGE = 2
E_DECODE = 5
E_NFC = 6
E_HEADER = 7

SEP = "#META#Header#End#"
META = "#META#"
PAGE = re.compile(r"PageV\d+P\d+")

# أصنافُ السطر خمسةٌ معلَنةٌ لا سادسَ لها؛ والعنوانُ يحمل درجةً معه.
WASL = "وصل"        # ~~ وصلُ فقرةٍ سابقة
HEAD = "عنوان"      # ‎# |‎ أو ‎### |‎ أو ‎### ||‎ — والدرجةُ عددُ العصيّ
PARA = "فقرة"       # ‎#‎ بدءُ فقرة
BLANK = "فراغ"
BARE = "عارٍ"        # نصٌّ بلا وسمٍ أصلًا — حاضرٌ في ثلاثةٍ من الأربعةَ عشرَ
KINDS = (WASL, HEAD, PARA, BLANK, BARE)

# العنوانُ وسمُه ‎#‎ متبوعًا بعصًا واحدةٍ فأكثر؛ ويُفحَص قبلَ الفقرة وإلّا ابتلعته.
RE_HEAD = re.compile(r"^(#+)\s*(\|+)")
RE_PARA = re.compile(r"^#")


class NormalizeError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ــ ① القراءة ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def read_text(path):
    """بايتاتٌ ← نصّ. utf-8-sig دائمًا، والمخالفُ يسقط بموضعه لا يُرقَّع."""
    try:
        raw = open(path, "rb").read()
    except OSError as exc:
        raise NormalizeError(E_USAGE, f"تعذّرت قراءةُ «{path}»: {exc}")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise NormalizeError(
            E_DECODE,
            f"«{path}»: بايتةٌ لا تُفَكّ عند {exc.start} ({exc.reason}) — "
            "ولا يُرقَّع بمحرف بدل",
        )
    return text


def has_bom(path):
    """البومُ يُعلَن ولا يُسكَت عنه: حاضرٌ في شاهدين من الأربعةَ عشرَ."""
    with open(path, "rb") as fh:
        return fh.read(3) == b"\xef\xbb\xbf"


# ــ ② حارس NFC ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def guard_nfc(text, path):
    """التطبيعُ يُفحَص ولا يُفرَض: من خالف NFC أُعلن وسقط."""
    if not unicodedata.is_normalized("NFC", text):
        nfc = unicodedata.normalize("NFC", text)
        n = sum(1 for a, b in zip(text, nfc) if a != b)
        raise NormalizeError(
            E_NFC,
            f"«{path}»: ليس مطبَّعًا NFC ({len(text)} ← {len(nfc)} محرفًا، "
            f"وأوّلُ خلافٍ بعد {n} موضعًا) — لا يُطبَّع في الظلام",
        )


# ــ ③ التقشير ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def split_header(text, path):
    """ترويسةٌ ومتنٌ على فاصلٍ واحدٍ بالضبط؛ والعدُّ يُصرَخ به إن خالف."""
    n = text.count(SEP)
    if n != 1:
        raise NormalizeError(
            E_HEADER,
            f"«{path}»: فاصلُ الترويسة {SEP} ورد {n} مرّةً لا مرّةً واحدة — "
            "لا يُحزَر بأوّلِ فاصل",
        )
    head, body = text.split(SEP, 1)
    # سطرُ الفاصل ينتهي بسطرٍ جديدٍ هو من الفاصل لا من المتن، فيُطرَح وحدَه.
    if body.startswith("\n"):
        body = body[1:]
    return head, body


def parse_meta(head):
    """#META# key :: value  ·  #META# key: value — والمجهولُ يُحفَظ خامًا لا يُطرَح."""
    meta, loose = {}, []
    for line in head.split("\n"):
        if not line.startswith(META):
            if line.strip():
                loose.append(line)
            continue
        rest = line[len(META):].strip()
        if "::" in rest:
            key, _, value = rest.partition("::")
        elif ":" in rest:
            key, _, value = rest.partition(":")
        else:
            loose.append(line)
            continue
        key = key.strip()
        if key:
            meta[key] = value.strip()
    return meta, loose


# ــ ④ التصنيف والترقيم ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def classify(line):
    """سطرٌ ← (صنفٌ، درجةٌ). الدرجةُ عددُ العصيِّ في العنوان، و0 فيما سواه."""
    if not line.strip():
        return BLANK, 0
    if line.startswith("~~"):
        return WASL, 0
    m = RE_HEAD.match(line)
    if m:
        return HEAD, len(m.group(2))
    if RE_PARA.match(line):
        return PARA, 0
    return BARE, 0


def read_lines(body):
    """سطورُ المتن سجلّاتٍ: الخامُ محفوظٌ، والترقيمُ منتزَعٌ حقلًا لا محذوفًا."""
    lines = body.split("\n")
    # سطرٌ جديدٌ في آخر الملفِّ ينهي السطرَ الأخير ولا يفتح سادسًا فارغًا.
    if lines and lines[-1] == "":
        lines.pop()
    out = []
    for i, raw in enumerate(lines, 1):
        kind, degree = classify(raw)
        pages = PAGE.findall(raw)
        out.append(
            {
                "رقم": i,
                "صنف": kind,
                "درجة": degree,
                "ترقيم": pages,
                "خام": raw,
                "نصّ": PAGE.sub("", raw).strip(),
            }
        )
    return out


def measure(path):
    """القياسُ كلُّه في دالّةٍ واحدة: ما لم يُعَدّ هنا لا يُدَّعى في تقرير."""
    text = read_text(path)
    guard_nfc(text, path)
    head, body = split_header(text, path)
    meta, loose = parse_meta(head)
    lines = read_lines(body)

    kinds = {k: 0 for k in KINDS}
    degrees, pages = {}, []
    for rec in lines:
        kinds[rec["صنف"]] += 1
        if rec["صنف"] == HEAD:
            degrees[rec["درجة"]] = degrees.get(rec["درجة"], 0) + 1
        pages.extend(rec["ترقيم"])

    return {
        "ملفّ": os.path.basename(path),
        "بايتات": os.path.getsize(path),
        "محارف": len(text),
        "بوم": has_bom(path),
        "ترويسة": meta,
        "ترويسةٌ خام": loose,
        "أسطر": len(lines),
        "أصناف": kinds,
        "درجاتُ العناوين": dict(sorted(degrees.items())),
        "ترقيم": len(pages),
        "أوّلُ ترقيم": pages[0] if pages else None,
        "آخرُ ترقيم": pages[-1] if pages else None,
        "بلا ترقيم": not pages,
    }


# ــ التقرير ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def first_of(meta, *keys):
    """أوّلُ حقلٍ حاضرٍ من أسماءٍ معدودة؛ وNODATA غيابٌ لا قيمة."""
    for k in keys:
        v = meta.get(k)
        if v and v not in ("NODATA", "NOCODE", "NOTGIVEN"):
            return v
    return "—"


def report(m):
    print(f"— {m['ملفّ']}")
    print(f"  بايتات {m['بايتات']:,} · محارف {m['محارف']:,} · "
          f"بوم {'نعم' if m['بوم'] else 'لا'} · أسطرُ متنٍ {m['أسطر']:,}")
    title = first_of(m["ترويسة"], "Title", "020.BookTITLE", "029.BookTITLEalt")
    author = first_of(m["ترويسة"], "Author", "010.AuthorNAME", "010.AuthorAKA")
    print(f"  ترويسةٌ: {len(m['ترويسة'])} حقلًا · العنوان {title} · المؤلِّف {author[:60]}")
    print("  أصناف: " + " · ".join(f"{k} {m['أصناف'][k]:,}" for k in KINDS))
    if m["درجاتُ العناوين"]:
        print("  درجاتُ العناوين: "
              + " · ".join(f"{d} عصًا {n:,}" for d, n in m["درجاتُ العناوين"].items()))
    if m["بلا ترقيم"]:
        print("  الترقيم: **بلا ترقيم** — لا PageVxxPyy في المتن كلِّه")
    else:
        print(f"  الترقيم: {m['ترقيم']:,} موضعًا · "
              f"من {m['أوّلُ ترقيم']} إلى {m['آخرُ ترقيم']}")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="normalize.py",
        description="من البايت المختوم إلى نصٍّ مقروءٍ معدود — بلا تطبيعٍ أصلًا",
    )
    ap.add_argument("paths", nargs="+", metavar="ملفّ")
    ap.add_argument("--json", action="store_true", help="الأعدادُ نفسُها JSON")
    ap.add_argument("--lines", action="store_true", help="سطرًا سطرًا بصنفه")
    args = ap.parse_args(argv)

    rc = 0
    out = []
    for path in args.paths:
        try:
            m = measure(path)
        except NormalizeError as exc:
            print(f"صريخ: {exc.message}", file=sys.stderr)
            rc = max(rc, exc.code)
            continue
        if args.lines:
            for rec in read_lines(split_header(read_text(path), path)[1]):
                print(f"{rec['رقم']}\t{rec['صنف']}\t{rec['درجة']}\t"
                      f"{','.join(rec['ترقيم']) or '-'}\t{rec['نصّ'][:60]}")
        elif args.json:
            out.append(m)
        else:
            report(m)
    if args.json and out:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    sys.exit(main())
