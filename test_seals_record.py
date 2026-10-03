#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مصادمةُ وديعةِ سجلِّ الأختام — ستُّ حرّاسٍ كُنَّ مضمَّنةً في `ci.yml` فنُقلت ههنا.

**لِمَ النقل؟** كانت هذه الحرّاسُ ستًّا مكتوبةً داخل `python - <<'PY'` في
خطوةٍ من `ci.yml`. وما سكن في قلب خطوةِ تشغيلٍ لا يُشغَّل محلّيًّا ولا يُكذَّب:
لا يعرف الكاتبُ أنّ حارسًا منها عَمِيَ إلا بدفعٍ وانتظار، ولا يستطيع أن يسأله
«هل تستطيع أن ترفض؟». فنُقلت إلى ملفٍّ يُستدعى من `ci.yml` كما هو، ويُشغَّل
محلّيًّا كما هو، **وفيه محاولاتُ تكذيبِه**: ستُّ مدخلاتٍ محرَّفةٍ يجب أن يُردَّ
كلٌّ منها بالحارس المسمّى له.

والشروطُ والنتائجُ وحالاتُ الرفضِ محفوظةٌ بأعيانها: كلُّ حارسٍ هو شرطُه نفسُه،
ونصُّ صريخه نفسُه، ومخرَجُه 1 كما كان.

الاستعمال:
    python test_seals_record.py <المودَعة> <المولَّدة>   # مصادمة
    python test_seals_record.py --falsify                # محاولاتُ التكذيب

المخارج: 0 موافقٌ · 1 حارسٌ صرخ · 2 سوءُ استعمال.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys

E_OK, E_SCREAM, E_USAGE = 0, 1, 2


class Scream(Exception):
    """صريخُ حارسٍ — نصُّه هو نفسُه ما كان يُطبَع في `ci.yml`."""


def guards(deposited, produced):
    """الحرّاسُ الستُّ على التوالي — أوّلُ صريخٍ يقطع، كما كان `sys.exit(1)` يقطع.

    ويعيد سطرَ البيان عند السلامة.
    """
    if deposited != produced:
        raise Scream("seals.json المودَع خالف ما يُنتجه السجلّ — صريخ")

    R = produced["سجلُّ_الأختام"]
    if R["أختامٌ_بلا_مولِّد"]:
        raise Scream(f"أختامٌ بلا مولِّدٍ حيّ: {R['أختامٌ_بلا_مولِّد']} — صريخ")
    if R["ودائعُ_خالفت"] or R["أختامٌ_انحرفت"]:
        raise Scream(f"انحرافٌ: {R['ودائعُ_خالفت']} · {R['أختامٌ_انحرفت']} — صريخ")
    if not all(t["مرفوضة"] for t in R["اختبارُ_التكذيب"]):
        raise Scream("سجلُّ الأختام لا يستطيع أن يرفض — حارسٌ أعمى — صريخ")

    # وعاءُ [مكتشَف]: قياسٌ من مصدرٍ غيرِ مختومٍ يُرجِّح ولا يحكم. والحارسُ ههنا يقرأ
    # **الوديعةَ المولَّدة** لا النصَّ: أيُّ مكتشَفٍ فقد وسمَه أو ادّعى صنفَ بوّابةٍ يُسقط
    # الخطوة. والسجلُّ فارغٌ اليوم بإعلانٍ، فالمفحوصُ بنيتُه — ولا يُسكَت عن انزلاقه.
    disc = R["مكتشَفات"]
    bad = [d["اسم"] for d in disc
           if d["صنف"] != "[مكتشَف]" or d["وسم"] != "غير مختوم"]
    if bad:
        raise Scream(f"مكتشَفٌ فقد وسمَه أو ادّعى صنفًا حاكمًا: {bad} — صريخ")
    if R["سجلُّ_الترشيح"]["الكلّ"] != len(disc):
        raise Scream("سجلُّ الترشيح يخالف عددَ المكتشَفات — صريخ")

    return (f"أختامٌ حيّةٌ مصادَمة: {R['بوّابات']} بوّابةً · {R['شواهد']} شاهدًا "
            f"· {len(disc)} مكتشَفًا خارجَ الحكم ✓")


# ــ محاولاتُ التكذيب: مدخلٌ محرَّفٌ لكلِّ حارسٍ، واسمُ الحارس المنتظَرِ معه ــــــــ
def _mismatched(d):
    d["سجلُّ_الأختام"]["بوّابات"] += 1
    return d


def _no_generator(d):
    d["سجلُّ_الأختام"]["أختامٌ_بلا_مولِّد"] = ["ختمٌ مصنوعٌ بلا مولِّد"]
    return d


def _drifted(d):
    d["سجلُّ_الأختام"]["أختامٌ_انحرفت"] = ["ختمٌ مصنوعٌ انحرف"]
    return d


def _blind(d):
    d["سجلُّ_الأختام"]["اختبارُ_التكذيب"] = [dict(محاولة="مصنوعة", مرفوضة=False)]
    return d


def _unmarked_discovery(d):
    d["سجلُّ_الأختام"]["مكتشَفات"] = [dict(اسم="مصنوع", صنف="[بوّابة]", وسم="مختوم")]
    d["سجلُّ_الأختام"]["سجلُّ_الترشيح"]["الكلّ"] = 1
    return d


def _ledger_mismatch(d):
    d["سجلُّ_الأختام"]["سجلُّ_الترشيح"]["الكلّ"] += 1
    return d


# والحقلُ الرابع **مُعلَنٌ لا مطويّ**: أيُحرَّف الطرفان أم المولَّدةُ وحدَها؟
#   فحارسُ المطابقةِ الأوّلُ يسبق الخمسةَ الباقية، فلو حُرِّفت المولَّدةُ وحدَها
#   لَرُدَّت كلُّ محاولةٍ بصريخه هو ولَبقيت الخمسةُ غيرَ مُجرَّبة — وذلك حارسٌ
#   يُظَنُّ مُكذَّبًا وهو لم يُمَسّ.
TRIALS = (
    ("المودَعةُ خالفت المولَّدة", _mismatched, "خالف ما يُنتجه السجلّ", False),
    ("ختمٌ بلا مولِّدٍ حيّ", _no_generator, "أختامٌ بلا مولِّدٍ حيّ", True),
    ("ختمٌ انحرف", _drifted, "انحرافٌ", True),
    ("حارسٌ أعمى لا يرفض", _blind, "لا يستطيع أن يرفض", True),
    ("مكتشَفٌ ادّعى صنفًا حاكمًا", _unmarked_discovery, "ادّعى صنفًا حاكمًا", True),
    ("سجلُّ الترشيح خالف عدَّتَه", _ledger_mismatch, "يخالف عددَ المكتشَفات", True),
)


def falsify(produced):
    """كلُّ تحريفٍ يجب أن يُردَّ بصريخه هو — ونجاحُ واحدٍ منها يعني حارسًا أعمى."""
    passed = []
    for name, break_it, needle, both in TRIALS:
        broken = break_it(copy.deepcopy(produced))
        try:
            guards(copy.deepcopy(broken if both else produced), broken)
        except Scream as exc:
            if needle not in str(exc):
                raise AssertionError(
                    f"المحاولة «{name}» رُدَّت بصريخٍ آخر: {exc}") from None
            passed.append(name)
        else:
            raise AssertionError(f"المحاولة «{name}» لم تُردّ — الحارسُ أعمى")
    return passed


def main(argv=None):
    ap = argparse.ArgumentParser(description="مصادمةُ وديعةِ سجلِّ الأختام")
    ap.add_argument("deposited", nargs="?", help="induction/seals.json")
    ap.add_argument("produced", nargs="?", help="مخرَجُ --json الطازج")
    ap.add_argument("--falsify", action="store_true",
                    help="محاولاتُ تكذيبِ الحرّاس على المخرَج الطازج")
    args = ap.parse_args(argv)
    if not args.deposited or not args.produced:
        ap.error("يلزم مساران: المودَعةُ والمولَّدة")

    with open(args.deposited, encoding="utf-8") as fh:
        deposited = json.load(fh)
    with open(args.produced, encoding="utf-8") as fh:
        produced = json.load(fh)

    try:
        line = guards(deposited, produced)
    except Scream as exc:
        print(f"::error::{exc}")
        return E_SCREAM
    print(line)

    if args.falsify:
        passed = falsify(produced)
        print(f"محاولاتُ التكذيب: {len(passed)} رُدَّت كلُّها ✓")
    return E_OK


if __name__ == "__main__":
    sys.exit(main())
