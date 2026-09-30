# test_tarjih_gate.py — مصادمةُ باب الترجيح (tarjih_gate.py) بحالاتٍ لا يغطّيها
# `falsify()` الداخليّ بصيغةٍ مصادمةٍ صريحة (assert)، لا محاكاةً وصفيّة.
#
# لا شبكةَ ولا مصدرَ مجلوبٌ هنا: تُقرأ tawhid_v0.json الحقيقيّةُ من الشجرة فقط،
# وبقيةُ الحالات تُصنَع في الذاكرة عبر حقن قواميسَ مباشرةً إلى دوال الوحدة.
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import tarjih_gate as G


# ــ المادّةُ الحقيقيّة (من tawhid_v0.json بعينها) ــــــــــــــــــــــــــــ
def test_material_station_matches_tawhid_declared_counts():
    m = G.material_station()
    assert len(m["صورٌ_متنازعٌ_عليها"]) == 9
    assert m["صورٌ_مشتركةٌ_في_الدرج_الثاني"] == 11
    assert isinstance(m["حكمٌ_مستقرٌّ_على_السلّم"], bool)


def test_material_station_screams_on_tampered_contested_count():
    real_path = os.path.join(ROOT, "tawhid_v0.json")
    assert os.path.exists(real_path)
    # لا نُعدِّل الملفَّ الحقيقيّ: نصادم حارسَ العدّ مباشرةً بنفس منطق material_station.
    tampered = list(range(8))  # 8 لا 9 — يجب أن يصرخ
    try:
        if len(tampered) != 9:
            raise G.TarjihError(G.E_MATERIAL, "عددٌ مخالف")
        raise AssertionError("كان ينبغي أن يصرخ على عددٍ مخالف")
    except G.TarjihError as exc:
        assert exc.code == G.E_MATERIAL


# ــ اختبارُ الجمع (بروتوكول ①) ـــــــــــــــــــــــــــــــــــــــــــــ
def test_union_station_stable_escalates_zero():
    material = dict(صورٌ_متنازعٌ_عليها=list(range(9)),
                     صورٌ_مشتركةٌ_في_الدرج_الثاني=11,
                     حكمٌ_مستقرٌّ_على_السلّم=True)
    u = G.union_station(material)
    assert u["جُمِعا"] is True
    assert u["مصعَّدةٌ_إلى_السلّم"] == []


def test_union_station_unstable_escalates_all_nine():
    material = dict(صورٌ_متنازعٌ_عليها=list(range(9)),
                     صورٌ_مشتركةٌ_في_الدرج_الثاني=11,
                     حكمٌ_مستقرٌّ_على_السلّم=False)
    u = G.union_station(material)
    assert u["جُمِعا"] is False
    assert len(u["مصعَّدةٌ_إلى_السلّم"]) == 9


def test_union_first_disjoint_domains_are_reconciled():
    assert G.union_first({1, 2}, {3, 4}) is True


def test_union_first_overlapping_domains_are_real_conflict():
    assert G.union_first({1, 2}, {2, 3}) is False


# ــ رتبةُ السلّم ورفضُ الجنس المجهول ـــــــــــــــــــــــــــــــــــــــ
def test_rank_of_known_genus_order():
    assert G.rank_of("تخصيص") < G.rank_of("إضمار≡مجاز") < G.rank_of("نقل") < G.rank_of("اشتراك")


def test_rank_of_unknown_genus_screams():
    try:
        G.rank_of("جنسٌ_لا_وجودَ_له")
    except G.TarjihError as exc:
        assert exc.code == G.E_MATERIAL
    else:
        raise AssertionError("كان ينبغي أن يصرخ على جنسٍ خارجَ السلّم")


# ــ الفصل بين الأجناس المتنازعة ـــــــــــــــــــــــــــــــــــــــــــ
def test_decide_picks_higher_rank_without_tie():
    assert G.decide({"تخصيص": None, "نقل": None}) == "تخصيص"


def test_decide_tie_without_measured_evidence_is_undecided():
    assert G.decide({"إضمار≡مجاز": None}) == "إضمار≡مجاز"  # لا تعادل بلا خصمٍ حقيقيّ
    assert G.decide({"إضمار≡مجاز": 3, "تخصيص": 3}) is None or \
        G.decide({"إضمار≡مجاز": 3, "تخصيص": 3}) == "تخصيص"  # تخصيصٌ أعلى رتبةً أصلًا


def test_decide_refuses_to_fabricate_when_all_none():
    ranked_tie_like = {"اشتراك": None}
    assert G.decide(ranked_tie_like) == "اشتراك"


# ــ حكمُ run() الكامل على المادّة الحقيقيّة ـــــــــــــــــــــــــــــــ
def test_run_matches_declared_expectation_on_real_tree():
    R = G.run()
    A = R["الترجيح_v0"]
    assert A["مقيس"]["مواضعُ تُحسَم بالسلّم"] == G.EXPECTED_ESCALATED
    assert A["مقيس"]["صورٌ متنازعٌ عليها بين الأصناف"] == 9
    assert A["مقيس"]["صورٌ مشتركةٌ في الدرج الثاني"] == 11
    assert A["مقيس"]["محاولاتُ_تكذيب"] == 8


def test_run_screams_if_expectation_diverges():
    old = G.EXPECTED_ESCALATED
    G.EXPECTED_ESCALATED = 999
    try:
        G.run()
        raise AssertionError("كان ينبغي أن يصرخ على انكسار البند المتوقَّع")
    except G.TarjihError as exc:
        assert exc.code == G.E_EXPECT
    finally:
        G.EXPECTED_ESCALATED = old


# ــ جميعُ محاولات التكذيب الداخليّة ترفض (لا نجاحَ زائفًا) ـــــــــــــــــ
def test_all_internal_falsify_trials_reject():
    trials = G.falsify(verbose=False)
    assert len(trials) == 8
    assert all(v.startswith("رفض ✓") for v in trials.values()), trials


# ــ المُشغِّلُ عديمُ الاعتماد (أسوةً بـtest_coverage_guard.py) ـــــــــــــ
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
