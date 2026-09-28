# export_seals.py — مُصدِّرُ أختامِ [بوّابة] بإزاحاتها: نافذةٌ للقارئ البعيد، لا نسخةٌ ثانية.
#
# العلّةُ التي يقتلها هذا الملفّ: البانِي في مستودعٍ آخر (Alghanem) يحتاج مقاديرَ هذا
# المستودع ليبني عليها براهينَه. فإن نُقلت إليه أرقامًا مكتوبةً صارت **نسخةً ثانيةً
# تتخلّف** — وهو عينُ ما يمنعه البابُ الخامس ثَمَّ («سجلٌّ يخزن نسخةً ثانيةً من الرقم
# يصير هو القبرَ الذي جاء يفتحه»). فلا يُصدَّر الرقمُ وحدَه، بل **موضعُه**: الملفُّ،
# والسطرُ، والإزاحةُ بالبايتات، وبصمةُ الملفّ الذي فيه — فيقرأ البانِي الأصلَ من موضعه.
#
# والإزاحاتُ **مشتقّةٌ بـ`ast` لا مكتوبة**: تُقرأ مواضعُ استدعاءات `S(...)` في
# `seals.py` نفسِه، ويُصادَم اسمُ كلِّ استدعاءٍ باسم الختم في `SEALS` بالترتيب — فإن
# زِيد ختمٌ أو أُزيح سطرٌ تحرّكت الإزاحةُ معه، ولا تتخلّف ورقةٌ عن الشجرة.
#
# ولِمَ [بوّابة] وحدَها؟ لأنّ مادّةَ البناء ثَمَّ الأختامُ الحيّةُ التي **تحكم**؛ و[شاهد]
# يُعرَض ولا يحكم، فتصديرُه مادةَ برهانٍ يرفع عَرَضًا إلى بوّابة — وذاك تحريمُ ما لم
# يُحرَّم (البابُ السابع في `USOOL_AL-UNBOOB`). وعددُهما معًا مُعلَنٌ في المخرَج.
#
# وحاكمان لا واحد: يُصدَّر مع كلِّ ختمٍ **مصادمتُه بالوديعة** (فارقٌ صفرٌ أو مخالفة)،
# ومعها **فواتيرُ الدعاوى بإشاراتها وأحكامِها المشتقّة** من `deposit_law.verdict`.
# فصفرُ الخلاف يشهد أنّ الرقمَ يُولَّد، والفاتورةُ وحدَها تحكم أنّه ربح.
#
# وهذا المُصدِّرُ **لا يُعيد توليدَ الودائع** — تلك سلطةُ `seals.regen_all` وحدَها،
# ولا تُكرَّر ههنا. فيُعلَن في المخرَج صراحةً أنّ المصادمةَ بالمودَع لا بالطازج
# (`مصادمة_بالمودَع_لا_بالطازج`)، لئلّا تُقرأ شهادةً ليست له.
#
# المخارج: 0 نجاح · 2 استعمال · 8 إزاحةٌ لم تُشتَقّ (ast خالف SEALS) · 9 ختمٌ خالف وديعتَه.
import argparse
import ast
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

sys.path.insert(0, HERE)
import seals
from seals import (GATE, WITNESS, DISCOVERED, SEALS, DISCOVERIES,
                   deposit_path, dig)

SEALS_FILE = os.path.join(HERE, "seals.py")

EXIT_USAGE = 2
EXIT_OFFSET = 8
EXIT_DEPOSIT = 9

NOTE = ("المصادمةُ ههنا بالوديعة المودَعة لا بمخرَجٍ طازج؛ وإعادةُ التوليد سلطةُ "
        "induction/seals.py --falsify وحدَها، ولا تُكرَّر في مُصدِّر.")


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def byte_offsets(path):
    """إزاحةُ أوّلِ بايتٍ في كلّ سطرٍ من الملفّ — لتُحسَب إزاحةُ الاستدعاء بالبايتات."""
    offsets, at = [], 0
    with open(path, "rb") as fh:
        for line in fh:
            offsets.append(at)
            at += len(line)
    return offsets


def seal_call_sites():
    """مواضعُ استدعاءات S(...) **داخلَ قائمة SEALS وحدَها** — مقروءةٌ بـast لا مكتوبة.

    ويُصادَم اسمُ كلِّ استدعاءٍ باسم الختم في SEALS بالترتيب؛ فالاختلافُ يعني أنّ
    الإزاحةَ تشير إلى غير ختمِها، وهي حينئذٍ أسوأُ من غيابها.

    ولِمَ لا تُمشَّط الشجرةُ كلُّها بحثًا عن `S(`؟ لأنّ في `falsify` ختمًا مصنوعًا
    عمدًا ليُرفَض («بلا دالّة») — وهو تجربةُ تكذيبٍ لا ختمًا في السجلّ؛ فمشطُ الملفّ
    كلِّه يعدُّه ختمًا ويُزحزح الإزاحاتِ كلَّها بعده موضعًا واحدًا.
    """
    with open(SEALS_FILE, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=SEALS_FILE)
    lines = byte_offsets(SEALS_FILE)
    listing = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "SEALS" for t in node.targets):
            listing = node.value
    if not isinstance(listing, ast.List):
        raise SystemExit("::error::SEALS ليست قائمةً معلنةً في seals.py — لا إزاحةَ تُشتَقّ")
    sites = []
    for element in listing.elts:
        if not (isinstance(element, ast.Call) and isinstance(element.func, ast.Name)
                and element.func.id == "S" and element.args):
            raise SystemExit("::error::عنصرٌ في SEALS ليس استدعاءَ S — الإزاحةُ لا تُشتَقّ")
        first = element.args[0]
        name = first.value if isinstance(first, ast.Constant) else None
        sites.append((element.lineno, element.col_offset, name))
    if len(sites) != len(SEALS):
        raise SystemExit(f"::error::استدعاءاتُ S في seals.py {len(sites)} وأختامُ SEALS "
                         f"{len(SEALS)} — الإزاحةُ لا تُشتَقّ على اختلافٍ في العدّ")
    out = []
    for (lineno, col, name), seal in zip(sites, SEALS):
        if name != seal["اسم"]:
            raise SystemExit(f"::error::إزاحةُ السطر {lineno} تحمل الاسم «{name}» "
                             f"والختمُ في موضعه «{seal['اسم']}» — إزاحةٌ تشير إلى غير ختمِها")
        out.append({"ملف": "induction/seals.py", "سطر": lineno,
                    "إزاحة_بايتية": lines[lineno - 1] + col})
    return out


def deposit_reading(seal):
    """قيمةُ الختم من وديعته المودَعة، ومصادمتُها بالمختوم — صفرٌ أو مخالفةٌ مسمّاة."""
    path = deposit_path(seal["وديعة"])
    if not os.path.exists(path):
        return None, "وديعةٌ غائبةٌ عن الشجرة"
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    try:
        got = dig(doc, seal["مسار"], seal["اسم"])
    except KeyError as exc:
        return None, str(exc)
    if got != seal["قيمة"]:
        return got, f"الوديعةُ تعطي {got!r} والمختومُ {seal['قيمة']!r}"
    return got, None


def export():
    sites = seal_call_sites()
    gates, mismatches = [], []
    # [مكتشَف] **لا يُصدَّر**، ومنعُه صريحٌ لا صامت: لو صُدِّر مع أختام البوّابة لقرأه
    # المستهلكُ خارجَ الشجرة سندًا — وهو قياسٌ من مصدرٍ **غيرِ مختوم** قد ينزاح غدًا
    # فينقلب الجوابُ كاذبًا بلا إنذار. وصمتُ الغياب يحتمل السهو، والصريخُ لا يحتمله.
    for seal in SEALS:
        if seal["صنف"] == DISCOVERED:
            mismatches.append(f"{seal['اسم']}: {DISCOVERED} في SEALS — ولا يُصدَّر")
    for seal, site in zip(SEALS, sites):
        if seal["صنف"] != GATE:
            continue
        got, problem = deposit_reading(seal)
        if problem:
            mismatches.append(f"{seal['اسم']}: {problem}")
        gates.append({
            "اسم": seal["اسم"],
            "قيمة": seal["قيمة"],
            "دالّة": seal["دالّة"],
            "مقام": seal["مقام"],
            "صنف": seal["صنف"],
            "وديعة": {"ملف": os.path.relpath(deposit_path(seal["وديعة"]), ROOT),
                      "مسار_المفتاح": list(map(str, seal["مسار"])),
                      "بصمة": (sha256_of(deposit_path(seal["وديعة"]))
                               if os.path.exists(deposit_path(seal["وديعة"])) else None)},
            "إزاحة_الإعلان": site,
            "مصادمة_الوديعة": "فارقٌ صفر" if not problem else problem,
        })
    doc = {
        "مُصدِّر": "induction/export_seals.py",
        "تنبيه": NOTE,
        "بصمة_السجل": {"ملف": "induction/seals.py", "sha256": sha256_of(SEALS_FILE)},
        "العدّ": {"الكلّ": len(SEALS),
                  GATE: sum(1 for s in SEALS if s["صنف"] == GATE),
                  WITNESS: sum(1 for s in SEALS if s["صنف"] == WITNESS),
                  DISCOVERED: {"عدّ": len(DISCOVERIES),
                               "مصدَّرٌ": False,
                               "علّة": ("قياسٌ من مصدرٍ غيرِ مختوم — يُرجِّح ولا يحكم، "
                                        "فلا يُقرَأ سندًا خارج الشجرة")}},
        "أختام_البوّابة": gates,
        "الفواتير": [{"دعوى": claim, "Δ": delta, "الحكمُ_المشتقّ": حكم}
                     for claim, delta, حكم in seals._bill_rows()],
    }
    return doc, mismatches


def main():
    ap = argparse.ArgumentParser(
        description="تصديرُ أختام [بوّابة] بإزاحاتها ليقرأ البانِي الأصلَ من موضعه")
    ap.add_argument("--json", metavar="مسار", help="كتابةُ المخرَج إلى ملفّ بدل الخرج القياسي")
    args = ap.parse_args()

    try:
        doc, mismatches = export()
    except SystemExit:
        raise
    except Exception as exc:                            # noqa: BLE001 — يُسمّى العطلُ ولا يُبتلع
        print(f"::error::تعذّر التصدير: {exc}", file=sys.stderr)
        return EXIT_OFFSET

    text = json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)

    if mismatches:
        for problem in mismatches:
            print(f"::error::{problem}", file=sys.stderr)
        return EXIT_DEPOSIT
    print(f"صُدِّر {len(doc['أختام_البوّابة'])} ختمَ {GATE} بإزاحاتها — مصادمةُ الودائع بفارق صفر ✓",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as exc:
        if isinstance(exc.code, str):
            print(exc.code, file=sys.stderr)
            sys.exit(EXIT_OFFSET)
        raise
