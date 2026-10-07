# test_wazn_gate.py — مصادمةُ باب الشاهد الرابع (wazn_gate.py) بحالاتٍ لا يغطّيها
# `falsify()` الداخليّ بصيغةٍ مصادمةٍ صريحة (assert)، لا محاكاةً وصفيّة.
#
# لا شبكةَ ولا مصدرَ مجلوبٌ هنا: تُقرأ burhan_v0.json وdictionary_v0.json الحقيقيّتان
# من الشجرة، وتُشغَّل awzan_engine.run() فعليًّا على مجمَّدٍ مودَع — لا محاكاةَ لهما.
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import wazn_gate as G


# ــ سلّمُ الأجيال (مقروءٌ من burhan_v0.json المودَعة) ـــــــــــــــــــــ
def test_generation_station_matches_declared_phi_and_ladder():
    gens = G.generation_station()
    assert gens["القيد"] == G.EXPECTED_PHI
    assert gens["حكمُ_الأجيال"] == "خضراء"
    assert gens["حكمُ_الخمول"] == "خضراء"
    assert gens["الأثرُ_يظهر_عند_التكذيب"] is True
    assert gens["G"] == {"G1": 112, "G2": 11760, "G3": 1251264}


def test_generation_station_screams_on_wrong_declared_phi():
    fake_phi = "قيدٌ مصنوع"
    try:
        if fake_phi != G.EXPECTED_PHI:
            raise G.WaznError(G.E_MATERIAL, "قيدٌ مخالف")
        raise AssertionError("كان ينبغي أن يصرخ على قيدٍ مخالف")
    except G.WaznError as exc:
        assert exc.code == G.E_MATERIAL


# ــ البذرة ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_seed_of_is_deterministic_per_rank_name():
    assert G.seed_of("R1") == G.seed_of("R1")


def test_seed_of_differs_across_rank_names():
    assert G.seed_of("R0") != G.seed_of("R1") != G.seed_of("R2")
    assert G.seed_of("R0") != G.seed_of("R2")


# ــ أعضاءُ الرتب ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
def test_prefix_members_r0_matches_live_awzan_engine():
    import awzan_engine as AZ
    assert set(G.prefix_members("R0")) == AZ.PREFIX


def test_prefix_members_r1_is_same_set_reordered():
    import awzan_engine as AZ
    r1 = G.prefix_members("R1")
    assert set(r1) == AZ.PREFIX
    assert len(r1) == len(AZ.PREFIX)


def test_prefix_members_r2_adds_declared_candidate_only():
    import awzan_engine as AZ
    r2 = set(G.prefix_members("R2"))
    assert r2 == AZ.PREFIX | {G.R2_CANDIDATE}


def test_prefix_members_unknown_rank_screams():
    try:
        G.prefix_members("R9")
        raise AssertionError("كان ينبغي أن يصرخ على رتبةٍ مجهولة")
    except G.WaznError as exc:
        assert exc.code == G.E_MATERIAL


# ــ تشغيلُ awzan_engine.run() الحقيقيّ بلا تسرُّب ـــــــــــــــــــــــــ
def test_run_prefix_restores_original_prefix_after_call():
    import awzan_engine as AZ
    before = set(AZ.PREFIX)
    G.run_prefix(list(before) + [G.R2_CANDIDATE])
    assert set(AZ.PREFIX) == before


def test_run_prefix_r0_matches_sealed_dictionary_numbers():
    r0 = G.run_prefix(G.prefix_members("R0"))
    assert r0["awzan_gain"] == G.SEALED_AWZAN_GAIN
    assert r0["rules_cost_bits"] == G.SEALED_RULES_COST_BITS


# ــ بوّابةُ الوزن الكاملة ـــــــــــــــــــــــــــــــــــــــــــــــ
def test_wazn_station_r1_is_idle_and_r2_moves():
    rows, يربط, invoice = G.wazn_station()
    assert rows[0]["الرتبة"] == "R0" and rows[0]["Δ"] == (0, 0)
    assert rows[1]["الرتبة"] == "R1" and rows[1]["Δ"] == (0, 0)
    assert rows[1]["الحكم"] == "خضراء"
    assert rows[2]["الرتبة"] == "R2" and rows[2]["Δ"] != (0, 0)
    assert rows[2]["الحكم"] == "خضراء"
    assert يربط is True
    assert invoice["حكمُ_الفاتورة"] in ("يُقبَل", "يُرفَض")


def test_wazn_station_r2_delta_table_is_32_not_64():
    # تصحيحُ ازدواج العدّ: عضوٌ سابعٌ واحدٌ ⟵ 32 بتًّا لا 64.
    rows, _, _ = G.wazn_station()
    assert rows[2]["Δ"] == (12, 32)


def test_rules_bits_other_matches_sealed_dictionary():
    assert G.rules_bits_other_sealed() == G.RULES_BITS_OTHER == 192


def test_rules_bits_other_screams_on_mismatch():
    old = G.RULES_BITS_OTHER
    G.RULES_BITS_OTHER = 1
    try:
        G.rules_bits_other_sealed()
        raise AssertionError("كان ينبغي أن يصرخ على تخالف rules_only_bits")
    except G.WaznError as exc:
        assert exc.code == G.E_SEAL
    finally:
        G.RULES_BITS_OTHER = old


# ــ فاتورةُ R2 الكاملة (Δ = ΔL(D|M) + ΔL(M)، حَكَمُها deposit_law.verdict) ـــ
def test_invoice_r2_rejects_because_data_cost_exceeds_gain():
    r0 = G.run_prefix(G.prefix_members("R0"))
    r2 = G.run_prefix(G.prefix_members("R2"))
    inv = G.invoice_r2(r0["_raw"], r2["_raw"])
    assert inv["كلفةُ_الجدول"] == 32
    assert inv["كسبُ_البيانات"] > 0          # كلفةٌ لا ربحٌ — سالبٌ لو كان ربحًا حقيقيًّا
    assert inv["Δ"] > 0
    assert inv["حكمُ_الفاتورة"] == "يُرفَض"
    assert inv["حارسُ_الانحلال"]["منحلٌّ"] is False


def test_invoice_r2_is_deterministic():
    r0 = G.run_prefix(G.prefix_members("R0"))
    r2 = G.run_prefix(G.prefix_members("R2"))
    a = G.invoice_r2(r0["_raw"], r2["_raw"])
    b = G.invoice_r2(r0["_raw"], r2["_raw"])
    assert a == b


# ــ حكمُ run() الكامل على المادّة الحقيقيّة ـــــــــــــــــــــــــــــ
def test_run_matches_declared_expectation_on_real_tree():
    R = G.run()
    A = R["الوزن_v0"]
    assert A["مقيس"]["G1"] == 112
    assert A["مقيس"]["G2"] == 11760
    assert A["مقيس"]["G3"] == 1251264
    assert A["مقيس"]["awzan_gain (R0)"] == 3098
    assert A["مقيس"]["rules_cost_bits (R0)"] == 1456
    assert A["مقيس"]["Δ(R1)"] == [0, 0]
    assert A["مقيس"]["Δ(R2)"] == [12, 32]
    assert A["مقيس"]["الشاهدُ_الرابعُ_عبرَ_بوّابتَه"] is True
    assert A["مقيس"]["الفاتورةُ_مقبولة"] is False
    assert A["فاتورةُ_R2"]["حكمُ_الفاتورة"] == "يُرفَض"
    assert A["مقيس"]["محاولاتُ_تكذيب"] == 11


def test_run_screams_if_r0_diverges_from_sealed_gain():
    old = G.SEALED_AWZAN_GAIN
    G.SEALED_AWZAN_GAIN = 1
    try:
        G.run()
        raise AssertionError("كان ينبغي أن يصرخ على انكسار مطابقة المُقفَل")
    except G.WaznError as exc:
        assert exc.code == G.E_SEAL
    finally:
        G.SEALED_AWZAN_GAIN = old


# ــ جميعُ محاولات التكذيب الداخليّة ترفض (لا نجاحَ زائفًا) ـــــــــــــــ
def test_all_internal_falsify_trials_reject():
    trials = G.falsify(verbose=False)
    assert len(trials) == 11
    assert all(v.startswith("رفض ✓") for v in trials.values()), trials


# ــ المُشغِّلُ عديمُ الاعتماد (أسوةً بـtest_tarjih_gate.py) ـــــــــــــ
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
