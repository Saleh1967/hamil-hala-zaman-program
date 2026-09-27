# hiyad.py — دعوى الحياد: «الألفُ عنصرٌ محايد، وربّما حروفُ العلّة محايدٌ موضعيّ».
#
# الدعوى مُجملةٌ فتُفصَّل: «محايدٌ» في أيِّ بُعد؟ فالحقلُ 112 بُعدان لا بُعدٌ واحد
# (حرفٌ × حالة)، والحيادُ في أحدهما لا يُلزِم الحيادَ في الآخر. فتُعرَض على أربعة
# فحوصٍ يستطيع كلُّ واحدٍ منها أن يرفض، ثمّ على الحَكَم المودَع (الفاتورة):
#
#   ① حيادُ الحالة  — هل يحمل الحرفُ حركةً قطّ؟
#   ② حيادٌ موضعيّ  — وهل يختلف ذلك باختلاف الموضع؟
#   ③ حيادٌ جبريّ   — هل يُطوى وسمًا ويُستردّ بلا خسارة؟ (الوسيطُ مُفقِدٌ والارتدادُ أعمى)
#   ④ حيادٌ تقابليّ — هل يفرّق بين هيئتين؟ فما فرّق فليس محايدًا.
#
# — الحكم —
# ① **الألفُ محايدةٌ في الحالة حيادًا تامًّا مقيسًا**: 43,545/43,545 = 1.0000 عُرْيًا.
#    لا تسكن خليّةً واحدةً من 112 البتّة، وكذلك «ى» 2,592 و«آ» 1,511. وهي الحروفُ
#    الثلاثةُ وحدَها في المجمَّد كلِّه التي بلغت الواحدَ الصحيح.
# ② **«محايدٌ موضعيّ» تثبت لـ و/ي بشرطها المقيس**: أوّلًا 0.0000 و0.0002 — لا حيادَ
#    البتّة (واوُ العطف ومضارعةُ الياء)؛ ووسطًا 0.7150 و0.4703، وآخرًا 0.8400 لـ«ي».
#    فالحيادُ فيهما **دالّةُ موضعٍ** لا صفةَ حرف. وأمّا الألفُ فحيادُها غيرُ موضعيّ:
#    1.0000 في المواضع الثلاثة جميعًا.
# ③ الطيُّ يرتدّ تامًّا (77,801/77,801) لكنّ **10,791 ألفًا لا تُطوى**: أوّلُ الكلمة لا
#    يسارَ له يسنده — وهو رأسُ الوصل بعينه. **لا محايدَ بلا يسارٍ يحمله.**
#    ولـ و/ي موضعٌ واحدٌ متعذّر في المجمَّد كلِّه: «يس».
# ④ **دعوى الحياد مردودةٌ في بُعد الحرف**: حذفُ الألف يُصادِم 1,167 هيئةً ويُضيع
#    تمييزَ 1,355 (كذب · كاذب · كذاب · كذابا) في 11,024 موضعًا. والمحايدُ لا يفرّق.
# ⑤ **والحَكَمُ يقلب الترتيب**: طيُّ الألف — وهي الأتمُّ حيادًا في الحالة — **يُرفَض**
#    (+24,145)، وطيُّ و/ي — وهما المحايدان موضعيًّا لا مطلقًا — **يُقبَل** (−5,427).
#    فالحيادُ المقيسُ في بُعدٍ لا يشتري قبولًا في الفاتورة، والقبولُ لا يُنال بالوصف.
import argparse, hashlib, json, math, os, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from deposit_law import verdict                # المصادقُ المركزيّ — الحكمُ لا يُعاد كتابتُه

CORPUS = os.path.join(ROOT, "mujammad.txt")
SEAL = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"

MADD = 0x0670
SHADDA = 0x0651
VOWM = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TANM = {0x064B: "فتحة", 0x064C: "ضمة", 0x064D: "كسرة"}
MK = {"فتحة": "\u064E", "ضمة": "\u064F", "كسرة": "\u0650", "سكون": "\u0652"}
TN = {"فتحة": "\u064B", "ضمة": "\u064C", "كسرة": "\u064D"}
BARE = "عُرْي"
ILLA = "اوي"                       # حروفُ العلّة — مرتَّبةٌ معلنةً، ورمزُ الوسم فهرسُها + 1

AR = lambda c: 0x0621 <= ord(c) <= 0x064A
KEEP = lambda w: "".join(c for c in w if AR(c) or 0x064B <= ord(c) <= 0x0652 or ord(c) == MADD)

# ── أرقامُ هذه الجولة، تُجمَّد بنصّها ثمّ تُصادَم بفارق صفرٍ أو صريخ ──────────────
SEALED_HIYAD = dict(
    ألف=43545, ألف_عُرْي=43545, مقصورة=2592, ممدودة=1511,
    واو=25092, ياء=23054,
    ألف_أول=10791, ألف_وسط=15735, ألف_آخر=17019,
    واو_أول=10084, ياء_أول=4771, ياء_أول_عُرْي=1,
    طيُّ_الألف_ارتداد=77801, طيُّ_الألف_متعذّر=10791,
    طيُّ_العلّة_متعذّر=14177, طيُّ_الواو_والياء_متعذّر=1,
    تصادمُ_حذف_الألف=1167, ضياعُ_حذف_الألف=1355, مواضعُ_حذف_الألف=11024,
    تصادمُ_حذف_العلّة=2614, ضياعُ_حذف_العلّة=5425, مواضعُ_حذف_العلّة=31615,
    فاتورةُ_الأساس=2383040, طيُّ_الألف=24145, طيُّ_العلّة=18636, طيُّ_الواو_والياء=-5427)


# ═══ الأساسُ: قراءةٌ ونزولٌ وصعودٌ — بنفس قواعد jami3_mani3 المعلنة ══════════════
def read_verses(path=CORPUS):
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == SEAL, "ليس المجمَّد — البصمةُ خُولفت"
    verses = []
    for ln in blob.decode("utf-8-sig").splitlines():
        if not ln.strip() or not any(AR(c) for c in ln):
            continue
        ws = [w for w in ln.split(" ") if any(AR(c) for c in w)]
        if ws:
            verses.append(ws)
    assert len(verses) == 6236 and sum(len(v) for v in verses) == 77801, "المصالحةُ خُولفت"
    return verses


def descend(word):
    """R5 الشدّةُ ساكنٌ ثمّ متحرّك · R4 التنوينُ حركةٌ ثمّ نونٌ ساكنة · الخنجريةُ وسمٌ مرافق."""
    out, i, n = [], 0, len(word)
    while i < n:
        ch = word[i]
        if not AR(ch):
            i += 1
            continue
        marks = []
        while i + 1 < n and (0x064B <= ord(word[i + 1]) <= 0x0652 or ord(word[i + 1]) == MADD):
            i += 1
            marks.append(ord(word[i]))
        tan = next((m for m in marks if m in TANM), None)
        vow = next((m for m in marks if m in VOWM), None)
        st = VOWM[vow] if vow else TANM[tan] if tan else BARE
        if SHADDA in marks:
            out.append((ch, "سكون", "R5", False))
        out.append((ch, st, "R4" if tan and not vow else "رسم", MADD in marks))
        if tan:
            out.append(("ن", "سكون", "R4", False))
        i += 1
    return out


def ascend(units):
    """صعودٌ أعمى: لا يرى الكلمةَ الأصل، فلا يستطيع أن يخفي ضياعًا."""
    out, i, n = "", 0, len(units)
    while i < n:
        ch, st, src, dg = units[i]
        if src == "R5":
            ch, st, src, dg = units[i + 1]
            sh = "\u0651"
            i += 2
        else:
            sh = ""
            i += 1
        tail = "\u0670" if dg else ""
        if src == "R4":
            out += ch + sh + TN[st] + tail
            i += 1
        else:
            out += ch + sh + (MK.get(st, "") if st != BARE else "") + tail
    return out


# ═══ ① و② حيادُ الحالة، وموضعيّتُه ══════════════════════════════════════════════
def state_neutrality(verses, U):
    """لكلِّ حرفٍ نسبةُ العُرْي — والمحايدُ في الحالة مَن لم يحمل حركةً قطّ (نسبةٌ = 1).
    ثمّ الموضعُ: أوّلُ الوحدات · وسطُها · آخرُها — فالحيادُ قد يكون دالّةَ موضعٍ لا صفةَ حرف."""
    per, pos = defaultdict(Counter), defaultdict(Counter)
    for v in verses:
        for w in v:
            u = U[w]
            for j, (ch, st, _, _) in enumerate(u):
                per[ch][st] += 1
                if ch in ILLA:
                    pos[(ch, "أول" if j == 0 else "آخر" if j == len(u) - 1 else "وسط")][st] += 1
    tot = lambda c: sum(c.values())
    letters = {c: dict(عدد=tot(k), عُرْي=k[BARE], نسبة=round(k[BARE] / tot(k), 4))
               for c, k in per.items() if tot(k) > 500}
    places = {f"{c}·{p}": dict(عدد=tot(k), نسبة=round(k[BARE] / tot(k), 4),
                               أعلى=dict(k.most_common(3)))
              for (c, p), k in pos.items() if tot(k)}
    return letters, places


# ═══ ③ الحيادُ الجبريّ: الطيُّ والاسترداد ═══════════════════════════════════════
def fold(units, letters):
    """طيُّ حرفِ علّةٍ **عارٍ** وسمَ مدٍّ على الوحدة السابقة — وهو معنى «العنصر المحايد»:
    ما لا يشغل موضعًا مستقلًّا. ويُعَدّ **المتعذّر**: ما لا يسارَ له يحمله."""
    out, stuck = [], []
    for ch, st, src, dg in units:
        if ch in letters and st == BARE and src == "رسم":
            if out and out[-1][4] == 0:
                out[-1][4] = 1 + ILLA.index(ch)
                continue
            stuck.append(ch)
        out.append([ch, st, src, dg, 0])
    return out, stuck


def unfold(folded):
    out = []
    for ch, st, src, dg, md in folded:
        out.append((ch, st, src, dg))
        if md:
            out.append((ILLA[md - 1], BARE, "رسم", False))
    return out


def algebraic_neutrality(verses, U, letters):
    ok, stuck, ex = 0, 0, Counter()
    for v in verses:
        for w in v:
            f, s = fold(U[w], letters)
            stuck += len(s)
            if s:
                ex[w] += 1
            if ascend(unfold(f)) == KEEP(w):
                ok += 1
    return dict(ارتداد=ok, متعذّر=stuck, أمثلةُ_التعذّر=[w for w, _ in ex.most_common(3)])


# ═══ ④ الحيادُ التقابليّ: هل يفرّق بين هيئتين؟ ═══════════════════════════════════
def contrastive(verses, letters):
    """المحايدُ لا يفرّق. فإن أُسقط الحرفُ من الهيئات فتصادمت، فقد كان يفرّق — والعدُّ يُظهره."""
    forms = Counter()
    for v in verses:
        for w in v:
            forms["".join(c for c in w if AR(c))] += 1
    g = defaultdict(set)
    for f in forms:
        g["".join(c for c in f if c not in letters)].add(f)
    amb = [(k, sorted(s)) for k, s in g.items() if len(s) > 1]
    return dict(تصادم=len(amb), ضياعُ_التمييز=sum(len(s) - 1 for _, s in amb),
                مواضع=sum(forms[x] for _, s in amb for x in s[1:]),
                أمثلة=[f"{k or '∅'} ⟵ {' · '.join(s[:5])}"
                       for k, s in sorted(amb, key=lambda x: -len(x[1]))[:3]])


# ═══ ⑤ الحَكَم: الفاتورة نفسُها، والوسمُ مدفوعُ الثمن ═══════════════════════════
def cost(c):
    n = sum(c.values())
    return -sum(k * math.log2(k / n) for k in c.values())


def bill(verses, U, letters):
    """خلايا + منشأ + خنجرية + **وسمُ المدّ**. ولا يُشترى القبولُ بإخفاء ثمنِ وسم."""
    cell, org, dgv, md = Counter(), Counter(), Counter(), Counter()
    for v in verses:
        for w in v:
            if letters:
                f, _ = fold(U[w], letters)
                for ch, st, src, dg, m in f:
                    cell[(ch, st)] += 1
                    org[src] += 1
                    dgv[dg] += 1
                    md[m] += 1
            else:
                for ch, st, src, dg in U[w]:
                    cell[(ch, st)] += 1
                    org[src] += 1
                    dgv[dg] += 1
    t = cost(cell) + cost(org) + cost(dgv) + (cost(md) if letters else 0)
    return dict(وحدات=sum(org.values()), خلايا=round(cost(cell)), منشأ=round(cost(org)),
                خنجرية=round(cost(dgv)), وسمُ_المدّ=round(cost(md)) if letters else 0,
                الكلّ=round(t))


def main():
    verses = read_verses()
    U = {}
    for v in verses:
        for w in v:
            U.setdefault(w, descend(w))
    print("دعوى الحياد: «الألفُ عنصرٌ محايد، وربّما حروفُ العلّة محايدٌ موضعيّ»")
    print(f"  المجمَّد: {len(verses):,} آيةً · {sum(len(v) for v in verses):,} كلمةً · الختمُ مطابق\n")

    # ── ① حيادُ الحالة ──
    L, P = state_neutrality(verses, U)
    order = sorted(L.items(), key=lambda x: -x[1]["نسبة"])
    print("— ① حيادُ الحالة: نسبةُ العُرْي لكلِّ حرفٍ (فوق 500 موضع) —")
    for c, d in order[:6]:
        mark = "  ⟸ محايدٌ تامًّا" if d["نسبة"] == 1.0 else ""
        print(f"    {c}  {d['نسبة']:.4f}  من {d['عدد']:>7,}{mark}")
    print(f"    … وأدناها: " + " · ".join(f"{c} {d['نسبة']:.4f}" for c, d in order[-4:]))
    assert L["ا"]["عدد"] == SEALED_HIYAD["ألف"] and L["ا"]["عُرْي"] == SEALED_HIYAD["ألف_عُرْي"]
    assert L["ى"]["عدد"] == SEALED_HIYAD["مقصورة"] and L["آ"]["عدد"] == SEALED_HIYAD["ممدودة"]
    assert L["و"]["عدد"] == SEALED_HIYAD["واو"] and L["ي"]["عدد"] == SEALED_HIYAD["ياء"]
    assert L["ا"]["نسبة"] == 1.0 and L["ى"]["نسبة"] == 1.0 and L["آ"]["نسبة"] == 1.0
    print("    ✓ الألفُ والمقصورةُ والممدودةُ وحدَها بلغت الواحدَ الصحيح — دعوى الحياد "
          "**تثبت في بُعد الحالة**\n")

    # ── ② الحيادُ الموضعيّ ──
    print("— ② حيادٌ موضعيّ: أهو صفةُ حرفٍ أم دالّةُ موضع؟ —")
    for c in ILLA:
        row = " · ".join(f"{p} {P[f'{c}·{p}']['نسبة']:.4f} ({P[f'{c}·{p}']['عدد']:,})"
                         for p in ("أول", "وسط", "آخر") if f"{c}·{p}" in P)
        print(f"    {c}: {row}")
    assert P["ا·أول"]["عدد"] == SEALED_HIYAD["ألف_أول"]
    assert P["ا·وسط"]["عدد"] == SEALED_HIYAD["ألف_وسط"]
    assert P["ا·آخر"]["عدد"] == SEALED_HIYAD["ألف_آخر"]
    assert P["و·أول"]["عدد"] == SEALED_HIYAD["واو_أول"] and P["و·أول"]["نسبة"] == 0.0
    assert P["ي·أول"]["عدد"] == SEALED_HIYAD["ياء_أول"]
    assert P["ي·أول"]["أعلى"].get(BARE, 0) == SEALED_HIYAD["ياء_أول_عُرْي"]
    print("    ✓ و/ي **محايدان موضعيًّا لا مطلقًا**: أوّلًا صفرٌ (واوُ العطف ومضارعةُ الياء)، "
          "ووسطًا وآخرًا حيادٌ غالب")
    print("    ✗ والألفُ حيادُها **غيرُ موضعيّ**: 1.0000 في المواضع الثلاثة — فشطرُ الدعوى "
          "الثاني لا ينطبق عليها\n")

    # ── ③ الحيادُ الجبريّ ──
    print("— ③ حيادٌ جبريّ: أيُطوى وسمًا ويُستردّ؟ (الوسيطُ مُفقِدٌ والارتدادُ أعمى) —")
    A = {}
    for nm, ls in (("ا", "ا"), ("ا و ي", ILLA), ("و ي", "وي")):
        A[ls] = algebraic_neutrality(verses, U, ls)
        d = A[ls]
        print(f"    طيُّ ({nm:5s}): ارتدادٌ {d['ارتداد']:,}/77,801 = {d['ارتداد'] / 77801:.4f}"
              f" · متعذّرٌ {d['متعذّر']:,}"
              + (f" · مثالُه {d['أمثلةُ_التعذّر'][0]}" if d["أمثلةُ_التعذّر"] else ""))
    assert A["ا"]["ارتداد"] == SEALED_HIYAD["طيُّ_الألف_ارتداد"]
    assert A["ا"]["متعذّر"] == SEALED_HIYAD["طيُّ_الألف_متعذّر"]
    assert A[ILLA]["متعذّر"] == SEALED_HIYAD["طيُّ_العلّة_متعذّر"]
    assert A["وي"]["متعذّر"] == SEALED_HIYAD["طيُّ_الواو_والياء_متعذّر"]
    print(f"    ✓ الارتدادُ تامٌّ، لكنّ {A['ا']['متعذّر']:,} ألفًا **لا تُطوى**: أوّلُ الكلمة "
          "لا يسارَ له يحمله — وهو رأسُ الوصل بعينه")
    print("      **لا محايدَ بلا يسارٍ يسنده.** ولـ و/ي موضعٌ واحدٌ متعذّرٌ في المجمَّد "
          "كلِّه: فاتحةُ «يس»\n")

    # ── ④ الحيادُ التقابليّ ──
    print("— ④ حيادٌ تقابليّ: أيفرّق بين هيئتين؟ فما فرّق فليس محايدًا —")
    C = {}
    for nm, ls in (("ا", "ا"), ("و", "و"), ("ي", "ي"), ("ا و ي", ILLA)):
        C[ls] = contrastive(verses, ls)
        d = C[ls]
        print(f"    حذفُ ({nm:5s}): تصادمَ {d['تصادم']:,} هيئةً · ضاع تمييزُ "
              f"{d['ضياعُ_التمييز']:,} · في {d['مواضع']:,} موضعًا")
        print(f"          {d['أمثلة'][0]}")
    assert C["ا"]["تصادم"] == SEALED_HIYAD["تصادمُ_حذف_الألف"]
    assert C["ا"]["ضياعُ_التمييز"] == SEALED_HIYAD["ضياعُ_حذف_الألف"]
    assert C["ا"]["مواضع"] == SEALED_HIYAD["مواضعُ_حذف_الألف"]
    assert C[ILLA]["تصادم"] == SEALED_HIYAD["تصادمُ_حذف_العلّة"]
    assert C[ILLA]["ضياعُ_التمييز"] == SEALED_HIYAD["ضياعُ_حذف_العلّة"]
    assert C[ILLA]["مواضع"] == SEALED_HIYAD["مواضعُ_حذف_العلّة"]
    print("    ✗ **الدعوى مردودةٌ في بُعد الحرف**: المحايدُ لا يفرّق، والألفُ تفرّق في "
          f"{C['ا']['مواضع']:,} موضعًا\n")

    # ── ⑤ الحَكَم ──
    print("— ⑤ الحَكَم: الفاتورة (ووسمُ المدّ مدفوعُ الثمن) —")
    base = bill(verses, U, None)
    print(f"    الحقلُ كما هو          {base['وحدات']:>7,} وحدةً · {base['الكلّ']:>9,} بت")
    B = {}
    for nm, ls in (("ا", "ا"), ("ا و ي", ILLA), ("و ي", "وي")):
        b = bill(verses, U, ls)
        b["فرق"] = b["الكلّ"] - base["الكلّ"]
        B[ls] = b
        print(f"    طيُّ ({nm:5s})           {b['وحدات']:>7,} وحدةً · {b['الكلّ']:>9,} بت "
              f"(وسمُ المدّ {b['وسمُ_المدّ']:,}) · Δ {b['فرق']:+,} ⟹ "
              + verdict(b["فرق"]))
    assert base["الكلّ"] == SEALED_HIYAD["فاتورةُ_الأساس"], "فاتورةُ الأساس خالفت الجامعَ المانع"
    assert B["ا"]["فرق"] == SEALED_HIYAD["طيُّ_الألف"]
    assert B[ILLA]["فرق"] == SEALED_HIYAD["طيُّ_العلّة"]
    assert B["وي"]["فرق"] == SEALED_HIYAD["طيُّ_الواو_والياء"]
    print("\n    **والحَكَمُ يقلب الترتيب**: الألفُ الأتمُّ حيادًا في الحالة **تُرفَض** "
          f"({B['ا']['فرق']:+,})، و و/ي المحايدان **موضعيًّا لا مطلقًا** **يُقبَلان** "
          f"({B['وي']['فرق']:+,}).")
    print("    فالحيادُ المقيسُ في بُعدٍ لا يشتري قبولًا في الفاتورة — والوصفُ لا يُغني "
          "عن الثمن.\n")

    print("الحكم: ① تثبت في الحالة (1.0000) · ② تثبت لـ و/ي بشرط الموضع لا للألف · "
          "③ تثبت بحدٍّ معدود (10,791 رأسَ وصلٍ لا يُطوى) · ④ تُرَدّ في الحرف (11,024 "
          "موضعَ تفريق) · ⑤ والحَكَمُ يقبل و/ي (−5,427) ويرفض الألف (+24,145).")

    return dict(الدعوى="الألفُ عنصرٌ محايد، وربّما حروفُ العلّة محايدٌ موضعيّ",
                حيادُ_الحالة=L, حيادٌ_موضعيّ=P,
                حيادٌ_جبريّ={k: v for k, v in A.items()},
                حيادٌ_تقابليّ={k: v for k, v in C.items()},
                الحَكَم=dict(أساس=base, **{k: v for k, v in B.items()}),
                الحكم="محايدةٌ في الحالة لا في الحرف · والعلّةُ محايدٌ موضعيٌّ يقبله الحَكَم")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    a = ap.parse_args()
    R = main()
    if a.json:
        json.dump({"دعوى_الحياد": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True, default=str)
        print(f"JSON ⟵ {a.json}")
