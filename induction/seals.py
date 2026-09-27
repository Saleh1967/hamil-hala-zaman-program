# seals.py — سجلُّ الأختام الحيّة: لا رقمَ إلا بمولِّدٍ يُشغَّل، ولا رقمَ إلا باسم دالّتِه ومقامِه.
#
# العلّةُ التي يقتلها هذا الملفّ: الأرقامُ المختومة كانت ثوابتَ ميتةً تُقارَن وتُطبع، فيبقى
# الرقمُ معروضًا وإن مات مولِّدُه — أو يتغيّر صامتًا وإن بقي اسمُه. وهنا يصير كلُّ ختمٍ
# **ستّةَ حقولٍ معًا**، لا يُقبَل ناقصًا:
#     ① اسمٌ  ② وديعةٌ (ملفُّ JSON ومسارُ المفتاح داخله)  ③ قيمةٌ متوقَّعة
#     ④ دالّةٌ مولِّدة  ⑤ مقامٌ (التيارُ وشرطُه)  ⑥ صنفٌ: [بوّابة] تحكم · [شاهد] يُعرَض ولا يحكم
#
# ولِمَ الدالّةُ حقلٌ مستقلّ؟ لأنّ العطلَ الذي كشفته ليلةُ الإقفال كان **اسمًا واحدًا على
# مقامين حسابيين**: «H(البوّابة|سابقتها)» طُبع مرّةً 1.2050 ومرّةً 1.3985، والفرقُ لم يكن
# اتفاقيتين بل جدولَ نصفِ التدريب على مقاماتِ الأزواج كلِّها. فالاسمُ وحدَه لا يكفي.
#
# آليّةُ الحياة (regen_all): لكلِّ وديعةٍ يُشغَّل مولِّدُها إلى ملفٍّ طازجٍ في /tmp، ثمّ:
#     أ) تُصادَم الوديعةُ المودَعة بالطازج — فارقٌ صفرٌ أو صريخ.
#     ب) يُقرَأ كلُّ ختمٍ **من الطازج لا من الوديعة** — فلا يشهد الرقمُ لنفسه.
#     ج) مسارٌ مفقودٌ صريخٌ **ولو كان الختمُ [شاهدًا]** — فلا يبقى رقمٌ لا يولَّد.
# وتغييرُ رقمٍ مختومٍ لا يمرّ إلا بتعديلٍ معلنٍ في هذا الملفّ، مقرونٍ بفاتورته في رسالة الالتزام.
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

GATE = "[بوّابة]"      # رقمٌ يحكم: يمنع دمجًا، أو يَسقط به حكم
WITNESS = "[شاهد]"     # رقمٌ يُعرَض ولا يحكم — ويُولَّد مع ذلك، فالعرضُ ليس إعفاءً


def S(اسم, وديعة, مسار, قيمة, دالّة, مقام, صنف):
    """ختمٌ سداسيُّ الحقول — لا يُقبَل ناقصًا."""
    assert صنف in (GATE, WITNESS), f"صنفٌ غيرُ معلنٍ للختم {اسم}"
    assert دالّة and مقام, f"ختمٌ بلا دالّةٍ أو بلا مقام: {اسم}"
    return dict(اسم=اسم, وديعة=وديعة, مسار=tuple(مسار), قيمة=قيمة,
                دالّة=دالّة, مقام=مقام, صنف=صنف)


# المولِّدات: وديعةٌ ⟵ سطرُ تشغيلِها (تُكتب إلى ملفٍّ طازجٍ ثمّ تُصادَم).
GENERATORS = {
    "results.json": ["induction/induction_engine.py", "--require-corpus"],
    "online_peel.json": ["induction/online_peel.py"],
    "mirror.json": ["induction/mirror.py"],
    "deposit_law.json": ["induction/deposit_law.py"],
    "tensor_law.json": ["induction/tensor_law.py"],
    "jami3_mani3.json": ["induction/jami3_mani3.py"],
    "hiyad.json": ["induction/hiyad.py"],
}

SEALS = [
    # ——— الاستقراء: تيارُ بوّابات الآيات ———
    S("إنتروبيا البوّابة الشرطية", "results.json", ("مقيس", "H_cond"), 1.398473785338209,
      "run_gates ⟵ gate()", "بوّابات الآيات بالعبور · الجدولُ والمقاماتُ من الأزواج كلِّها (6,235)",
      GATE),
    S("أزواج العبور", "results.json", ("مقيس", "Np"), 6235,
      "run_gates", "بوّابات الآيات بالعبور — حدُّ الآية يُعبَر معلنًا", GATE),
    S("بوّابة العطف C", "results.json", ("مقيس", "marginal", "C"), 2888,
      "gate()", "مدخلُ كلِّ آيةٍ من 6,236 — وَ/فَ مفتوحةً", GATE),
    S("بوّابة التنوين T", "results.json", ("مقيس", "marginal", "T"), 102,
      "gate()", "مدخلُ الآية — خاتمةُ تنوينٍ أو تنوينُ فتحٍ مزاحٌ قبل ا/ى", GATE),
    S("فاتورة الأحاديّ", "results.json", ("مقيس", "unigram", 0), 4518.0773095090935,
      "invoice_unigram", "نصفُ التدريب 3,118 زوجًا · α=1 · خليةٌ log2(Ntr+1)", GATE),
    S("فارق الجشع عن الاستنفاد", "results.json", ("مقيس", "gap"), 0.0,
      "greedy_path ⟷ invoice_for", "الأقسامُ الـ52 كلُّها بحراسة ستيرلنج", GATE),
    S("خلايا الحقل 112 المشغولة", "results.json", ("مقيس", "حقل112", "alphabet"), 108,
      "run_field112", "مواضعُ الحقل 112 المرخَّصة — 223,611 موضعًا", GATE),

    # ——— التقشير الفوريّ ———
    S("مقشور فوريًّا", "online_peel.json", ("التقشير_الفوري", "أحوال", "مقشور"), 17979,
      "run() ⟵ peel", "المجمَّد 77,801 كلمةً · جدولُ 11 لاحقةً معلنة", GATE),
    S("باب «ي» حاكمًا (فوريّ)", "online_peel.json",
      ("التقشير_الفوري", "الجولة_الثالثة", "أحوال_فوريّ", "حارس-النسق(ي)"), 1495,
      "run2 ⟵ peel2", "شاهدُ النسق: الجذعُ شُوهد بلاحقةٍ أخرى — فوريًّا لا دفعيًّا", GATE),
    S("باب «ي» دفعيًّا عرضًا", "online_peel.json",
      ("التقشير_الفوري", "الجولة_الثالثة", "أحوال_دفعيّ_عرضًا", "حارس-النسق(ي)"), 1404,
      "run2 (دفعيّ)", "المقامُ الدفعيّ — عرضٌ موسومٌ لا يُجسَر بالفوريّ (فارق 91)", WITNESS),

    # ——— المرآة ———
    S("إجماع المرآة", "mirror.json", ("المرآة", "إجماع"), 0.0649,
      "run ⟵ build/peel", "77,801 كلمةً · الجدولُ المودَع", WITNESS),
    S("المرآة النزيهة", "mirror.json",
      ("المرآة", "إعادةُ_الاختبار", "المرآةُ_النزيهة", "نسبةٌ_على_الكلّ"), 0.3174,
      "honest_mirror", "بلا جذعٍ مخزَّن — وهذه **تكذب** فهي مرآةٌ حقًّا", GATE),
    S("تكذيبُ الهوية بجدولٍ فارغ", "mirror.json",
      ("المرآة", "إعادةُ_الاختبار", "الهويةُ_تحصيلُ_حاصل", "تجارِبُ_التكذيب", "جدولٌ_فارغ", "هوية"),
      1.0, "FALSIFY_TRIALS", "جدولُ لواحقَ فارغٌ يعطي الهويةَ التامّة — فالهويةُ تحصيلُ حاصل", GATE),

    # ——— قانون الوديعة ———
    S("فاتورة المودَع عند الكلمة", "deposit_law.json",
      ("قانون_الوديعة", "السلّمُ_الفراكتاليّ", "درجات", "L2 كلمة", "ρ"), -0.004,
      "rung", "L2 الكلمة · 14,870 هيكلًا — المشغّلُ ينقلب عند الكلمة", GATE),
    S("انحلال L3", "deposit_law.json",
      ("قانون_الوديعة", "السلّمُ_الفراكتاليّ", "درجات", "L3 آية", "انحلال"), 0.9708,
      "rung ⟵ حارسُ الانحلال", "|Σ|/N فوق العتبة — فرقمُ L3 لا يُنقَل", GATE),

    # ——— دعوى التنسور ———
    S("فاتورة التنسور", "tensor_law.json",
      ("دعوى_التنسور", "T2_تفنيد", "الفاتورةُ_ترفض", "جداول", "التنسور كما هو", "فائدة"), 69037,
      "tensor_bill", "الأساس 1,737,746 بتًّا — Δ موجبٌ ⟹ ترفض الوديعة", GATE),
    S("الميم لها منازع", "tensor_law.json",
      ("دعوى_التنسور", "T1_تصديق", "الميم", "ميم-بلا-منازع"), 1164,
      "run ⟵ T₁", "المدَّعى «بلا منازع» — والشاهدُ المضادّ من البايتات يكسره", WITNESS),

    # ——— الجامع المانع ———
    S("فاتورة الحقل 112", "jami3_mani3.json", ("البناءُ_الجامع_المانع", "الحَكَم", "فرق"), -310993,
      "verdict", "الخامُ 2,694,034 ⟷ الحقلُ 2,383,040 — Δ سالبٌ ⟹ وديعةٌ صالحة", GATE),
    S("خلايا مشغولة (جامع)", "jami3_mani3.json",
      ("البناءُ_الجامع_المانع", "الجامع", "خلايا_مشغولة"), 108,
      "partition", "قسمةُ التضمين والاستبعاد — تُصادَم بـfield112_laws.json", GATE),

    # ——— دعوى الحياد ———
    S("فاتورة طيّ الألف", "hiyad.json", ("دعوى_الحياد", "الحَكَم", "ا", "فرق"), 24145,
      "bill", "طيُّ الألف وسمًا — Δ موجبٌ ⟹ يُرفَض", GATE),
    S("فاتورة طيّ و/ي", "hiyad.json", ("دعوى_الحياد", "الحَكَم", "وي", "فرق"), -5427,
      "bill", "طيُّ العلّتين وسمًا — Δ سالبٌ ⟹ يُقبَل", GATE),
]


def dig(obj, path, name):
    """يشقُّ المسارَ في المخرَج الطازج — والمفقودُ صريخٌ ولو كان الختمُ [شاهدًا]."""
    cur = obj
    for key in path:
        if isinstance(cur, list):
            if not isinstance(key, int) or key >= len(cur):
                raise KeyError(f"الختم «{name}»: المسارُ {path} انقطع عند {key!r}")
            cur = cur[key]
        elif isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            raise KeyError(f"الختم «{name}»: المسارُ {path} انقطع عند {key!r} — "
                           f"رقمٌ بلا مولِّدٍ حيّ")
    return cur


def regenerate(deposit, outdir):
    """يشغّل مولِّدَ الوديعة إلى ملفٍّ طازجٍ ويُرجع محتواه — لا يُقرَأ رقمٌ من الوديعة نفسِها."""
    argv = GENERATORS[deposit]
    fresh = os.path.join(outdir, deposit)
    cmd = [sys.executable, os.path.join(ROOT, argv[0])] + argv[1:] + ["--json", fresh]
    if argv[0].endswith("induction_engine.py"):      # محرّكُ الاستقراء يأخذ --json=قيمة
        cmd = [sys.executable, os.path.join(ROOT, argv[0]), f"--json={fresh}"] + argv[1:]
    run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if run.returncode != 0:
        raise RuntimeError(f"مولِّدُ {deposit} سقط:\n{run.stdout[-2000:]}\n{run.stderr[-2000:]}")
    with open(fresh, encoding="utf-8") as fh:
        return json.load(fh)


def regen_all(verbose=True):
    """يعيد توليدَ كلِّ وديعةٍ وكلِّ ختمٍ ويصادمُهما — فارقٌ صفرٌ أو صريخ."""
    problems, checked = [], 0
    with tempfile.TemporaryDirectory() as tmp:
        for deposit in GENERATORS:
            fresh = regenerate(deposit, tmp)
            with open(os.path.join(HERE, deposit), encoding="utf-8") as fh:
                stored = json.load(fh)
            if fresh != stored:
                problems.append(f"{deposit}: الوديعةُ المودَعة خالفت ما يُنتجه مولِّدُها")
                if verbose:
                    print(f"::error::{problems[-1]}")
                continue
            if verbose:
                print(f"{deposit} مُعادةُ الإنتاج بفارق صفر ✓")
            for seal in SEALS:
                if seal["وديعة"] != deposit:
                    continue
                checked += 1
                try:
                    got = dig(fresh, seal["مسار"], seal["اسم"])
                except KeyError as exc:
                    problems.append(str(exc))
                    if verbose:
                        print(f"::error::{exc}")
                    continue
                if got != seal["قيمة"]:
                    problems.append(f"الختم «{seal['اسم']}» {seal['صنف']}: "
                                    f"المتوقَّع {seal['قيمة']} · المولَّد {got} — "
                                    f"({seal['دالّة']} · {seal['مقام']})")
                    if verbose:
                        print(f"::error::{problems[-1]}")
                elif verbose:
                    print(f"    ✓ {seal['صنف']} {seal['اسم']} = {got}  "
                          f"⟵ {seal['دالّة']} · {seal['مقام']}")
    if verbose:
        n_gate = sum(1 for s in SEALS if s["صنف"] == GATE)
        print(f"\nالأختام: {checked} مصادَمًا من {len(SEALS)} مسجَّلًا "
              f"({n_gate} {GATE} · {len(SEALS) - n_gate} {WITNESS}) — "
              f"{'كلُّها بفارق صفر ✓' if not problems else f'سقط منها {len(problems)} ✗'}")
    return problems


def falsify(verbose=True):
    """هل يستطيع هذا الحارسُ أن يرفض؟ — ثلاثُ تجارِبَ مكذِّبةٍ على نسخٍ في الذاكرة."""
    trials = {}
    sample = {"مقيس": {"H_cond": 1.398473785338209, "marginal": {"C": 2888}}}

    try:
        dig(sample, ("مقيس", "لا_وجود_له"), "تجربة")
        trials["مسارٌ مفقود"] = "لم يرفض ✗"
    except KeyError:
        trials["مسارٌ مفقود"] = "رفض ✓"

    got = dig(sample, ("مقيس", "H_cond"), "تجربة")
    trials["قيمةٌ مبدَّلة"] = "رفض ✓" if got != 1.2050 else "لم يرفض ✗"

    witness = [s for s in SEALS if s["صنف"] == WITNESS][0]
    try:
        dig({}, witness["مسار"], witness["اسم"])
        trials["شاهدٌ بلا مسار"] = "لم يرفض ✗"
    except KeyError:
        trials["شاهدٌ بلا مسار"] = "رفض ✓ — العرضُ ليس إعفاءً من التوليد"

    try:
        S("بلا دالّة", "results.json", ("مقيس",), 1, "", "مقام", GATE)
        trials["ختمٌ بلا دالّة"] = "لم يرفض ✗"
    except AssertionError:
        trials["ختمٌ بلا دالّة"] = "رفض ✓ — لا رقمَ بلا اسم دالّتِه"

    if verbose:
        print("— تكذيبُ الحارس (هل يستطيع أن يرفض؟) —")
        for k, v in trials.items():
            print(f"    {k}: {v}")
    assert all(v.startswith("رفض") for v in trials.values()), "حارسُ الأختام لا يرفض — فهو عرض"
    return trials


def main():
    ap = argparse.ArgumentParser(description="سجلُّ الأختام الحيّة")
    ap.add_argument("--falsify-only", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()

    print("سجلُّ الأختام — لا رقمَ إلا بمولِّدٍ يُشغَّل، ولا رقمَ إلا باسم دالّتِه ومقامِه\n")
    trials = falsify()
    problems = [] if args.falsify_only else regen_all()
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"الأختام": [dict(s, مسار=list(s["مسار"])) for s in SEALS],
                       "التكذيب": trials, "سقوط": problems},
                      fh, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {args.json}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
