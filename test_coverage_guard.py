# test_coverage_guard.py — مصادمةُ رقعة حارس الموضع في induction/seals.py: coverage()
#
# العطبُ المرقوع: كان `coverage()` يجمع أسماءَ ملفّات JSON بمسحٍ مسطَّحٍ (os.walk)
# يُذيب المجلَّد — فوديعةٌ خرجت عن مجلَّدها المرصود، أو تكرّر اسمُها في مجلَّدٍ آخر،
# كانت تمرّ صامتةً ما دام الاسمُ **موجودًا في مكانٍ ما** من الشجرة. الرقعةُ تصادم
# الزوجَ (اسمٌ، مجلَّد) لا الاسمَ وحدَه، بمقارنة موضع كلِّ وديعةٍ الفعليّ بموضعها
# المُعلَن في DEPOSIT_DIR (عبر deposit_reldir).
#
# خمسُ حالاتٍ هنا: ٣ قبل (ما كان الحارسُ القديم يُغفله فيلتقطه الجديد) · ٠ بعد
# (الشجرةُ الحقيقيّةُ نظيفةٌ) · ناسيةُ الخريطة ١ (افتراضٌ صامتٌ مشروع، لا عطب) ·
# الوجهُ المقلوب ١ (موضعٌ مخالفٌ صريحًا) · ومحاولتا التكذيب القائمتان سليمتان.
#
# لا شبكةَ ولا مصدرَ مجلوبٌ هنا: كلُّ حالةٍ مصنوعةٌ بحقنة _found/_locations/_ci،
# ولا يُمَسُّ ملفٌّ حقيقيٌّ من الشجرة.
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "induction"))

import seals as S


def _gated():
    return set(S.GENERATORS) | set(S.CI_COLLIDED)


# ــ ٠ بعد: الشجرةُ الحقيقيّةُ (بلا حقنةٍ) نظيفةٌ من الوجه المقلوب ــــــــــــــ
def test_real_tree_has_zero_location_problems():
    problems = S.coverage(verbose=False)
    mismatches = [p for p in problems if "الوجهُ المقلوب" in p]
    assert mismatches == [], mismatches


# ــ ناسيةُ الخريطة ١: وديعةٌ بلا عنوانٍ صريح في DEPOSIT_DIR (تفترض HERE صمتًا) ــ
# `hiyad.json` (من GENERATORS) لم تُذكَر في DEPOSIT_DIR: الافتراضُ الصامتُ إلى
# induction/ مشروعٌ هنا لأنّ الملفّ فعلًا هناك — فلا يُعَدُّ هذا وجهًا مقلوبًا.
def test_forgotten_map_entry_defaults_without_problem():
    assert "hiyad.json" not in S.DEPOSIT_DIR
    assert S.deposit_reldir("hiyad.json") == "induction"
    found = _gated()
    locations = {dep: {S.deposit_reldir(dep)} for dep in found}
    problems = S.coverage(verbose=False, _found=found, _locations=locations, _ci=S.ci_text())
    assert not any("hiyad.json" in p for p in problems)


# ــ الوجهُ المقلوب ١: وديعةٌ مُعلَنةٌ في ROOT، والشجرةُ لا تحويها إلا في induction/ ــ
def test_inverted_face_location_mismatch_is_caught():
    dep = "alama_v0.json"
    assert S.deposit_reldir(dep) == "."          # مُعلَنةٌ في ROOT
    found = _gated()
    locations = {d: {S.deposit_reldir(d)} for d in found}
    locations[dep] = {"induction"}               # لكنّها فعليًّا في induction/ فقط
    problems = S.coverage(verbose=False, _found=found, _locations=locations, _ci=S.ci_text())
    hits = [p for p in problems if "الوجهُ المقلوب" in p and dep in p]
    assert len(hits) == 1, problems


# ــ ٣ قبل: ثلاثُ صورٍ كان الحارسُ القديم (بالاسم وحدَه) يُغفلها ــــــــــــــــ
def test_before_1_duplicate_name_wrong_dir_old_guard_blind():
    """وديعةٌ اسمُها في مجلَّدين معًا (المُعلَن + آخر): القديمُ يراها 'موجودة' فيمرّ،
    والجديدُ يفحص أنّ موضعَها المُعلَن من بين مواضعها — فلا يُخدَع بالتكرار وحدَه،
    لكنّه يُمسك الحالةَ لو غاب موضعُها المُعلَن عن مجموعة مواضعها الفعليّة."""
    dep = "dictionary_v0.json"
    expected = S.deposit_reldir(dep)
    found = _gated()
    locations = {d: {S.deposit_reldir(d)} for d in found}
    # الملفّ الحقيقيّ غاب عن موضعه المُعلَن، ووُجد فقط في مجلَّدٍ آخر مكرَّرًا
    locations[dep] = {"burhan", "induction"}
    assert expected not in locations[dep]
    problems = S.coverage(verbose=False, _found=found, _locations=locations, _ci=S.ci_text())
    assert any("الوجهُ المقلوب" in p and dep in p for p in problems), problems


def test_before_2_present_only_elsewhere_never_at_declared_root():
    """وديعةٌ جذريّةٌ (`waqf_v0.json`) غابت عن ROOT كلّيةً ووُجدت فقط في induction/:
    الحارسُ القديم (اسمٌ فقط) كان يراها مغطّاةً بمجرَّد وجود الاسم في الشجرة."""
    dep = "waqf_v0.json"
    assert S.deposit_reldir(dep) == "."
    found = _gated()
    locations = {d: {S.deposit_reldir(d)} for d in found}
    locations[dep] = {"induction"}
    problems = S.coverage(verbose=False, _found=found, _locations=locations, _ci=S.ci_text())
    assert any("الوجهُ المقلوب" in p and dep in p for p in problems), problems


def test_before_3_burhan_deposit_leaked_to_root():
    """وديعتا `burhan/` (`burhan_v0.json`) لو ظهرتا في ROOT بدل بيت البرهان: الاسمُ
    وحدَه لا يفضح خروجَ الشهادة عن بيتها المرصود — والموضعُ يفضح."""
    dep = "burhan_v0.json"
    assert S.deposit_reldir(dep) == "burhan"
    found = _gated()
    locations = {d: {S.deposit_reldir(d)} for d in found}
    locations[dep] = {"."}
    problems = S.coverage(verbose=False, _found=found, _locations=locations, _ci=S.ci_text())
    assert any("الوجهُ المقلوب" in p and dep in p for p in problems), problems


# ــ محاولتا التكذيب القائمتان في falsify() سليمتان بعد الرقعة ـــــــــــــــــ
def test_existing_falsify_orphan_and_ci_claim_still_pass():
    orphan = S.coverage(verbose=False,
                         _found=set(S.GENERATORS) | set(S.CI_COLLIDED) | {"يتيم_v0.json"},
                         _ci=S.ci_text())
    assert any("يتيم_v0.json" in p for p in orphan)

    claim = S.coverage(verbose=False, _found=set(S.GENERATORS) | set(S.CI_COLLIDED), _ci="")
    assert len(claim) >= len(S.CI_COLLIDED)


# ــ المُشغِّلُ عديمُ الاعتماد ــــــــــــــــــــــــــــــــــــــــــــــــــ
def run():
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    good = bad = 0
    for name, fn in tests:
        try:
            fn()
        except Exception as exc:                       # noqa: BLE001 — يُعرَض لا يُبتلَع
            bad += 1
            print(f"  ✗ {name}: {exc}", file=sys.stderr)
        else:
            good += 1
            print(f"  ✓ {name}")
    print(f"\nالمطابقُ {good} · المخالفُ {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
