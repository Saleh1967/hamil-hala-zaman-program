#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مولِّدُ «سطر العقد» في `SOURCES.md` — خاناتٌ تُشتقُّ من مواضعها لا تُكتَب بيد.

**لِمَ مولِّدٌ ولم يكفِ الحارس؟** كان سطرُ العقد يُصادَم في
`test_normalize.test_contract_line_is_collided` ولا يُولَّد، فكان كلُّ تبدّلٍ في
موضعٍ يترك على الكاتب أن يُصلح الخانةَ بيده. وبيدٌ تُصلح خانةً هي بيدٌ تستطيع أن
تُبدّلها لتمرير الاختبار — وذلك بعينُه ما يمنعه `CONTRIBUTING.md` §٣. فالخاناتُ
ههنا **تُشتقّ**، والوثيقةُ تُكتَب من الاشتقاق، والحارسُ يستدعي هذا الاشتقاقَ
نفسَه ولا ينسخه (`CONTRIBUTING.md` §٦: الحَكَمُ واحدٌ يُستدعى ولا يُنسَخ).

**وما أثبتَه هذا المولِّدُ عند ولادته**: سطرُ العقد كان يعلن «أختامُ [بوّابة]
المصدَّرة = 580» و«أختامٌ بسندٍ مُعلَن = 580»، ومواضعُهما تعطي 624. والانزياحُ
ليس تقادمًا بطيئًا بل إيداعٌ بعينه: الدمجُ `45f26a2` أخذ جانبَ الفرعِ في
`SOURCES.md` (580) وجانبَ `main` في `induction/seals.json` (609) وجانبًا ثالثًا
في `induction/seals.py` (624) — فافترقت ثلاثتُها في إيداعٍ واحد.

المخارج: 0 موافقٌ · 1 خانةٌ خالفت موضعَها (مع `--check`) · 2 سوءُ استعمال.
"""
from __future__ import annotations

import argparse
import ast
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(ROOT, "SOURCES.md")

E_OK, E_DRIFT, E_USAGE = 0, 1, 2


def manifest_rows(path=None):
    """سطورُ البيان غيرَ المُعلَّقة، كلُّ سطرٍ قائمةَ حقولٍ بالتبويب."""
    path = path or os.path.join(ROOT, "sources_manifest.tsv")
    with open(path, encoding="utf-8") as fh:
        return [ln.rstrip("\n").split("\t") for ln in fh
                if ln.strip() and not ln.startswith("#")]


def peel_collisions(path=None):
    """عدَّةُ مصادمات التقشير — تُعَدُّ بـ`ast` من بايتات `test_normalize.py`.

    ولا تُستورَد الوحدةُ لتُعَدَّ دوالُّها: الاستيرادُ يجعل المولِّدَ تابعًا لحارسِه،
    فيدور كلٌّ منهما على الآخر. والعدُّ من الشجرةِ قراءةٌ لا تشغيل.
    """
    path = path or os.path.join(ROOT, "test_normalize.py")
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    return sum(1 for n in tree.body
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name.startswith("test_"))


def seal_counts():
    """عدَّتا أختام [بوّابة]: المصدَّرةُ، وذاتُ السند المُعلَن — من `SEALS` نفسِها."""
    sys.path.insert(0, os.path.join(ROOT, "induction"))
    import seals as S                                   # noqa: PLC0415 — عند الحاجة
    gates = [s for s in S.SEALS if s["صنف"] == S.GATE]
    return len(gates), sum(1 for s in gates if S.sanad_of(s))


def measure():
    """خاناتُ سطر العقد المشتقّةُ — اسمُ البند ⟶ مقدارُه كنصٍّ كما يُكتَب في الجدول.

    وما ليس ههنا ليس مطويًّا: صفوفُ المخارج ومصادمات الجلب تُصادَم بتشغيل
    طبقتيهما في `test_normalize`، فلا تُشتقُّ قراءةً ولا تُكتَب من ههنا.
    """
    rows = manifest_rows()
    widths = {len(r) for r in rows}
    if len(widths) != 1:
        raise SystemExit("صريخ: سطورُ البيان مختلفةُ عددِ الحقول — لا عرضَ واحدًا يُعلَن")
    states = [r[8] for r in rows]
    gates, with_sanad = seal_counts()
    return {
        "حقولُ البيان": str(len(rows[0])),
        "شهودٌ مختومون": str(states.count("مختوم")),
        "معذورون بالاسم": str(states.count("معذور")),
        "مصادماتُ التقشير": str(peel_collisions()),
        "أختامُ [بوّابة] المصدَّرة": str(gates),
        "أختامٌ بسندٍ مُعلَن": str(with_sanad),
    }


def doc_rows(text):
    """خاناتُ الجدول كما هي في بايتات الوثيقة: اسمُ البند ⟶ مقدارُه."""
    rows = {}
    for line in text.splitlines():
        if line.startswith("| ") and line.count("|") == 5:
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows[cells[0]] = cells[1]
    return rows


def drifts(text=None):
    """الخاناتُ التي خالفت مواضعَها: (البند، المكتوب، المُشتَقّ)."""
    if text is None:
        with open(DOC, encoding="utf-8") as fh:
            text = fh.read()
    rows = doc_rows(text)
    out = []
    for key, value in measure().items():
        if key not in rows:
            out.append((key, "غائبٌ عن الجدول", value))
        elif rows[key] != value:
            out.append((key, rows[key], value))
    return out


def rewrite(text):
    """نصُّ الوثيقةِ وقد كُتبت خاناتُه المشتقّةُ في مواضعها — وما سواها لا يُمَسّ."""
    derived = measure()
    out = []
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\n")
        if body.startswith("| ") and body.count("|") == 5:
            cells = [c.strip() for c in body.strip("|").split("|")]
            if cells[0] in derived:
                cells[1] = derived[cells[0]]
                body = "| " + " | ".join(cells) + " |"
                line = body + ("\n" if line.endswith("\n") else "")
        out.append(line)
    return "".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="سطرُ العقد — خاناتٌ تُشتقُّ لا تُكتَب")
    ap.add_argument("--check", action="store_true",
                    help="مصادمةُ الوثيقة بمواضعها، والخروجُ بـ1 عند أوّل انحراف")
    ap.add_argument("--write", action="store_true",
                    help="كتابةُ الخانات المشتقّة في SOURCES.md")
    args = ap.parse_args(argv)
    if args.check == args.write:
        ap.error("اختر --check أو --write، لا كليهما ولا واحدَ منهما")

    with open(DOC, encoding="utf-8") as fh:
        text = fh.read()

    if args.write:
        new = rewrite(text)
        if new != text:
            with open(DOC, "w", encoding="utf-8") as fh:
                fh.write(new)
        for key, value in measure().items():
            print(f"  {key} = {value}")
        print("سطرُ العقد مكتوبٌ من مواضعه ✓" if new != text
              else "سطرُ العقد موافقٌ مواضعَه — لا تبديل ✓")
        return E_OK

    bad = drifts(text)
    for key, written, derived in bad:
        print(f"::error::سطرُ العقد يعلن «{key} = {written}» وموضعُه يعطي {derived}",
              file=sys.stderr)
    if bad:
        print(f"صريخ: {len(bad)} خانةً خالفت موضعَها — أعِد التوليد بـ--write",
              file=sys.stderr)
        return E_DRIFT
    print(f"سطرُ العقد: {len(measure())} خاناتٍ مُصادَمةٍ بمواضعها بفارق صفر ✓")
    return E_OK


if __name__ == "__main__":
    sys.exit(main())
