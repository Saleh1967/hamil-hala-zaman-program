# merge_audit.py — العطبُ الذي لا يَحذِف: مصادمةُ الدمجِ بأبويه وأساسِهما.
#
# ثلاثةُ أعطابٍ وقعت في هذا المستودع من دمجين (`fc65dcb` ثمّ `ac99b42`)، وكلُّها
# من صنفٍ واحد: **إلحاقٌ أو إعادةُ ترتيبٍ لا حذف**. ولذلك لم يوقفها تعارضُ git
# (فلا تعارضَ بين إضافتين في موضعين)، ولم يُظهرها `git diff --numstat` (فلا نقصَ
# في العدّ)، ولم تُسقِطها مصادمةُ الودائع (فالنسخةُ المكرَّرةُ تقرأ الرقمَ نفسَه
# فتُصادَم بفارقِ صفر). أعطابٌ تمرُّ كلَّ حارسٍ قائمٍ ثمّ تظهر بعيدًا عن موضعها:
#   · `fc65dcb` أسقطَ 85 ختمًا من `induction/seals.py` — ظهرت بعد أسبوعٍ بـFileNotFoundError
#   · `fc65dcb` شبكَ خطوتَي «القسمة» و«الصرف» في `ci.yml` — ظهرت بـKeyError في بابٍ آخر
#   · `ac99b42` كرَّرَ الأختامَ الخمسةَ والثمانين — ظهرت بعددٍ مُشتَبَهٍ في سطرِ العقد
#
# وأداةُ الكشفِ كانت في المرّات الثلاثِ واحدةً: مصادمةُ الملفِّ بأبوَي الدمج.
# فهذه الأداةُ تلك المصادمةُ مُشغَّلةً لا موصوفة. وهي **ثلاثيّةٌ** لا ثنائيّة،
# إذ لا يُحكَم على سطرٍ إلا بمعرفةِ من أضافه: يُقاس الأساسُ (merge-base) مع
# الأبوين والدمجِ معًا، فيُشتَقُّ لكلِّ سطرٍ من أضافه ومن أسقطه.
#
# — ثلاثةُ أصنافٍ تُشتَقُّ من العددِ لا من النظر —
#   ① **سقوطٌ صامت**: غائبٌ عن الأساس · أضافه أحدُ الأبوين · والدمجُ لا يحويه.
#      أضافه أبٌ عامدًا فأسقطه الدمجُ بلا كلمة — وهو جرحُ الأختام الخمسةِ والثمانين.
#   ② **تكرارٌ صامت**: نصيبُه في الدمجِ أكثرُ من أكبرِ نصيبٍ له في أبٍ أو أساس.
#      بلغَه الأبوان من طريقين فأبقى الدمجُ النسختين — وهو جرحُ 674 ⟷ 589.
#   ③ **مُختلَقٌ في الحلّ**: لا أصلَ له في أبٍ ولا في أساس — كُتب بيدٍ عند فضِّ
#      التعارض. وهذا **يُسمّى ويُعَدُّ ولا يُسقِط**: فضُّ التعارضِ قد يوجب سطرًا
#      جديدًا بحقّ (عددٌ يُجمَع من شقّين مثلًا)، لكنّه لا يُطوى عن العين أبدًا.
#
# والأولان صريخٌ يُسقِط، والثالثُ دَينٌ معروضٌ — إذ لا يُدَّعى على المُختلَقِ أنّه
# عطبٌ، ولا يُسكَت عنه فيمرَّ كما مرَّ المفتاحُ المشوَّهُ في `seals.json`.
#
# ولا يُقاس على غيابٍ مطويّ: النسخةُ الضحلةُ (shallow) لا تحوي الأساسَ ولا
# الأبوين، فتُصرِّح الأداةُ بنقصِ التاريخِ وتخرج بمخرجه — ولا تقول «نظيفٌ» وهي
# لم تقرأ شيئًا. وهذا الفرقُ هو كلُّ الفرقِ بين حارسٍ وزينة.
#
# المخارج: 0 نظيفٌ (أو ليس دمجًا) · 2 خطأُ استعمال · 3 تكرارٌ صامت
#          · 4 سقوطٌ صامت · 5 تاريخٌ ناقصٌ لا يُقاس عليه.
#
# التشغيل:
#   python merge_audit.py                 يدقّق HEAD
#   python merge_audit.py <إيداع>         يدقّق إيداعًا بعينه
#   python merge_audit.py --json <مسار>   الأعدادُ نفسُها JSON
import argparse
import collections
import json
import os
import subprocess
import sys

E_USAGE = 2
E_DUP = 3
E_LOSS = 4
E_HISTORY = 5

ROOT = os.path.dirname(os.path.abspath(__file__))

# سطورٌ لا يُحكَم عليها: الفارغةُ ومحضُ الأقواسِ والفواصل. تكرارُها وسقوطُها
# لا يدلُّ على شيءٍ لأنّها تتكرّر بالبناء في كلِّ ملفٍّ مصدريّ، فإدخالُها في
# القياس ضجيجٌ يُغرِق الإشارة. وهي مُعلَنةٌ ههنا لا مطويّةٌ في شرط.
NOISE = {"", "]", "[", "}", "{", ")", "(", "),", "},", "],", "'''", '"""', "PY",
         "--", "---", "```", "|---|---|", "*", "#"}


def git(*args, cwd=ROOT):
    """يُشغِّل git ويُعيد مخرَجَه — والسقوطُ يُعرَض بنصِّه لا يُبتلَع."""
    run = subprocess.run(("git",) + args, cwd=cwd, capture_output=True, text=True)
    return run.returncode, run.stdout, run.stderr


def parents_of(commit):
    """أبوا الدمجِ — أو قائمةٌ دونَ اثنين إن لم يكن دمجًا."""
    code, out, err = git("rev-list", "--parents", "-n", "1", commit)
    if code != 0:
        raise LookupError(err.strip() or f"لا إيداعَ باسم {commit}")
    return out.split()[1:]


def have(rev):
    """أحاضرٌ هذا الكائنُ في النسخة؟ — النسخةُ الضحلةُ تُجيب لا."""
    return git("cat-file", "-e", f"{rev}^{{commit}}")[0] == 0


def significant(lines):
    """سطورٌ ذاتُ معنًى — والضجيجُ المُعلَنُ مطروحٌ قبلَ كلِّ قياس."""
    return [s for s in (ln.strip() for ln in lines) if s not in NOISE]


def blob_lines(rev, path):
    """سطورُ ملفٍّ عند إيداعٍ — والغائبُ قائمةٌ فارغةٌ لا سقوط."""
    code, out, _ = git("show", f"{rev}:{path}")
    return out.splitlines() if code == 0 else []


def files_of(rev_a, rev_b):
    """الملفّاتُ المتبدّلةُ بين إيداعين."""
    code, out, err = git("diff", "--name-only", rev_a, rev_b)
    if code != 0:
        raise LookupError(err.strip())
    return [p for p in out.splitlines() if p]


def ceiling(lines):
    """أطولُ كتلةٍ متّصلةٍ تتكرّر داخلَ الملفِّ نفسِه — سقفُ التكرارِ الطبيعيّ.

    وهذا هو **الحدُّ المقيسُ** الذي يُحكَم به، لا عددٌ مُختارٌ بالذوق: لكلِّ ملفٍّ
    تكرارُه المشروع (ترويسةُ خطوةٍ تتكرّر، `sys.exit(1)` يتكرّر)، فيُقاس هذا
    السقفُ في كلِّ أبٍ ثمّ يُطلَب من الدمجِ ألّا يتجاوزه. فسقفُ `seals.py` في
    الأبوين 3 وفي الدمجِ 111 — والفرقُ هو الجرحُ بعينه.
    """
    lo, hi, best = 1, len(lines), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        seen, found = set(), False
        for i in range(len(lines) - mid + 1):
            block = tuple(lines[i:i + mid])
            if block in seen:
                found = True
                break
            seen.add(block)
        if found:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    return best


def repeated_block(lines, length):
    """الكتلةُ الأولى التي تتكرّر بهذا الطول — تُعرَض بنصِّها لا بعددها."""
    seen = set()
    for i in range(len(lines) - length + 1):
        block = tuple(lines[i:i + length])
        if block in seen:
            return list(block)
        seen.add(block)
    return []


def lost_runs(parent, base, merge, floor):
    """كتلٌ متّصلةٌ أضافها أبٌ (ليست في الأساس) وغابت عن الدمجِ كلَّها."""
    base_set, merge_set = set(base), set(merge)
    runs, cur = [], []
    for line in parent:
        if line not in merge_set and line not in base_set:
            cur.append(line)
        else:
            if len(cur) > floor:
                runs.append(cur)
            cur = []
    if len(cur) > floor:
        runs.append(cur)
    return runs


def audit_file(path, base, p1, p2, merge):
    """يُصادِم ملفًّا واحدًا في المواضعِ الأربعةِ ويشتقُّ أصنافَه الثلاثة."""
    b, a1, a2, m = (significant(blob_lines(rev, path))
                    for rev in (base, p1, p2, merge))

    # السقفُ مقيسٌ من الأبوين والأساسِ معًا — فلا حدَّ يُختَلق
    floor = max(ceiling(b), ceiling(a1), ceiling(a2))
    top = ceiling(m)

    dup = repeated_block(m, top) if top > floor else []
    lost = lost_runs(a1, b, m, floor) + lost_runs(a2, b, m, floor)
    made = [ln for ln in set(m) - set(b) - set(a1) - set(a2)]

    return {"سقفُ_التكرارِ_في_الأبوين": floor, "سقفُه_في_الدمج": top,
            "كتلةٌ_تكرّرت_صامتةً": dup,
            "كتلٌ_سقطت_صامتةً": [len(r) for r in lost],
            "أولُ_ما_سقط": (lost[0][:4] if lost else []),
            "اختُلِقَ_في_الحلّ": sorted(made)}


def audit(commit="HEAD"):
    """التدقيقُ كلُّه — ويُعيد خريطةً معدودةً لا حكمًا مُدَّعًى."""
    parents = parents_of(commit)
    if len(parents) < 2:
        return {"إيداع": commit, "دمج": False,
                "الحكم": "ليس دمجًا — لا أبوين يُصادَم بهما"}

    p1, p2 = parents[0], parents[1]
    missing = [r for r in (p1, p2) if not have(r)]
    if missing:
        raise LookupError(
            "تاريخٌ ناقصٌ لا يُقاس عليه: أبٌ غائبٌ عن النسخة "
            + " · ".join(missing) + " — يُجلَب بـ«git fetch --deepen 50»")

    code, out, _ = git("merge-base", p1, p2)
    if code != 0:
        raise LookupError("لا أساسَ مشتركًا بين الأبوين — يُجلَب التاريخُ أوّلًا")
    base = out.strip()

    # لا يُدقَّق إلا ما مسَّه الطرفان: الملفُّ الذي تبدّل على جانبٍ واحدٍ يأخذه
    # git كاملًا بلا فضِّ تعارضٍ، فلا موضعَ فيه لهذا الصنفِ من العطب.
    touched = sorted(set(files_of(base, p1)) & set(files_of(base, p2)))

    files, lost, dup, made = {}, 0, 0, 0
    for path in touched:
        row = audit_file(path, base, p1, p2, commit)
        n_lost, n_dup = sum(row["كتلٌ_سقطت_صامتةً"]), len(row["كتلةٌ_تكرّرت_صامتةً"])
        if n_lost or n_dup or row["اختُلِقَ_في_الحلّ"]:
            files[path] = row
        lost += n_lost
        dup += n_dup
        made += len(row["اختُلِقَ_في_الحلّ"])

    return {
        "إيداع": commit, "دمج": True, "أساس": base, "أبوان": [p1, p2],
        "مقيس": {"ملفّاتٌ مسَّها الطرفان": len(touched),
                 "ملفّاتٌ فيها خبر": len(files),
                 "سطورٌ سقطت في كتلٍ متّصلة": lost,
                 "سطورُ الكتلةِ المكرّرة": dup,
                 "سطورٌ اختُلِقت في الحلّ": made},
        "ملفّات": files,
        "الحكم": ("سقوطٌ صامت" if lost else "تكرارٌ صامت" if dup else "نظيف"),
    }


def report(res):
    """يعرض المقيسَ سطرًا سطرًا — ولا يُطوى صنفٌ لأنّه صفر."""
    print("تدقيقُ الدمج — مصادمةُ الإيداعِ بأبويه وأساسِهما")
    print("=" * 78)
    if not res.get("دمج"):
        print(f"{res['إيداع']}: {res['الحكم']}")
        return 0

    m = res["مقيس"]
    print(f"الأساس {res['أساس'][:10]} · الأبوان "
          f"{res['أبوان'][0][:10]} ⟷ {res['أبوان'][1][:10]}")
    print(f"الميدان: {m['ملفّاتٌ مسَّها الطرفان']} ملفًّا مسَّها الطرفان معًا")
    for key in ("سطورٌ سقطت في كتلٍ متّصلة", "سطورُ الكتلةِ المكرّرة",
                "سطورٌ اختُلِقت في الحلّ"):
        print(f"  · {key}: {m[key]}")

    for path, row in res["ملفّات"].items():
        print(f"\n— {path}  (سقفُ التكرارِ في الأبوين "
              f"{row['سقفُ_التكرارِ_في_الأبوين']} ⟷ في الدمج {row['سقفُه_في_الدمج']})")
        if row["كتلةٌ_تكرّرت_صامتةً"]:
            blk = row["كتلةٌ_تكرّرت_صامتةً"]
            print(f"  ✗ كتلةٌ من {len(blk)} سطرًا تكرّرت — وسقفُ الأبوين دونَها:")
            for line in blk[:3]:
                print(f"      {line[:84]}")
        for n in row["كتلٌ_سقطت_صامتةً"][:4]:
            print(f"  ✗ كتلةٌ متّصلةٌ من {n} سطرًا أضافها أبٌ وغابت عن الدمج")
        for line in row["أولُ_ما_سقط"][:3]:
            print(f"      {line[:84]}")
        if row["اختُلِقَ_في_الحلّ"]:
            print(f"  · مُختلَقٌ في الحلّ: {len(row['اختُلِقَ_في_الحلّ'])} سطرًا")

    if m["سطورٌ اختُلِقت في الحلّ"]:
        print(f"\nالمُختلَقُ في الحلّ {m['سطورٌ اختُلِقت في الحلّ']} سطرًا — "
              "يُسمّى ولا يُسقِط: فضُّ التعارضِ قد يوجب سطرًا بحقّ، ولا يُطوى")

    if m["سطورٌ سقطت في كتلٍ متّصلة"]:
        print("\n::error::سقوطٌ صامت — أضافه أبٌ كتلةً متّصلةً والدمجُ أسقطها")
        return E_LOSS
    if m["سطورُ الكتلةِ المكرّرة"]:
        print("\n::error::تكرارٌ صامت — بلغَه الأبوان فأبقى الدمجُ النسختين")
        return E_DUP
    print("\nالحكم: نظيفٌ — لا كتلةَ سقطت ولا كتلةَ تكرّرت فوقَ سقفِ الأبوين ✓")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="مصادمةُ الدمجِ بأبويه وأساسِهما")
    ap.add_argument("commit", nargs="?", default="HEAD")
    ap.add_argument("--json", metavar="مسار")
    args = ap.parse_args(argv)

    try:
        res = audit(args.commit)
    except LookupError as exc:
        print(f"صريخ: {exc}", file=sys.stderr)
        return E_HISTORY

    code = report(res)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {args.json}")
    return code


if __name__ == "__main__":
    sys.exit(main())
