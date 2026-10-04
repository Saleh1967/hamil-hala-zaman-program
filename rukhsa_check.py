#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مُصادِمُ سطرِ الترخيص — الرخصةُ دعوًى، والدعوى تُصادَم ببايتات الشجرة.

**لِمَ مُصادِمٌ أصلًا؟** لأنّ ملفَّ `LICENSE` يقول «هذا المستودعُ تحت كذا»، وهذه
جملةٌ تَصْدُق يومَ تُكتَب وتَكْذِب في اليوم الذي تدخل فيه الشجرةَ بايتاتٌ ليست
للمشروع. فإن لم يكن للرخصة مُصادِمٌ صارت كأيِّ رقمٍ بلا مولِّدٍ في هذا المستودع:
صادقةً في ظاهرها، كاذبةً في مقدارها، ولا حارسَ يُسقِطها
(`CONTRIBUTING.md` §١ و§٤).

فهذا المُصادِمُ لا يُفتي في حقوقٍ ولا يَمنح إذنًا؛ يقيس خمسَ خاناتٍ من بايتات
الشجرة ويصادمها بما في `RUKHSA.md`:

  ① ملفّاتُ الشجرة          — `git ls-files` معدودةً
  ② حاوياتٌ مستثناة         — كلُّ `.docx` في الشجرة
  ③ مشمولٌ بالرخصة          — ① ناقصَ ②، مقيسًا لا مطروحًا بالنظر
  ④ حاوياتٌ موصولةٌ بالبيان  — المستثنى الذي له ختمٌ في `sources_manifest.tsv`
  ⑤ بايتاتُ مصادرَ في الشجرة — مسارٌ تحت `corpora/sources/` أو `corpora/inbox/`

وأخطرُ الخانات ⑤: صفرُها هو الذي يجعل الاكتفاءَ ببصمةِ المصدر موقفًا مقيسًا لا
دعوى. فإن صارت غيرَ صفرٍ فقد أُعيد نشرُ بايتاتِ مصدرٍ، ويسقط الباب.

وجدولُ الحاويات يُصادَم بثلاثة أوجه لا بالعدِّ وحدَه: الطولُ وsha256 يُقاسان من
البايتات، والمعرِّفُ يُصادَم بالبيان — فحاويةٌ تدخل الشجرةَ بلا سطرٍ في الجدول،
أو تُبدَّل بايتاتُها، أو ينفصل ختمُها عن البيان: كلُّها تُسقِط الباب.

الاستعمال:
    python rukhsa_check.py            # تقريرٌ معدود
    python rukhsa_check.py --check    # مصادمةُ RUKHSA.md ببايتات الشجرة
    python rukhsa_check.py --write    # كتابةُ الخانات المقيسة في RUKHSA.md
    python rukhsa_check.py --falsify  # محاولاتُ تكذيبِ الحرّاس

المخارج: 0 موافقٌ · 1 حارسٌ صرخ · 2 سوءُ استعمال.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(ROOT, "RUKHSA.md")
MANIFEST = os.path.join(ROOT, "sources_manifest.tsv")

E_OK, E_SCREAM, E_USAGE = 0, 1, 2

# المسارات التي لا تدخل الشجرةَ بالبناء (.gitignore) — وحضورُ واحدٍ منها إعادةُ نشر.
SOURCE_DIRS = ("corpora/sources/", "corpora/inbox/")
CONTAINER_EXT = ".docx"


class Scream(Exception):
    """صريخُ حارسٍ — نصُّه هو حكمُه."""


# ═══ ① القياس من البايتات ═══════════════════════════════════════════════════
def tracked():
    """ملفّاتُ الشجرة كما يعدّها git — لا مشطٌ لنظام الملفّات يلتقط غيرَ المودَع."""
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return [p for p in out.decode("utf-8").split("\0") if p]


def measure_container(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        raw = fh.read()
    return len(raw), hashlib.sha256(raw).hexdigest()


def manifest_seals():
    """خريطةُ sha256 ⟶ المعرِّف من البيان: الحقلُ الأوّل والثامن لكلِّ سطرٍ مختوم."""
    seals = {}
    with open(MANIFEST, encoding="utf-8") as fh:
        for line in fh:
            if line.lstrip().startswith("#") or not line.strip():
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) >= 9 and f[8].strip() == "مختوم":
                seals[f[7].strip()] = f[0].strip()
    return seals


def census(files=None):
    """الخاناتُ الخمسُ والجدول — مقيسةً كلُّها، ولا خانةَ تُكتَب بالنظر."""
    files = tracked() if files is None else files
    containers = sorted(f for f in files if f.lower().endswith(CONTAINER_EXT))
    seals = manifest_seals()

    rows, linked = [], 0
    for path in containers:
        length, sha = measure_container(path)
        ident = seals.get(sha, "—")
        linked += ident != "—"
        rows.append({"ملف": path, "طول": length, "sha256": sha, "المعرِّف": ident})

    republished = sorted(f for f in files if f.startswith(SOURCE_DIRS))
    return {
        "خانات": {
            "ملفّاتُ الشجرة": len(files),
            "حاوياتٌ مستثناة": len(containers),
            "مشمولٌ بالرخصة": len(files) - len(containers),
            "حاوياتٌ موصولةٌ بالبيان": linked,
            "بايتاتُ مصادرَ في الشجرة": len(republished),
        },
        "جدول": rows,
        "مُعادُ_النشر": republished,
    }


# ═══ ② الحرّاس ══════════════════════════════════════════════════════════════
CELL = re.compile(r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<value>\d+)\s*\|", re.M)
ROW = re.compile(r"^\|\s*`(?P<file>[^`]+)`\s*\|\s*(?P<len>[\d,]+)\s*\|\s*"
                 r"`(?P<sha>[0-9a-f]{64})`\s*\|\s*`(?P<id>[^`]+)`\s*\|", re.M)


def doc_cells(text):
    return {m.group("name"): int(m.group("value")) for m in CELL.finditer(text)}


def doc_rows(text):
    return [{"ملف": m.group("file"), "طول": int(m.group("len").replace(",", "")),
             "sha256": m.group("sha"), "المعرِّف": m.group("id")}
            for m in ROW.finditer(text)]


def guards(text, got):
    """خمسُ خاناتٍ وجدولٌ — أوّلُ صريخٍ يقطع، ويعيد سطرَ البيان عند السلامة."""
    cells = doc_cells(text)
    for name, value in got["خانات"].items():
        if name not in cells:
            raise Scream(f"خانةُ «{name}» غائبةٌ عن سطر الترخيص — لا تُطوى")
        if cells[name] != value:
            raise Scream(f"خانةُ «{name}»: الوثيقةُ {cells[name]} والمقيسُ {value}")

    # ⑤ أخطرُها: بايتاتُ مصدرٍ في الشجرة إعادةُ نشرٍ لا يرخّصها المشروع.
    if got["خانات"]["بايتاتُ مصادرَ في الشجرة"]:
        raise Scream("بايتاتُ مصادرَ دخلت الشجرة: "
                     f"{got['مُعادُ_النشر']} — لا يُرخَّص ما لا يُملَك")

    rows, want = doc_rows(text), got["جدول"]
    if len(rows) != len(want):
        raise Scream(f"جدولُ الحاويات {len(rows)} صفًّا والمقيسُ {len(want)}")
    for a, b in zip(rows, want):
        if a != b:
            raise Scream(f"صفُّ الحاوية خالف بايتاتِه: {a} ⟷ {b}")

    # وكلُّ حاويةٍ موصولةٌ بالبيان: الاستثناءُ المنفصلُ عن ختمٍ دعوى بلا سند.
    if got["خانات"]["حاوياتٌ موصولةٌ بالبيان"] != got["خانات"]["حاوياتٌ مستثناة"]:
        orphan = [r["ملف"] for r in want if r["المعرِّف"] == "—"]
        raise Scream(f"حاويةٌ مستثناةٌ بلا ختمٍ في البيان: {orphan}")

    c = got["خانات"]
    return (f"سطرُ الترخيص: {c['ملفّاتُ الشجرة']} ملفًّا · "
            f"{c['مشمولٌ بالرخصة']} مشمولًا · {c['حاوياتٌ مستثناة']} حاويةً "
            f"مستثناةً موصولةً بالبيان · صفرُ بايتاتِ مصدرٍ مُعادةِ النشر ✓")


# ═══ ③ محاولاتُ التكذيب ═════════════════════════════════════════════════════
def _bad_cell(text, got):
    n = got["خانات"]["ملفّاتُ الشجرة"]
    return text.replace(f"| ملفّاتُ الشجرة | {n} |",
                        f"| ملفّاتُ الشجرة | {n + 1} |"), got


def _dropped_row(text, got):
    row = got["جدول"][0]
    return re.sub(rf"^\|\s*`{re.escape(row['ملف'])}`.*\n", "", text, count=1,
                  flags=re.M), got


def _twisted_sha(text, got):
    sha = got["جدول"][0]["sha256"]
    return text.replace(sha, "0" * 64), got


def _republished(text, got):
    import copy
    broken = copy.deepcopy(got)
    broken["مُعادُ_النشر"] = ["corpora/sources/ghost.txt"]
    broken["خانات"]["بايتاتُ مصادرَ في الشجرة"] = 1
    # تُوافَق الوثيقةُ على الكذبة عمدًا، ليُبتلى حارسُ ⑤ نفسُه لا حارسُ الخانات.
    return rewrite(text, broken), broken


def _unlinked(text, got):
    import copy
    broken = copy.deepcopy(got)
    broken["جدول"][0]["المعرِّف"] = "—"
    broken["خانات"]["حاوياتٌ موصولةٌ بالبيان"] -= 1
    # تُوافَق الوثيقةُ أيضًا، ليُبتلى حارسُ الوصل لا حارسُ الخانات ولا حارسُ الصفّ.
    return rewrite(text, broken), broken


TRIALS = (
    ("خانةٌ خالفت المقيس", _bad_cell, "والمقيسُ"),
    ("حاويةٌ سقطت من الجدول", _dropped_row, "جدولُ الحاويات"),
    ("بصمةٌ حُرِّفت", _twisted_sha, "خالف بايتاتِه"),
    ("بايتاتُ مصدرٍ في الشجرة", _republished, "لا يُرخَّص ما لا يُملَك"),
    ("حاويةٌ انفصلت عن البيان", _unlinked, "بلا ختمٍ في البيان"),
)


def falsify(text, got):
    passed = []
    for name, break_it, needle in TRIALS:
        broken_text, broken_got = break_it(text, got)
        try:
            guards(broken_text, broken_got)
        except Scream as exc:
            if needle not in str(exc):
                raise AssertionError(
                    f"المحاولة «{name}» رُدَّت بصريخٍ آخر: {exc}") from None
            passed.append(name)
        else:
            raise AssertionError(f"المحاولة «{name}» لم تُردّ — الحارسُ أعمى")
    return passed


# ═══ ④ الكتابة ══════════════════════════════════════════════════════════════
def rewrite(text, got):
    """الخاناتُ والجدولُ يُكتبان من القياس — فلا رقمَ في RUKHSA.md بيدٍ."""
    for name, value in got["خانات"].items():
        text = re.sub(rf"^\|\s*{re.escape(name)}\s*\|\s*\d+\s*\|",
                      f"| {name} | {value} |", text, flags=re.M)
    table = "\n".join(
        f"| `{r['ملف']}` | {r['طول']:,} | `{r['sha256']}` | `{r['المعرِّف']}` |"
        for r in got["جدول"])
    return re.sub(r"(?m)^\|\s*`[^`]+\.docx`.*(?:\n\|\s*`[^`]+\.docx`.*)*",
                  lambda _: table, text, count=1)


def main(argv=None):
    ap = argparse.ArgumentParser(description="مُصادِمُ سطرِ الترخيص")
    ap.add_argument("--check", action="store_true", help="مصادمةُ RUKHSA.md")
    ap.add_argument("--write", action="store_true", help="كتابةُ الخانات المقيسة")
    ap.add_argument("--falsify", action="store_true", help="محاولاتُ التكذيب")
    args = ap.parse_args(argv)

    got = census()
    with open(DOC, encoding="utf-8") as fh:
        text = fh.read()

    if args.write:
        fresh = rewrite(text, got)
        if fresh != text:
            with open(DOC, "w", encoding="utf-8") as fh:
                fh.write(fresh)
            print("سطرُ الترخيص كُتب من القياس ✓")
        else:
            print("سطرُ الترخيص موافقٌ قياسَه — لا تبديل ✓")
        text = fresh

    if not (args.check or args.write or args.falsify):
        for name, value in got["خانات"].items():
            print(f"  {name} = {value}")
        for row in got["جدول"]:
            print(f"  {row['ملف']} · {row['طول']:,} · {row['المعرِّف']}")
        return E_OK

    try:
        print(guards(text, got))
    except Scream as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return E_SCREAM

    if args.falsify:
        passed = falsify(text, got)
        print(f"محاولاتُ التكذيب: {len(passed)} رُدَّت كلُّها ✓")
    return E_OK


if __name__ == "__main__":
    sys.exit(main())
