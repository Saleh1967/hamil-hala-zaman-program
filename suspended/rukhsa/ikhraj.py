#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""إخراجُ الحاويات — صكُّ تفويضٍ موقَّعٌ بالبايتات، وبرهانُ استردادٍ قبل الحذف.

**لِمَ أداةٌ لا أمرُ `git rm`؟** لأنّ حذفَ بايتاتٍ لا يملكها المشروعُ قرارٌ لا
رجعةَ فيه إن ضاع أصلُها، و`git rm` لا يسأل: أمستردّةٌ هي؟ وبإذنِ من؟ فالأداةُ
تجعل الإخراجَ **فعلًا مشروطًا بثلاثة** لا واحدٍ منها نثرٌ:

  ① **تفويضٌ بيد المالك** — `RUKHSA_EJECT_OWNER=1`، كما يُختَم المصدرُ في
     `fetch_source.sh` بـ`SOURCES_SEAL_OWNER=1`. لا تُخرِج آلةٌ ما لم يأذن مالكُه.
  ② **توقيعٌ على البايتات لا على الاسم** — الصكُّ أدناه يسمّي كلَّ حاويةٍ بختمها
     الثلاثيِّ (بصمةُ كائن git · الطول · sha256). فلو بُدِّلت بايتاتُ ملفٍّ تحت
     اسمِه المأذونِ فيه سقط الإذنُ عنه: التوقيعُ على ما قيس لا على ما سُمّي،
     ولا تركب حاويةٌ غريبةٌ موجةَ إذنٍ أُعطي لغيرها.
  ③ **برهانُ الاستردادِ قبل الحذف** — لا تُحذَف بايتةٌ حتى تُقرأ من إيداعٍ مثبَّتٍ
     في التاريخ وتُصادَم بختمها. فالإخراجُ نقلٌ من الرأس إلى التاريخ، لا إعدام.

وبعد التنفيذ تبقى الأداةُ حارسًا لا أثرًا: `--check` يُشغَّل في CI فيصادم الصكَّ
بحال الشجرة — فعودةُ حاويةٍ إلى الرأس، أو انقطاعُ استردادها من التاريخ، كلتاهما
تُسقِط البابَ من لحظتها.

الاستعمال:
    python rukhsa/ikhraj.py              # تقريرٌ معدود: أمستردّةٌ؟ أخارجةٌ؟
    python rukhsa/ikhraj.py --check      # مصادمةُ الصكِّ بحال الشجرة (CI)
    python rukhsa/ikhraj.py --falsify    # محاولاتُ تكذيبِ الحرّاس
    RUKHSA_EJECT_OWNER=1 python rukhsa/ikhraj.py --eject   # بيد المالك وحدَه

المخارج: 0 موافقٌ · 1 حارسٌ صرخ · 2 سوءُ استعمال · 3 تفويضٌ غائب.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "sources_manifest.tsv")

E_OK, E_SCREAM, E_USAGE, E_NO_WRIT = 0, 1, 2, 3

OWNER_ENV = "RUKHSA_EJECT_OWNER"

# ═══ ① صكُّ التفويض ═════════════════════════════════════════════════════════
# نصُّ إذنِ المالك منقولٌ بحرفه لا مُعادٌ بصياغتنا — لأنّ المُعادَ صياغتُه إذنُ
# الكاتبِ لا إذنُ الآذِن. والتاريخُ معه، فالإذنُ حادثةٌ مؤرَّخةٌ لا حالٌ دائمة.
WRIT = {
    "المالك": "Saleh1967 (صالح الغانم) — صاحبُ حقوق هذا المستودع في LICENSE",
    "التاريخ": "2026-10-04",
    "نصُّ_الإذن": "اخرج الحاويات وفق افضل الممارسات بتفويض المالك وتوقيعه",
    "التوقيع": f"{OWNER_ENV}=1 على بايتاتٍ مسمّاةٍ بختمها الثلاثيِّ أدناه",
    "حدُّ_الإذن": (
        "إخراجُ الحاويات الثلاثِ المسمّاةِ ههنا من رأس الشجرة وحدَه. "
        "ولا يَمنح هذا الصكُّ: إعادةَ كتابةِ التاريخ، ولا حذفَ مستخرَجاتها "
        "المودَعة، ولا إخراجَ ملفٍّ لم يُسمَّ ولم يُقَس ههنا."
    ),
}

# الحاوياتُ المأذونُ في إخراجها — كلُّ واحدةٍ مقيَّدةٌ بأربعة: مسارُها في الرأس،
# ومعرِّفُها في البيان، وإيداعُ التاريخ الذي تُستردُّ منه، وختمُها الثلاثيّ.
# فالإذنُ لا يُقرأ على اسمٍ وحدَه: يُقرأ على بايتاتٍ بعينها مسمّاةٍ بأربعين محرفًا.
CONTAINERS = (
    {
        "المعرِّف": "shakhsiyya_j1",
        "المسار": "الشخصية الإسلامية الجزء الأول (1).docx",
        "الإيداع": "b7abcad328db8a69349e02ef3e4ad4076b1a7486",
        "بصمةُ_الكائن": "7de0bc2bfb71ba0c85003b44e7c7d7ccbf7d9ec4",
        "الطول": 283112,
        "sha256": "5e327aa2563af094962833951972b7537a872119a58bbfce5f2a813d20c88e17",
    },
    {
        "المعرِّف": "shakhsiyya_j3",
        "المسار": "الشخصية الاسلامية الجزء الثالث ورد (2).docx",
        "الإيداع": "b7abcad328db8a69349e02ef3e4ad4076b1a7486",
        "بصمةُ_الكائن": "3529f2f21e53391e4c11caa64adf38bc86713814",
        "الطول": 673537,
        "sha256": "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd",
    },
    {
        "المعرِّف": "surca_badiha",
        "المسار": "سرعة البديهة.docx",
        "الإيداع": "2bb18501598278bb3facac84e60cff5bb4b25219",
        "بصمةُ_الكائن": "f9f1c3f422b574d44a12c32bee8f4d908b40d86f",
        "الطول": 74472,
        "sha256": "483cf19f6153cfb31bb6d965e1b7da6927f330633b49c586360f3567798bc161",
    },
)

CONTAINER_EXT = ".docx"


class Scream(Exception):
    """صريخُ حارسٍ — نصُّه هو حكمُه."""


# ═══ ② القياس من البايتات ═══════════════════════════════════════════════════
def _git(*args, binary=False):
    run = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if run.returncode != 0:
        return None
    return run.stdout if binary else run.stdout.decode("utf-8")


def tracked():
    """ملفّاتُ الرأس كما يعدّها git — لا مشطٌ لنظام الملفّات يلتقط غيرَ المودَع."""
    out = _git("ls-files", "-z")
    if out is None:
        raise Scream("تعذّرت قراءةُ شجرة git — ولا يُقاس على غيابٍ مطويّ")
    return [p for p in out.split("\0") if p]


def retrieve(entry):
    """يستردُّ بايتاتِ الحاوية من إيداعها المثبَّت ويقيسها — ولا يقرأ شجرةَ العمل.

    ثلاثةُ أوجهٍ تُقاس ولا تُنقَل: بصمةُ كائن git (هي شهادةُ المصدر)، والطول،
    وsha256. والمسارُ يُقرأ **داخل** الإيداع لا في الرأس — فالإخراجُ لا يمسّه.
    """
    got = {"المعرِّف": entry["المعرِّف"], "إيداعٌ حاضر": False,
           "كائنٌ حاضر": False, "بصمةٌ طابقت": False,
           "طولٌ طابق": False, "sha256 طابقت": False, "مستردّة": False}

    if _git("rev-parse", "--verify", "-q", entry["الإيداع"] + "^{commit}") is None:
        return got
    got["إيداعٌ حاضر"] = True

    obj = _git("rev-parse", "--verify", "-q",
               f"{entry['الإيداع']}:{entry['المسار']}")
    if obj is None:
        return got
    obj = obj.strip()
    got["كائنٌ حاضر"] = True
    got["بصمةٌ طابقت"] = obj == entry["بصمةُ_الكائن"]

    raw = _git("cat-file", "blob", obj, binary=True)
    if raw is None:
        return got
    got["طولٌ طابق"] = len(raw) == entry["الطول"]
    got["sha256 طابقت"] = hashlib.sha256(raw).hexdigest() == entry["sha256"]
    got["مستردّة"] = all(got[k] for k in
                         ("بصمةٌ طابقت", "طولٌ طابق", "sha256 طابقت"))
    return got


def census(files=None):
    """حالُ الصكِّ مقيسةً: أخارجةٌ من الرأس؟ أمستردّةٌ من التاريخ؟"""
    files = tracked() if files is None else files
    head = set(files)
    rows = []
    for entry in CONTAINERS:
        row = dict(retrieve(entry))
        row["في الرأس"] = entry["المسار"] in head
        rows.append(row)

    # وحاوياتُ الرأس تُمشَّط بالامتداد لا بأسماء الصكّ: فحاويةٌ تدخل باسمٍ لم
    # يُؤذَن فيه تُلتقَط ههنا ولا تمرّ لأنّ الصكَّ لا يسمّيها.
    return {
        "صفوف": rows,
        "خانات": {
            "حاوياتٌ في الصكّ": len(CONTAINERS),
            "حاوياتٌ في الرأس": sum(1 for f in files
                                    if f.lower().endswith(CONTAINER_EXT)),
            "حاوياتٌ مستردَّةٌ من التاريخ": sum(1 for r in rows if r["مستردّة"]),
            "بايتاتٌ خرجت من الرأس": sum(e["الطول"] for e in CONTAINERS),
        },
    }


# ═══ ③ الحرّاس ══════════════════════════════════════════════════════════════
def guards(got):
    """ثلاثةُ حرّاسٍ — أوّلُ صريخٍ يقطع، ويعيد سطرَ الحال عند السلامة."""
    cells = got["خانات"]

    # ① لا تُحذَف بايتةٌ لا تُستردّ — وهذا الحارسُ يَحرُس بعد التنفيذ كما قبله.
    lost = [r["المعرِّف"] for r in got["صفوف"] if not r["مستردّة"]]
    if lost:
        raise Scream(f"حاويةٌ لا تُستردُّ من التاريخ: {lost} — "
                     "الإخراجُ نقلٌ إلى التاريخ لا إعدام")

    # ② الصكُّ منفَّذٌ: ما أُذِن في إخراجه خارجٌ من الرأس، فعودتُه نقضٌ صامت.
    back = [r["المعرِّف"] for r in got["صفوف"] if r["في الرأس"]]
    if back:
        raise Scream(f"حاويةٌ عادت إلى الرأس بعد إخراجها: {back} — "
                     "الصكُّ يُنفَّذ أو يُنقَض بيدٍ معلنة، ولا يشيخ صامتًا")

    # ③ ولا حاويةَ خارجَ الصكّ: الامتدادُ يُمشَّط فلا يدخل ما لم يُؤذَن فيه.
    if cells["حاوياتٌ في الرأس"]:
        raise Scream(f"{cells['حاوياتٌ في الرأس']} حاويةً في الرأس لم يسمِّها "
                     "الصكّ — ما لا يملكه المشروعُ لا يدخل رأسَه")

    return (f"صكُّ الإخراج: {cells['حاوياتٌ في الصكّ']} حاويةً مأذونًا فيها · "
            f"{cells['حاوياتٌ مستردَّةٌ من التاريخ']} مستردَّةً من التاريخ · "
            f"صفرُ حاويةٍ في الرأس · {cells['بايتاتٌ خرجت من الرأس']:,} "
            "بايتةً خرجت ✓")


# ═══ ④ التنفيذ — بيد المالك وحدَه ═══════════════════════════════════════════
def eject(dry_run=False):
    """يُخرج الحاوياتِ المأذونَ فيها — ولا بايتةَ تُحذَف قبل أن تُستردّ وتُصادَم."""
    if os.environ.get(OWNER_ENV) != "1":
        raise SystemExit(
            f"الإخراجُ بيد المالك وحدَه: {OWNER_ENV}=1 "
            f"python rukhsa/ikhraj.py --eject\n"
            f"  الإذنُ المنقولُ في الصكّ: «{WRIT['نصُّ_الإذن']}» ({WRIT['التاريخ']})")

    head = set(tracked())
    done, already = [], []
    for entry in CONTAINERS:
        got = retrieve(entry)
        if not got["مستردّة"]:
            raise Scream(
                f"«{entry['المعرِّف']}» لا يُستردُّ من {entry['الإيداع'][:7]} "
                f"({got}) — لا تُحذَف بايتةٌ لا تُقرَأ من التاريخ")
        if entry["المسار"] not in head:
            already.append(entry["المعرِّف"])
            continue
        if dry_run:
            done.append(entry["المعرِّف"])
            continue
        run = subprocess.run(["git", "-C", ROOT, "rm", "--quiet", "--",
                              entry["المسار"]], capture_output=True, text=True)
        if run.returncode != 0:
            raise Scream(f"تعذّر إخراجُ «{entry['المعرِّف']}»: {run.stderr.strip()}")
        done.append(entry["المعرِّف"])
    return done, already


# ═══ ⑤ محاولاتُ التكذيب ═════════════════════════════════════════════════════
def _back_in_head(got):
    import copy
    broken = copy.deepcopy(got)
    broken["صفوف"][0]["في الرأس"] = True
    return broken


def _unretrievable(got):
    import copy
    broken = copy.deepcopy(got)
    broken["صفوف"][0]["مستردّة"] = False
    return broken


def _stray_container(got):
    import copy
    broken = copy.deepcopy(got)
    broken["خانات"]["حاوياتٌ في الرأس"] = 1
    return broken


TRIALS = (
    ("حاويةٌ عادت إلى الرأس", _back_in_head, "عادت إلى الرأس"),
    ("حاويةٌ انقطع استردادُها", _unretrievable, "لا تُستردُّ من التاريخ"),
    ("حاويةٌ لم يسمِّها الصكّ", _stray_container, "لم يسمِّها"),
)


def falsify(got):
    passed = []
    for name, break_it, needle in TRIALS:
        try:
            guards(break_it(got))
        except Scream as exc:
            if needle not in str(exc):
                raise AssertionError(
                    f"المحاولة «{name}» رُدَّت بصريخٍ آخر: {exc}") from None
            passed.append(name)
        else:
            raise AssertionError(f"المحاولة «{name}» لم تُردّ — الحارسُ أعمى")
    return passed


# ═══ ⑥ المُشغِّل ════════════════════════════════════════════════════════════
def report(got):
    print("صكُّ إخراج الحاويات — توقيعُه على البايتات لا على الأسماء\n")
    print(f"  المالك: {WRIT['المالك']}")
    print(f"  الإذن ({WRIT['التاريخ']}): «{WRIT['نصُّ_الإذن']}»")
    print(f"  حدُّه: {WRIT['حدُّ_الإذن']}\n")
    for row, entry in zip(got["صفوف"], CONTAINERS):
        mark = "✓" if row["مستردّة"] and not row["في الرأس"] else "✗"
        print(f"  {mark} {entry['المعرِّف']:<16} {entry['الطول']:>9,} بايتًا · "
              f"إيداع {entry['الإيداع'][:7]} · "
              f"{'في الرأس' if row['في الرأس'] else 'خارجَ الرأس'} · "
              f"{'مستردّة' if row['مستردّة'] else 'غيرُ مستردّة'}")
    print()
    for name, value in got["خانات"].items():
        print(f"  {name}: {value:,}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="إخراجُ الحاويات بتفويض المالك")
    ap.add_argument("--check", action="store_true", help="مصادمةُ الصكِّ بحال الشجرة")
    ap.add_argument("--falsify", action="store_true", help="محاولاتُ تكذيبِ الحرّاس")
    ap.add_argument("--eject", action="store_true", help="التنفيذُ — بيد المالك وحدَه")
    ap.add_argument("--dry-run", action="store_true", help="مع --eject: بلا حذف")
    args = ap.parse_args(argv)

    try:
        if args.eject:
            done, already = eject(dry_run=args.dry_run)
            for ident in done:
                print(f"أُخرِجت «{ident}» من الرأس — وبايتاتُها في التاريخ مستردَّةٌ "
                      f"مصادَمةً بختمها الثلاثيّ")
            for ident in already:
                print(f"«{ident}» خارجةٌ سلفًا — لا يُعاد إخراجُها")
            if not done and not already:
                print("لا حاويةَ في الصكّ")

        got = census()
        if args.falsify:
            for name in falsify(got):
                print(f"  محاولة «{name}»: رُدَّت ✓")
        if args.check or args.eject:
            print(guards(got))
        elif not args.falsify:
            report(got)
    except Scream as exc:
        print(f"صريخ: {exc}", file=sys.stderr)
        return E_SCREAM
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return E_NO_WRIT
    return E_OK


if __name__ == "__main__":
    sys.exit(main())
