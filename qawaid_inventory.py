#!/usr/bin/env python3
"""جردٌ آليٌّ مغلقٌ لقواعد «أبحاث اللغة» في المتن المختوم."""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter

import shakhsiyya_extract as SX

ROOT = os.path.dirname(os.path.abspath(__file__))
MATN = os.path.join(ROOT, SX.MATN)
START_HEADING = "أبحـاث اللغة"
END_HEADING = "أقسـام الكتـاب والسُّـنّة"
STATUSES = ("مبرهَنة", "مردودة", "معلّقة", "غير قابلة للقياس بالمقام الحالي")

CHAPTERS = (
    "أبحـاث اللغة", "طـريق معـرفة اللغة العـربية", "ألفاظ اللغة وأقسامها",
    "تقسـيم اللفظ باعتبار الدال وحده", "المفـرد", "الاسـم",
    "تقسيم اللفظ باعتبار المدلول وحده", "المـرَكَّب",
    "تقسيم اللفظ باعتبار الدال والمدلول", "الترادف", "الاشـتراك",
    "الحقيقة والمجاز", "الحقيقة الشـرعية", "وجـود الحقائق الشـرعية",
    "القرآن كلُّه عربي\nوليس فيه ولا كلمة واحدة غير عربية",
    "الحقيقة العـرفية", "الألفاظ المنقولة", "تعـارض ما يخل بالفهم",
    "الفعـل", "الحـرف", "المنطـوق والمفهـوم", "المنطـوق", "المفهـوم",
    "دلالة الاقتضاء", "دلالة التنبيه والإيماء", "دلالة الإشـارة",
    "مفهـوم الموافقة", "مفهـوم المخالفة", "مفهـوم الصفة",
    "مفهـوم الشـرط", "مفهـوم الغاية", "مفهـوم العدد",
    "ما لم يعمل به من مفهـوم المخالفة",
)

TYPE_PATTERNS = (
    ("تعريف", re.compile(
        r"(?:^|\s)(?:هو|هي|وهو|وهي)\s|عبارة عن|تعريف|عُرّف|عرفوه|"
        r"يسمى|تسمى|المراد ب|معنى [^؛.!؟:]{0,50} هو"
    )),
    ("قسمة", re.compile(
        r"ينقسم|تنقسم|أقسام|أنواع|أحدها|والثاني|والثالث|والرابع|"
        r"والخامس|والسادس|والسابع|(?:إما|إمّا) [^؛.!؟:]{0,160} أو"
    )),
    ("شرط", re.compile(
        r"يشترط|اشترط|شرط|لا بد|بشرط|لا يجوز|يجوز|يمتنع|"
        r"لا يصح|لا يكون|لا تكون"
    )),
    ("مثال", re.compile(
        r"مثال|مثله|مثل |كقول|كقوله|(?:^|\s)وقوله|قال تعالى|"
        r"كدلالة|نحو|وذلك ك|وذلك مثل|فمثاله"
    )),
)

REPOSITORIES = (
    dict(معرّف="المشروع",
         رابط="https://github.com/Saleh1967/hamil-hala-zaman-program",
         مرجع="الفرع الذي ولّد الوديعة"),
    dict(معرّف="shakhsiyya_j3", رابط="repo=self",
         مرجع="sources_manifest.tsv:67 @ b7abcad328db8a69349e02ef3e4ad4076b1a7486"),
    dict(معرّف="شهود_OpenITI", رابط="https://github.com/OpenITI",
         مرجع="sources_manifest.tsv"),
    dict(معرّف="مقاييس_الجذور", رابط="https://github.com/Saleh1967/Alghanem",
         مرجع="maqayis_layer.SOURCE"),
)


class InventoryError(Exception):
    pass


def byte_offset(text, char_offset):
    return len(text[:char_offset].encode("utf-8"))


def chapter_spans(section, section_start):
    spans = []
    cursor = 0
    for heading in CHAPTERS:
        pattern = re.compile(r"(?m)^" + re.escape(heading) + r"$")
        matches = list(pattern.finditer(section))
        matches = [match for match in matches if match.start() >= cursor]
        if not matches:
            raise InventoryError(f"غاب عنوانُ بابٍ: {heading!r}")
        if len(matches) != 1:
            raise InventoryError(f"عنوانُ بابٍ غيرُ فريد: {heading!r}")
        at = matches[0].start()
        spans.append((heading.replace("\n", " "), section_start + at))
        cursor = at + len(heading)
    return [(name, start, spans[i + 1][1] if i + 1 < len(spans)
             else section_start + len(section))
            for i, (name, start) in enumerate(spans)]


def sentence_spans(text, start, end):
    for line in re.finditer(r"[^\n]+", text[start:end]):
        line_start = start + line.start()
        for piece in re.finditer(r".+?(?:(?<=[؛.!؟])(?=\s)|$)", line.group()):
            raw = piece.group()
            left = len(raw) - len(raw.lstrip())
            value = raw.strip()
            if value:
                yield line_start + piece.start() + left, value


def unique_anchor(raw, text, char_at, sentence):
    start = char_at
    end = char_at + len(sentence)
    while True:
        excerpt = text[start:end].encode("utf-8")
        if raw.count(excerpt) == 1:
            return start, excerpt
        if start == 0 and end == len(text):
            raise InventoryError(f"تعذّر إفراد المرساة: {sentence[:80]!r}")
        start = max(0, start - 16)
        end = min(len(text), end + 16)


def fold(text):
    plain = "".join(
        char for char in unicodedata.normalize("NFD", text)
        if not unicodedata.combining(char)
    ).replace("ـ", "")
    return plain.translate(str.maketrans("أإآىةؤئ", "ااايهوي"))


def classify_status(kind, chapter, text):
    if kind == "قسمة" and chapter in {
        "تقسـيم اللفظ باعتبار الدال وحده",
        "تقسيم اللفظ باعتبار المدلول وحده",
        "تقسيم اللفظ باعتبار الدال والمدلول",
    }:
        return ("مبرهَنة", "aqsam_v0.json",
                "بناءُ العدد والشجرة مصادَمٌ ببايتات المتن؛ لا يعني ذلك صدقَ كل فرع")
    if chapter == "تقسيم اللفظ باعتبار المدلول وحده" and kind != "مثال":
        return ("مردودة", "sidq_v0.json",
                "صدقُ قسمة المدلول لم يقم بمكيال الوضع المتاح")
    plain = fold(text)
    if kind == "مثال" and any(w in plain for w in (
        "ليس من البر الصيام في السفر",
        "من اقتطع شبرا من الارض",
        "لا صلاه الا بفاتحه الكتاب",
        "لا يقضي القاضي بين اثنين وهو غضبان",
    )):
        return ("معلّقة", "dalalat_v0.json",
                "الشاهد لم يتحقق بحرفه في نسختين مختومتين")
    return ("غير قابلة للقياس بالمقام الحالي", None,
            "نقلٌ مسجّل بمرساته؛ لا حكمَ عدديًّا حيًّا يطابق هذا البند بعينه")


def build():
    raw = open(MATN, "rb").read()
    if len(raw) != SX.MATN_BYTES or hashlib.sha256(raw).hexdigest() != SX.MATN_SHA256:
        raise InventoryError("المتن غاب أو خالف ختم shakhsiyya_extract.FROZEN")
    text = raw.decode("utf-8")
    start = text.index(START_HEADING, 10_000)
    end = text.index(END_HEADING, start)
    chapters = chapter_spans(text[start:end], start)
    rows = []
    type_counts = Counter()
    status_counts = Counter()
    for chapter_index, (chapter, chapter_start, chapter_end) in enumerate(chapters, 1):
        chapter_rows = 0
        for char_at, sentence in sentence_spans(text, chapter_start, chapter_end):
            if sentence in {heading for raw_heading in CHAPTERS
                            for heading in (raw_heading, *raw_heading.splitlines())}:
                continue
            kinds = [name for name, pattern in TYPE_PATTERNS if pattern.search(sentence)]
            for kind in kinds:
                anchor_at, excerpt = unique_anchor(raw, text, char_at, sentence)
                status, evidence, reason = classify_status(kind, chapter, sentence)
                type_counts[kind] += 1
                status_counts[status] += 1
                chapter_rows += 1
                rows.append({
                    "مرساة": f"ل-{chapter_index:02d}-{chapter_rows:03d}-{kind}",
                    "باب": chapter,
                    "نوع": kind,
                    "نص": sentence,
                    "موضع": {
                        "إزاحة": byte_offset(text, anchor_at),
                        "طول": len(excerpt),
                        "sha256": hashlib.sha256(excerpt).hexdigest(),
                        "فريدٌ_في_المتن": True,
                    },
                    "حكم": status,
                    "دليل": evidence,
                    "علّة": reason,
                })
    if set(status_counts) - set(STATUSES):
        raise InventoryError("ظهر حكمٌ خارج الأصناف الأربعة")
    chapter_rows = []
    for i, (name, chapter_start, chapter_end) in enumerate(chapters, 1):
        body = text[chapter_start:chapter_end].encode("utf-8")
        chapter_rows.append({
            "مرساة": f"باب-{i:02d}", "اسم": name,
            "إزاحة": byte_offset(text, chapter_start), "طول": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "بنود": sum(row["باب"] == name for row in rows),
        })
    payload = {
        "المصدر": {
            "ملف": SX.MATN, "طول": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "بدايةُ_أبحاث_اللغة": byte_offset(text, start),
            "نهايةُ_أبحاث_اللغة": byte_offset(text, end),
        },
        "المستودعات": list(REPOSITORIES),
        "الأبواب": chapter_rows,
        "البنود": rows,
    }
    digest = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {"جردُ_القواعد_v0": {
        **payload,
        "المقيس": {
            "أبواب": len(chapter_rows), "بنود": len(rows),
            "الأنواع": dict(sorted(type_counts.items())),
            "الأحكام": {status: status_counts[status] for status in STATUSES},
        },
        "اعتمادُ_المالك": {
            "المالكُ_المطلوب": "@Saleh1967",
            "حالة": "بانتظار توقيع المالك",
            "بصمةُ_المحمول": digest,
            "بيان": "لا ينتحل المولّد توقيع المالك؛ يعتمد المالك هذه البصمة من حسابه.",
        },
    }}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", metavar="PATH")
    args = parser.parse_args(argv)
    try:
        result = build()
    except (InventoryError, OSError, UnicodeError, ValueError) as exc:
        print(f"qawaid_inventory: {exc}", file=sys.stderr)
        return 4
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        with open(args.json, "w", encoding="utf-8") as stream:
            stream.write(rendered)
    print(json.dumps(result["جردُ_القواعد_v0"]["المقيس"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
