# rukhsa/cert_jabr.py — شهادةُ الجبر: أحكامُ الرخصة ثلاثةٌ لا اثنان، والبرهانُ بالاستقصاء.
#
# العطبُ الذي تقتله هذه الشهادة: «لم يُفحَص» تُقرَأ مرّةً «ممنوع» ومرّةً «مباح»، فيُبنى
# على الجهل حكمٌ في أحد الاتجاهين. فالحاملُ ههنا ثلاثيٌّ معلن:
#
#     ⊥ مُثبَتُ المنع   <   ⊘ محجورٌ (لم يُقَس)   <   ⊤ مُثبَتُ الإذن
#
# والعملُ على الحزمة ⊗ = أصغرُ الرتب (إعادةُ نشر مجموعٍ لا تُباح إلا إن أُبيح كلُّ جزء)،
# و⊕ = أكبرُها. ولا جدولَ يُكتَب بيدٍ: الجدولان مشتقّان من الترتيب المُعلَن وحدَه.
#
# وكلُّ ما يُدَّعى ههنا **مُستقصًى** لا مُستنبَطٌ بمثال: 3² زوجًا و3³ ثلاثيّةً تُمشَّط كلُّها،
# والاستكمالاتُ (كلُّ تأويلٍ ممكنٍ للمحجور) تُعَدُّ واحدةً واحدة. فالبرهانُ عَدٌّ لا بلاغة.
#
# المنهجُ الذي تُحاكَم به (بنودُ `burhan/THE-PROOF.md` السبعة):
#   ① الأساسُ يُعلَن قبل العدد — وهو ههنا **صوريٌّ محض**: لا شجرةَ ولا بايتاتِ مصدر.
#   ② المتوقَّعُ يُسجَّل قبل التشغيل — في `EXPECTED` أدناه، في بايتات الشهادة نفسِها.
#   ③ القيدُ الساقطُ يُثبَّت بعدده.    ④ ما لم يُعلَن متوقَّعُه يبقى معلَّقًا.
#   ⑤ كلُّ حارسٍ يَعُدُّ غيرَ الصفر في صورةٍ مكذِّبة — ومحاولاتُ التكذيب أدناه.
#   ⑥ القيدُ يُحَلّ ولا يُختار.        ⑦ العطبُ يُقاس مداه.
import argparse, itertools, json, sys

# الحاملُ الثلاثيُّ ورتبُه — تعدادٌ لا عدد، والجداولُ تُشتقُّ منه.
BOT = "⊥"
SUS = "⊘"
TOP = "⊤"
ORDER = [BOT, SUS, TOP]                 # الرتبةُ موضعٌ في هذا التعداد

# المتوقَّعُ قبل التشغيل — كلُّ عددٍ ههنا مُشتَقٌّ بالعدّ أدناه، فمخالفتُه مأخذ.
EXPECTED = {
    "أزواج": 9,                          # 3²
    "ثلاثيّات": 27,                       # 3³
    "شواهدُ_قانونِ_الحجر": 7,              # ثلاثيّاتُ {⊤,⊘} التي فيها ⊘ واحدٌ فأكثر: 2³−1
    "ثلاثيّاتٌ_يُبدِّلها_طيُّ_الحجر": 7,     # حيثُ ⊘ فولًا — وهي بعينها السبع
    "استكمالات": 64,                      # Σ على 3³ من 2^(عدد ⊘) = 4³
    "استكمالاتٌ_تُكذِّبُ_المتحفِّظ": 0,
    "استكمالاتٌ_تُكذِّبُ_المتفائل": 19,     # 3³ استكمالًا لشعاعاتِ {⊤,⊘} ناقصَ 2³ سليمة
}

# ③ قيدٌ سقط، يُثبَّت بعدده ولا يُطوى: سُجِّل متوقَّعُ «استكمالاتٌ تُكذِّبُ المتفائل»
# أوّلَ مرّةٍ **37** (= 64 − 27)، فكذّبه التشغيلُ بـ**19**. وعلّةُ السقوط مسمّاةٌ لا
# مُجمَلة: الـ37 عدَّت استكمالاتِ شعاعاتٍ فيها ⊥، والسياسةُ المتفائلةُ **لا تعمل**
# على تلك أصلًا فلا تُكذَّب بها. والعدُّ الصحيحُ على شعاعات {⊤,⊘} وحدَها:
# 3³ استكمالًا، منها 2³ يرفع كلَّ محجورٍ إلى إذن — فالباقي 19.
DROPPED = {"البند": "استكمالاتٌ_تُكذِّبُ_المتفائل", "المسجَّلُ_أوّلًا": 37, "المقيس": 19,
           "العلّة": "الـ37 عدَّت شعاعاتٍ فيها ⊥ لا تعمل عليها السياسةُ المتفائلةُ أصلًا"}


def rank(v):
    """رتبةُ الحكم — موضعُه في التعداد المُعلَن، لا رقمٌ مكتوبٌ بيدٍ ثانية."""
    return ORDER.index(v)


def meet(a, b):
    """⊗ الحزمة: أصغرُ الرتبتين — فجزءٌ ممنوعٌ يمنع الحزمة، ومحجورٌ يحجرها."""
    return a if rank(a) <= rank(b) else b


def join(a, b):
    return a if rank(a) >= rank(b) else b


def fold(vector, op=meet, unit=TOP):
    out = unit
    for v in vector:
        out = op(out, v)
    return out


def acts(verdict):
    """العملُ المتحفِّظ: لا يُعاد النشرُ إلا على إذنٍ **مُثبَت** — فالمحجورُ لا يُفتي."""
    return verdict == TOP


def acts_optimistic(verdict):
    """سياسةٌ مضادّةٌ تُعرَض لتُكذَّب: «ما لم يُمنَع صراحةً فهو مباح»."""
    return verdict != BOT


def completions(vector):
    """كلُّ تأويلٍ ممكنٍ للمحجور: ⊘ ⟶ ⊤ أو ⊥، والمُثبَتُ لا يتبدّل."""
    choices = [[v] if v != SUS else [TOP, BOT] for v in vector]
    return list(itertools.product(*choices))


def laws(triples, pairs):
    """أحكامُ الشبكة — مُستقصاةً لا مُستنبَطةً بمثال. القيمةُ عددُ المخالفات (صفرٌ = قام)."""
    return {
        "إبدالُ_⊗": sum(meet(a, b) != meet(b, a) for a, b in pairs),
        "إبدالُ_⊕": sum(join(a, b) != join(b, a) for a, b in pairs),
        "تجميعُ_⊗": sum(meet(meet(a, b), c) != meet(a, meet(b, c)) for a, b, c in triples),
        "تجميعُ_⊕": sum(join(join(a, b), c) != join(a, join(b, c)) for a, b, c in triples),
        "تماثلُ_⊗": sum(meet(a, a) != a for a in ORDER),
        "امتصاصٌ_⊗⊕": sum(meet(a, join(a, b)) != a for a, b in pairs),
        "محايدُ_⊗_هو_⊤": sum(meet(a, TOP) != a for a in ORDER),
        "ماحي_⊗_هو_⊥": sum(meet(a, BOT) != BOT for a in ORDER),
        "توزيعُ_⊗_على_⊕": sum(
            meet(a, join(b, c)) != join(meet(a, b), meet(a, c)) for a, b, c in triples),
    }


def quarantine_law(triples):
    """قانونُ الحجر: ما خلا من ⊥ وفيه ⊘ فحزمتُه ⊘ — لا ⊤ ولا ⊥.

    وهو قولُ `CONTRIBUTING.md` §١ في المحجور T₃ بعينه: **لا يُعَدُّ لنا ولا علينا**.
    والشواهدُ تُعَدّ (البندُ ⑤): حارسٌ بلا شاهدٍ حارسٌ بلا مادّة.
    """
    witnesses, breaks = 0, 0
    for t in triples:
        if BOT in t and SUS in t:
            # ⊥ أقوى: الحزمةُ ممنوعةٌ ولو حضر المحجور — وهذا فرعٌ آخر، لا شاهدَ ههنا.
            if fold(t) != BOT:
                breaks += 1
            continue
        if SUS not in t:
            continue
        witnesses += 1
        if fold(t) != SUS:
            breaks += 1
    return witnesses, breaks


def collapse_law(triples):
    """طيُّ الحجر إلى منع (⊘ ⟶ ⊥): يُبدِّل **الدعوى** ولا يُبدِّل **العمل**.

    فالمتحفِّظُ يعمل عملَ من يمنع، ولا يقول قولَه — وهذا فرقٌ مقيسٌ لا بلاغة:
    عددُ الثلاثيّات التي تتبدّل دعواها غيرُ صفر، وعددُ ما يتبدّل عملُه صفر.
    """
    claim_changed = act_changed = 0
    for t in triples:
        folded = fold(t)
        collapsed = fold(tuple(BOT if v == SUS else v for v in t))
        claim_changed += folded != collapsed
        act_changed += acts(folded) != acts(collapsed)
    return claim_changed, act_changed


def stability(triples):
    """ثباتُ العمل تحت كلِّ استكمال — جوابُ «المضيفُ محجوب» مقيسًا لا مرجوًّا.

    لكلِّ شعاعِ أحكامٍ ولكلِّ تأويلٍ ممكنٍ لمحجوراته: هل يبقى ما عُمِل به مأذونًا؟
    المتحفِّظُ (⊤ وحدَه) لا يُكذَّب في استكمالٍ واحد؛ والمتفائلُ يُكذَّب بعددٍ يُعَدّ.
    فحجرُ مرايا Zenodo لا يُنقِص إذنًا ولا يَمنح واحدًا: العملُ هو هو في التأويلين.
    """
    total = conservative = optimistic = 0
    for t in triples:
        folded = fold(t)
        for completion in completions(t):
            total += 1
            settled = fold(completion)
            if acts(folded) and settled != TOP:
                conservative += 1
            if acts_optimistic(folded) and settled != TOP:
                optimistic += 1
    return total, conservative, optimistic


# ═══ محاولاتُ التكذيب — كلُّ حارسٍ يُبتلى بصورةٍ تكذبه، ويجب أن يَعُدَّ غيرَ الصفر ═══
def _trial_quarantine(triples):
    """لو صار ⊘⊗⊘ = ⊤ لانقلب الحجرُ إفتاءً — فكم ثلاثيّةً يكسرها ذلك؟"""
    broken = 0
    for t in triples:
        if BOT in t or SUS not in t:
            continue
        folded = TOP if set(t) <= {TOP, SUS} else fold(t)   # الجدولُ المحرَّف
        if folded != SUS:
            broken += 1
    return broken


def _trial_optimistic(triples):
    """ولو عُمِل بالسياسة المتفائلة لَكُذِّبت باستكمالاتٍ تُعَدّ."""
    return stability(triples)[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    pairs = list(itertools.product(ORDER, repeat=2))
    triples = list(itertools.product(ORDER, repeat=3))
    fails = []

    if len(ORDER) != 3 or len(set(ORDER)) != 3:
        fails.append("الحاملُ ليس ثلاثيًّا — الشهادةُ بلا موضوع")

    law_breaks = laws(triples, pairs)
    for name, broken in law_breaks.items():
        if broken:
            fails.append(f"حكمُ «{name}» سقط في {broken} صورةً")

    witnesses, breaks = quarantine_law(triples)
    if breaks:
        fails.append(f"قانونُ الحجر سقط في {breaks} ثلاثيّة")
    claim_changed, act_changed = collapse_law(triples)
    if act_changed:
        fails.append(f"طيُّ الحجر بدّل العملَ في {act_changed} ثلاثيّة — التحفُّظُ ليس منعًا")
    if not claim_changed:
        fails.append("طيُّ الحجر لم يُبدِّل دعوًى واحدة — فالحجرُ والمنعُ سواءٌ، وهذا باطل")

    total, conservative, optimistic = stability(triples)
    if conservative:
        fails.append(f"العملُ المتحفِّظُ كُذِّب في {conservative} استكمالًا")
    if not optimistic:
        fails.append("السياسةُ المتفائلةُ لم تُكذَّب — الحارسُ بلا مادّة")

    # ⑤ الحرّاسُ يُبتلَون: صورةٌ مكذِّبةٌ يجب أن تُعَدَّ فيها المخالفاتُ غيرَ صفر.
    trials = {
        "جدولٌ يجعل ⊘⊗⊘ إذنًا": _trial_quarantine(triples),
        "سياسةٌ تعمل على المحجور": _trial_optimistic(triples),
    }
    for name, counted in trials.items():
        if not counted:
            fails.append(f"المحاولة «{name}» لم تُعَدَّ لها مخالفة — حارسٌ أعمى")

    measured = {
        "أزواج": len(pairs),
        "ثلاثيّات": len(triples),
        "شواهدُ_قانونِ_الحجر": witnesses,
        "ثلاثيّاتٌ_يُبدِّلها_طيُّ_الحجر": claim_changed,
        "استكمالات": total,
        "استكمالاتٌ_تُكذِّبُ_المتحفِّظ": conservative,
        "استكمالاتٌ_تُكذِّبُ_المتفائل": optimistic,
    }
    for name, want in EXPECTED.items():
        if measured[name] != want:
            fails.append(f"المتوقَّعُ المسجَّلُ «{name}» = {want} والمقيسُ {measured[name]}")

    out = {
        "الشهادة": "CERT-JABR",
        "الأساس": "صوريٌّ محض — لا شجرةَ ولا بايتاتِ مصدر",
        "الحامل": ORDER,
        "القانون": "⊗ = أصغرُ الرتبتين · ⊕ = أكبرُهما — مشتقّان من الترتيب لا مكتوبَين",
        "أحكامٌ_مُستقصاةٌ_بلا_مخالفة": sorted(law_breaks),
        "مقيس": measured,
        "متوقَّعٌ_قبل_التشغيل": EXPECTED,
        "قيدٌ_سقط_فثُبِّت_بعدده": DROPPED,
        "محاولاتُ_التكذيب": trials,
        "حكم": "خضراء" if not fails else "ساقطة",
        "مآخذ": fails,
    }

    print("— CERT-JABR: جبرُ الأحكام الثلاثة —")
    print(f"    {len(law_breaks)} حكمًا مُستقصًى على {len(triples)} ثلاثيّةً · "
          f"لا مخالفةَ في واحدٍ منها")
    print(f"    قانونُ الحجر: {witnesses} شاهدًا · {breaks} مخالفة · "
          f"طيُّ الحجر يُبدِّل {claim_changed} دعوًى و{act_changed} عملًا")
    print(f"    الاستكمالات: {total} · تُكذِّبُ المتحفِّظ {conservative} · "
          f"وتُكذِّبُ المتفائل {optimistic}")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ المحجورُ لا يُفتي ولا يُعَدُّ علينا — والعملُ ثابتٌ تحت كلِّ تأويل"
          if not fails else "    ✗ سقطت")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
