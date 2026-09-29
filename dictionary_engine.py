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
    """تغطية الأوزان (و٣-قلع) على المعلَّق ث+ع — تُحسب هنا بالمحرّك نفسه، لا برقمٍ منقول."""
    import awzan_engine as AZ
    rich = AZ.tokenize_rich(path, verses)
    matched = shadda_ovl = 0
    for va, vb in zip(verses, rich):
        for wa, wb in zip(va, vb):
            if classify_word(wa, sup)[0] not in ("ث", "ع"):
                continue
            if AZ.hit(wb, "و٣-قلع") is not None:
                matched += 1
                shadda_ovl += any(d for _, _, d in wb)
    return matched, shadda_ovl, sum(len(t) for t in AZ.T.values()) * 8 + len(AZ.PREFIX) * 8 * 4


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
    mabni_words = 0
    Nw = 0
    for ws in toks:
        for w in ws:
            Nw += 1
            k, rule = classify_word(w, sup)
            cnt[k] += 1
            rule_cov[rule] += 1
            if k == "ق":
                q_split[w[-1][0]] += 1
                if w[-1][0] in Q_RASM:
                    q_words[w[-1][0]] += 1
                    q_forms[w[-1][0]].add(tuple(w))
                    if definite_evidence(w):
                        q_defi[w[-1][0]] += 1
            if mabni_loci(w):
                mabni_words += 1
    z_chk = cnt["ز"]
    assert Nw == 77801 and z_chk == 3153, f"مصالحة hamil خُالفت: Nw={Nw} ز={z_chk} — صريخ"
    # تغطية القواعد المعلنة: الشدة في النص الخام (لا توسيع R5 هنا — هذا v0 السطحي).
    # والفرقُ بين المقام الخام والمفكوك مصنَّفٌ هنا صنفين لا رقمًا مبهمًا:
    #   علامات-رسم: كتلةٌ بلا حرفٍ عربيّ (ۖ ۚ ۗ ۞ …) — تسقطها parse_verses لأنها ليست موضعَ كلمة
    #   ترويسة: أسطرُ إسناد النسخة (GlobalQuran/Tanzil) بلا حرفٍ عربيٍّ البتّة
    raw_words = 0; shadda_words = 0
    word_positions = 0; rasm_marks = 0; header_words = 0
    blob = open(path, encoding="utf-8").read()
    for ln in blob.splitlines():
        if not ln.strip():
            continue
        arabic_line = any("\u0621" <= ch <= "\u064a" for ch in ln)
        for w in ln.split(" "):
            if not w.strip():
                continue
            raw_words += 1
            if not arabic_line:
                header_words += 1
            elif not any("\u0621" <= ch <= "\u064a" for ch in w):
                rasm_marks += 1
            else:
                word_positions += 1
                if "ّ" in w:
                    shadda_words += 1
    assert word_positions == Nw and word_positions + rasm_marks + header_words == raw_words, \
        f"مقامُ المواضع خُولف: مواضع={word_positions} علامات={rasm_marks} ترويسة={header_words} — صريخ"
    n_var = sum(1 for c in sup.values() if len(c) >= 2)
    sup_states = Counter()
    for c in sup.values():
        if len(c) >= 2:
            for st in c:
                sup_states[st] += 1
    awzan_words, awzan_shadda, awzan_bits = awzan_cover(path, verses, sup)
    awzan_gain = awzan_words - awzan_shadda          # الجديدُ وحده: ما لم تغطّه ح-شدة
    scream = raw_words - shadda_words - awzan_gain
    # المتبقّي على مقامٍ واحد: مقامُ المواضع المفكوكة (77,801) لا الخام — فالعلاماتُ والترويسةُ
    # ليست مواضعَ كلماتٍ أصلًا، ولا تحملُ شدّةً البتّة، فبقاؤها في ⚑ تضخيمٌ لا دَين.
    scream_positions = word_positions - shadda_words - awzan_gain
    cost_bits = len(["ز-مزاح", "ق-فراغ", "ع-تبدل", "ث-وحدة",
                     "ح-شدة", "ح-جار-ملتصق"]) * 8 * 4 + awzan_bits
    # حكمُ الرسم: «ق» صنفٌ رابعٌ نهائيّ — الطبقة التاليةُ تشخيصيّةٌ معدودة لا تُحتسب تغطيةً
    # ولا تُسعَّر، فالحدّان ⚑ والكلفة محروسان بالعدّ هنا صراحةً.
    assert scream == 57603 and cost_bits == 1456, \
        f"حدُّ حكم الرسم خُولف: ⚑={scream} كلفة={cost_bits} — صريخ"
    assert scream_positions == 52998 and rasm_marks == 4578 and header_words == 27, \
        f"تصنيفُ الفرق خُولف: ⚑مواضع={scream_positions} علامات={rasm_marks} ترويسة={header_words} — صريخ"
    q_rasm = {e: dict(words=q_words[e], forms=len(q_forms[e]), definite=q_defi[e])
              for e in Q_RASM}
    q_rasm_total = dict(words=sum(q_words.values()), forms=sum(len(f) for f in q_forms.values()),
                        definite=sum(q_defi.values()))
    q_rasm_total["definite_pct"] = round(q_rasm_total["definite"] / q_rasm_total["words"] * 100, 2)
    return dict(Nw=Nw, cnt=dict(cnt), z=z_chk, q_split=dict(q_split),
                q_rasm=dict(by_ending=q_rasm, total=q_rasm_total, verdict="ق-فراغ صنفٌ رابعٌ نهائيّ"),
                skeletons=len(sup), n_var=n_var, sup_states=dict(sup_states),
                coverage=dict(raw_words=raw_words, shadda_words=shadda_words,
                              word_positions=word_positions,
                              rasm_marks=rasm_marks, header_words=header_words,
                              raw_minus_positions=raw_words - word_positions,
                              jar_mabni_words=mabni_words,
                              awzan_words=awzan_words, awzan_gain=awzan_gain,
                              scream=scream,          # ⚑ على المقام الخام (تاريخيّ — مُضخَّم بالعلامات)
                              shadda_only_positions=word_positions - shadda_words,
                              scream_positions=scream_positions),  # ⚑ الحقيقيّ على مقام المواضع
                rules_cost_bits=cost_bits)

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
    print(f"تغطية المبني السطحية: شدّة {R['coverage']['shadda_words']:,} كلمة · جار ملتصق {R['coverage']['jar_mabni_words']:,} · "
          f"أوزان {R['coverage']['awzan_words']:,} (جديدها {R['coverage']['awzan_gain']:,}) · "
          f"⚑ المتبقّي {R['coverage']['scream']:,} (لا قاعدة سطحية له — دَين المعجم الكامل)")
    C = R["coverage"]
    print(f"مقامان لا يُخلطان: خام {C['raw_words']:,} = مواضع {C['word_positions']:,} + "
          f"علامات رسمٍ {C['rasm_marks']:,} + ترويسة إسنادٍ {C['header_words']:,} "
          f"(الفرق {C['raw_minus_positions']:,} ليس كلماتٍ أصلًا ولا يحمل شدّةً) — "
          f"فـ⚑ على مقام المواضع {C['scream_positions']:,} (وبالشدّة وحدها {C['shadda_only_positions']:,})")
    print(f"كلفة القواعد الست + جدول الأوزان معلنة: {R['rules_cost_bits']} بت — تُخصم من أي ربحٍ يُبنى عليها")
    if out:
        json.dump({"المعجم_v0": R}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {out}")

if __name__ == "__main__":
    main()
