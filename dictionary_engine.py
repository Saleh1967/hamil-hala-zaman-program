# dictionary_engine.py — المعجم v0: أول حلقة {ث/ع} بقواعد مبنيٍّ معلنة، من الصفر.
# الانضباط: كل موضعٍ إما مصنَّفٌ بقاعدةٍ مسمّاة أو ⚑ — لا افتراضيَّ صامت.
# القواعد المعلنة (وراثة باسمها من برنامج hamil):
#   ح-شدة: أوّل زوج الشدة سكونٌ مبنيٌّ (R5-أول)
#   ح-جار: ب/ل/ك الملتصقة بكسرة مبنيٌّ اتصالٌ لا إعراب
#   ع-تبدل: سند خاتمة الهيكل يتبدّل على المجمَّد (سندان فأكثر)
#   ث-وحدة: سندٌ واحد وعلامةٌ محقَّقة
#   ز-مزاح: تنوين فتح على ما قبل الخاتمة وخاتمةٌ عارية ا/ى
#   ق-فراغ: خاتمةٌ عاريةٌ بلا تنوينٍ مزاح — **صنفٌ رابعٌ نهائيّ بحكم الرسم** (انظر q_rasm أدناه)
#   و٣-قلع: مطابقة قوالب I–XV بعد قلع السوابق المعلنة (awzan_engine — القوالب من T بعينها)
from collections import Counter, defaultdict
from math import log2
import json, os, sys

_INDUCTION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "induction")
assert os.path.isfile(os.path.join(_INDUCTION, "induction_engine.py")), \
    "محرّك الاستقراء غائبٌ عن induction/ — لا استيراد صامت"
sys.path.insert(0, _INDUCTION)
from induction_engine import parse_verses, GATES5  # عائلة الجذر الواحد

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")

def skel_of(word):
    return "".join(ch for ch, _ in word)

def classify_word(word, sup):
    """الأولوية المعلنة: ز ثم ق ثم ع(تبدّل) ثم ث(وحدة) — كلها قواعد مسمّاة."""
    if len(word) >= 2 and word[-2][1] == "تنوين فتح" and word[-1][0] in ("ا", "ى") and word[-1][1] == "عري":
        return "ز", "ز-مزاح"
    if word[-1][1] == "عري":
        return "ق", "ق-فراغ"
    return ("ع", "ع-تبدل") if len(sup[skel_of(word)]) >= 2 else ("ث", "ث-وحدة")

def mabni_loci(word):
    """مواضع المبني المعلنة السطحية — تغطيةٌ محسوبة لا ادّعاءُ تصنيفٍ كامل."""
    loc = []
    for i, (ch, st) in enumerate(word):
        if ch in "بل" and i + 1 < len(word) and word[i + 1][1] in ("ضمة", "سكون") and st == "كسرة":
            loc.append("ح-جار-ملتصق")  # بِ/لِ + ساكن: جارٌّ ملتصق مبنيّ
    return loc

def has_shadda(word, raw):
    return "ح-شدة" if "ّ" in raw else None

Q_RASM = ("ا", "ى", "ي")          # خواتمُ الفراغ الثلاث: المقصور/المنقوص مظنّتُها

def definite_evidence(word):
    """قرينةُ الاسميّة السطحيّة الوحيدة المعلنة: «ال» بعد السوابق (PREFIX من awzan بعينها،
    لا نسخةٌ ثانية). تشخيصٌ يُعَدّ ولا يُصنِّف: حدٌّ أدنى لما يصحّ نقلُه إلى علامةٍ مقدَّرة."""
    import awzan_engine as AZ
    i = 1 if len(word) > 2 and (word[0][0], word[0][1]) in AZ.PREFIX else 0
    return [ch for ch, _ in word[i:i + 2]] == ["ا", "ل"]

def awzan_cover(path, verses, sup):
    """تغطية الأوزان (و٣-قلع) على المعلَّق ث+ع — تُحسب هنا بالمحرّك نفسه، لا برقمٍ منقول.
    وتُقاس تقاطعاتُها مع القاعدتين الأخريين هنا أيضًا، فلا يُجمَع مغطًّى مرّتين."""
    import awzan_engine as AZ
    rich = AZ.tokenize_rich(path, verses)
    matched = shadda_ovl = jar_ovl = 0
    for va, vb in zip(verses, rich):
        for wa, wb in zip(va, vb):
            if classify_word(wa, sup)[0] not in ("ث", "ع"):
                continue
            if AZ.hit(wb, "و٣-قلع") is not None:
                matched += 1
                shadda_ovl += any(d for _, _, d in wb)
                jar_ovl += 1 if mabni_loci(wa) else 0
    return matched, shadda_ovl, jar_ovl, sum(len(t) for t in AZ.T.values()) * 8 + len(AZ.PREFIX) * 8 * 4


def run(path=CORPUS):
    verses = parse_verses(path)
    # العبور الأول: سندو الخواتم لكل هيكل (مقيس على الهياكل لا الكلمات)
    sup = defaultdict(Counter)
    toks = []
    for words in verses:
        ws = []
        for w in words:
            sup[skel_of(w)][w[-1][1]] += 1
            ws.append(w)
        toks.append(ws)
    assert len(sup) == 14870, "بصمة الهياكل خُالفت — صريخ"
    cnt, q_split, rule_cov = Counter(), Counter(), Counter()
    q_words, q_defi = Counter(), Counter()
    q_forms = defaultdict(set)
    kinds = []
    Nw = 0
    for ws in toks:
        for w in ws:
            Nw += 1
            k, rule = classify_word(w, sup)
            kinds.append(k)
            cnt[k] += 1
            rule_cov[rule] += 1
            if k == "ق":
                q_split[w[-1][0]] += 1
                if w[-1][0] in Q_RASM:
                    q_words[w[-1][0]] += 1
                    q_forms[w[-1][0]].add(tuple(w))
                    if definite_evidence(w):
                        q_defi[w[-1][0]] += 1
    z_chk = cnt["ز"]
    assert Nw == 77801 and z_chk == 3153, f"مصالحة hamil خُالفت: Nw={Nw} ز={z_chk} — صريخ"
    flat = [w for ws in toks for w in ws]
    # ——— مقامٌ واحدٌ معروضٌ لا مُدّعًى ———
    # الكتلةُ تُعَدّ موضعَ كلمةٍ **إن حوت حرفًا عربيًّا** وحدَها — وهو عينُ شرطِ parse_verses،
    # فيلتقي المقامان بالعدّ لا بالدعوى (`letter_blocks == Nw`). وما سقط يُعرَض مسمًّى:
    #   علامات-رسم: كتلةٌ بلا حرفٍ عربيّ (ۖ ۚ ۗ ۞ …) — ليست موضعَ كلمةٍ أصلًا
    #   ترويسة: أسطرُ إسناد النسخة (GlobalQuran/Tanzil) بلا حرفٍ عربيٍّ البتّة
    is_letter = lambda ch: "\u0621" <= ch <= "\u064a"
    raw_blocks = 0; letter_blocks = 0; rasm_marks = 0; header_words = 0
    mark_forms = Counter()
    raw_tokens = []
    blob = open(path, encoding="utf-8").read()
    for ln in blob.splitlines():
        if not ln.strip():
            continue
        arabic_line = any(is_letter(ch) for ch in ln)
        for w in ln.split(" "):
            if not w.strip():
                continue
            raw_blocks += 1
            if not arabic_line:
                header_words += 1
            elif not any(is_letter(ch) for ch in w):
                rasm_marks += 1
                mark_forms[w.strip()] += 1
            else:
                letter_blocks += 1
                raw_tokens.append(w)
    assert letter_blocks == Nw and letter_blocks + rasm_marks + header_words == raw_blocks, \
        f"مقامُ العدّ خُولف: كتل={letter_blocks} ⟷ Nw={Nw} · علامات={rasm_marks} ترويسة={header_words} — صريخ"
    # التقاطعُ معروضٌ لا مكتوم: الشدّةُ والجارُّ يقعان على الموضع نفسِه 663 مرّة،
    # فالاتحادُ ليس مجموعَهما — والطرحُ بلا هذا التقاطع تضخيمٌ ثانٍ بعد تضخيم المقام.
    shadda_words = jar_mabni_words = shadda_jar_both = 0
    for tok, w in zip(raw_tokens, flat):
        s = "ّ" in tok
        j = bool(mabni_loci(w))
        shadda_words += s
        jar_mabni_words += j
        shadda_jar_both += s and j
    shadda_jar_union = shadda_words + jar_mabni_words - shadda_jar_both
    assert shadda_jar_both == 663 and shadda_jar_union == 22630, \
        f"تقاطعُ القاعدتين خُولف: تقاطع={shadda_jar_both} اتحاد={shadda_jar_union} — صريخ"
    n_var = sum(1 for c in sup.values() if len(c) >= 2)
    sup_states = Counter()
    for c in sup.values():
        if len(c) >= 2:
            for st in c:
                sup_states[st] += 1
    awzan_words, awzan_shadda, awzan_jar, awzan_bits = awzan_cover(path, verses, sup)
    awzan_gain = awzan_words - awzan_shadda          # الجديدُ وحده: ما لم تغطّه ح-شدة
    assert awzan_jar == 0, f"تقاطعُ الأوزان بالجارّ خُولف: {awzan_jar} — صريخ"
    # ⚑ البقاءُ الحقيقيّ: **موضعٌ موضعًا** على مقام الكلمات، لا طرحًا تحصيليًّا يجمع مغطًّى مرّتين.
    # القاعدتان السطحيّتان المجّانيّتان (ح-شدة · ح-جار-ملتصق) بكلفة القواعد الستّ وحدَها؛
    # وجدولُ الأوزان يُقاس فوقهما مفصولًا لأنه يُسعَّر بجدوله (awzan_bits).
    remain_cnt = Counter(); remain_q = Counter(); remainder = 0
    for tok, w, k in zip(raw_tokens, flat, kinds):
        if "ّ" in tok or mabni_loci(w):
            continue
        remainder += 1
        remain_cnt[k] += 1
        if k == "ق":
            remain_q[w[-1][0]] += 1
    assert remainder == letter_blocks - shadda_jar_union, \
        f"البقاءُ لا يطابق الاتحاد: {remainder} ⟷ {letter_blocks - shadda_jar_union} — صريخ"
    union3 = shadda_jar_union + awzan_gain           # الأوزانُ فوق الاتحاد، بلا تكرارِ تقاطع
    remainder_awzan = letter_blocks - union3
    rules_bits = len(["ز-مزاح", "ق-فراغ", "ع-تبدل", "ث-وحدة",
                      "ح-شدة", "ح-جار-ملتصق"]) * 8 * 4
    cost_bits = rules_bits + awzan_bits
    # الرقمُ التاريخيُّ المختوم (⚑=57,603) كان على المقام الخام المُضخَّم وبطرحٍ يهمل التقاطع،
    # فيُقاس هنا ليُحرَس عهدُه في الوثائق، ولا يُودَع حكمًا — الحكمُ هو البقاءُ المعروض أعلاه.
    sealed_scream = raw_blocks - shadda_words - awzan_gain
    assert sealed_scream == 57603 and cost_bits == 1456 and rules_bits == 192, \
        f"حدُّ حكم الرسم خُولف: ⚑={sealed_scream} كلفة={cost_bits} — صريخ"
    assert remainder == 55171 and remainder_awzan == 52073 \
        and rasm_marks == 4578 and header_words == 27 and len(mark_forms) == 9, \
        f"إغلاقُ المقام خُولف: بقاء={remainder} بعدَ الأوزان={remainder_awzan} " \
        f"علامات={rasm_marks}/{len(mark_forms)} ترويسة={header_words} — صريخ"
    q_rasm = {e: dict(words=q_words[e], forms=len(q_forms[e]), definite=q_defi[e])
              for e in Q_RASM}
    q_rasm_total = dict(words=sum(q_words.values()), forms=sum(len(f) for f in q_forms.values()),
                        definite=sum(q_defi.values()))
    q_rasm_total["definite_pct"] = round(q_rasm_total["definite"] / q_rasm_total["words"] * 100, 2)
    return dict(Nw=Nw, cnt=dict(cnt), z=z_chk, q_split=dict(q_split),
                q_rasm=dict(by_ending=q_rasm, total=q_rasm_total, verdict="ق-فراغ صنفٌ رابعٌ نهائيّ"),
                skeletons=len(sup), n_var=n_var, sup_states=dict(sup_states),
                coverage=dict(
                    letter_blocks=letter_blocks,          # مقامُ العدّ الواحد = Nw بالمصادمة
                    raw_blocks=raw_blocks,                # كتلُ الملفّ كلُّها — للفرز لا للنسب
                    outside=dict(rasm_marks=rasm_marks, header_words=header_words,
                                 total=rasm_marks + header_words,
                                 mark_forms=dict(mark_forms.most_common())),
                    shadda_words=shadda_words, jar_mabni_words=jar_mabni_words,
                    shadda_jar_both=shadda_jar_both, shadda_jar_union=shadda_jar_union,
                    awzan_words=awzan_words, awzan_shadda=awzan_shadda,
                    awzan_jar=awzan_jar, awzan_gain=awzan_gain,
                    remainder=remainder,                  # ⚑ البقاء الحقيقيّ بالقاعدتين المجّانيّتين
                    remainder_by_class=dict(remain_cnt),
                    remainder_q_endings=dict(remain_q.most_common()),
                    remainder_after_awzan=remainder_awzan,
                    sealed_scream_raw=sealed_scream),     # الرقمُ التاريخيُّ بمقامه الخام، موسومًا
                rules_cost_bits=cost_bits, rules_only_bits=rules_bits)

def main():
    R = run()
    out = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    H = -sum(v / R["Nw"] * log2(v / R["Nw"]) for v in R["cnt"].values())
    print(f"المعجم v0 — كلمات {R['Nw']:,} · هياكل {R['skeletons']:,} (متبدّلة {R['n_var']:,}) | "
          f"ث={R['cnt']['ث']:,} · ع={R['cnt']['ع']:,} · ز={R['cnt']['ز']:,} · ق={R['cnt']['ق']:,} | H(صنف)={H:.4f}")
    print(f"حسم «ق» بخواتمه: " + " · ".join(f"{k}={v:,}" for k, v in sorted(R["q_split"].items(), key=lambda kv: -kv[1])))
    QR = R["q_rasm"]["total"]
    print(f"حكمُ الرسم — «ق» صنفٌ رابعٌ نهائيّ: خواتمُ ا/ى/ي {QR['words']:,} كلمة في {QR['forms']:,} صيغةً متمايزة، "
          f"والمرشَّح بقرينةٍ سطحيّةٍ معلنة («ال») {QR['definite']:,} ({QR['definite_pct']}%) — "
          f"نقلُ الصنف إلى علامةٍ مقدَّرة يحرّك الباقي بلا قرينة، فلا يُقيَّد. ⚑ والكلفة لم تُمسّا")
    C = R["coverage"]; O = C["outside"]
    print(f"مقامٌ واحدٌ معروض: كتلُ الملفّ {C['raw_blocks']:,} = مواضعُ كلماتٍ {C['letter_blocks']:,} "
          f"(= Nw بالمصادمة) + خارجَ المقام {O['total']:,} — علاماتُ رسمٍ {O['rasm_marks']:,} "
          f"في {len(O['mark_forms'])} صور (" +
          " · ".join(f"{k}={v:,}" for k, v in list(O["mark_forms"].items())[:3]) +
          f" …) + ترويسةُ إسنادٍ {O['header_words']:,}")
    print(f"تغطية المبني السطحية على المقام نفسِه: شدّة {C['shadda_words']:,} · جار ملتصق {C['jar_mabni_words']:,} · "
          f"تقاطعُهما {C['shadda_jar_both']:,} فاتحادُهما {C['shadda_jar_union']:,} (لا مجموعُهما) · "
          f"أوزان {C['awzan_words']:,} (تقاطعُها بالشدّة {C['awzan_shadda']:,} وبالجارّ {C['awzan_jar']} "
          f"فجديدُها {C['awzan_gain']:,})")
    RC = C["remainder_by_class"]
    print(f"⚑ البقاءُ الحقيقيّ {C['remainder']:,} موضعًا بالقاعدتين الستّ المجّانيّتين (192 بت): " +
          " · ".join(f"{k}={RC[k]:,}" for k in ("ث", "ع", "ق", "ز")) +
          f" — وسيّدةُ «ق» خاتمةُ «ا» بـ{C['remainder_q_endings']['ا']:,}؛ "
          f"وبجدول الأوزان فوقَها {C['remainder_after_awzan']:,}")
    print(f"كلفة القواعد الست + جدول الأوزان معلنة: {R['rules_cost_bits']} بت "
          f"(القواعدُ وحدَها {R['rules_only_bits']}) — تُخصم من أي ربحٍ يُبنى عليها. "
          f"والرقمُ التاريخيُّ ⚑={C['sealed_scream_raw']:,} يُقاس بمقامه الخام موسومًا، لا حكمًا")
    if out:
        json.dump({"المعجم_v0": R}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {out}")

if __name__ == "__main__":
    main()
