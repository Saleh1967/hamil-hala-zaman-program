# induction_engine.py — جذرٌ مستقل: ماركوف + استقراء-ON ثم استقراء-FOR وبالعكس + الجشع + ستيرلنج
# من الصفر: لا استيراد من غيره. القوانين الموروثة معلنة بأسمائها:
#   α=1 تنعيمٌ لابلاسي موسوم · ترميز عدٍّ مسطَّح log2(Ntr+1) للخلية ·
#   تقسيم تدريب/اختبار متناوب (ل٣/ع٩) · فاتورة = بيانات + خريطة + جدول.
# ستيرلنج حارسُ الاستنفاد: عدد التقسيمات إلى k أجزاء = S(n,k) — يُعدّ ويُبرهَن بالتوليد.
# المجمَّد (إن وُجد): mujammad.txt بختم 8b387ea8… — غيابُه ⟵ وضعٌ بنيوي موسوم، لا قياس مؤجَّل بصمت.
from math import log2
from collections import Counter, defaultdict
import hashlib, os, json, argparse

CORPUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
SEAL = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"

VOW = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TAN = {0x064B: "تنوين فتح", 0x064C: "تنوين ضم", 0x064D: "تنوين كسر"}
AR = lambda ch: 0x0621 <= ord(ch) <= 0x063A or 0x0641 <= ord(ch) <= 0x064A

# ---------- ١) التحليل: كل آية ⟼ كلمات، وكل كلمة ⟼ (حرف، حالة) — من الصفر ----------
def parse_verses(path):
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == SEAL, "ليس المجمَّد — البصمة خُالفت"
    verses = []
    for ln in blob.decode("utf-8-sig").splitlines():
        if not ln.strip() or not any(AR(c) for c in ln):
            continue
        words = []
        for w in ln.split(" "):
            pos, i, n = [], 0, len(w)
            while i < n:
                if AR(w[i]):
                    ch = w[i]                      # الحرف يُحفَظ قبل استهلاك الحركات
                    marks = []
                    while i + 1 < n and (0x064B <= ord(w[i + 1]) <= 0x0652 or ord(w[i + 1]) == 0x0670):
                        i += 1; marks.append(ord(w[i]))
                    vs = [m for m in marks if m in VOW]; ts = [m for m in marks if m in TAN]
                    st = TAN[ts[0]] if ts else VOW[vs[0]] if vs else "فتحة" if 0x0670 in marks else "عري"
                    pos.append((ch, st))
                i += 1
            if pos:
                words.append(pos)
        if words:
            verses.append(words)
    assert len(verses) == 6236, "بصمة الآيات خُالفت"
    return verses

def states_stream(verses, cross):
    """تيار الحالات الموضعية. cross=False: داخل السطر فقط (ON) · cross=True: يُضاف حدُّ العبور بين السطرين."""
    big, prv, prev_last = Counter(), Counter(), None
    for words in verses:
        seq = [st for w in words for _, st in w]
        edges = list(zip(seq, seq[1:]))
        if cross and prev_last is not None:
            edges = [(prev_last, seq[0])] + edges
        for a, b in edges:
            big[(a, b)] += 1; prv[a] += 1
        if seq:
            prev_last = seq[-1]
    return big, prv

# ---------- ٢) بوّابات الآيات الخام (سطحية معلنة — بلا قلع، بلا معجم) ----------
JARR = {"من", "عن", "على", "الى", "في"}
JPRE = {"ب", "ل", "ك"}
GATES5 = ("C", "J", "A", "T", "B")

def gate(first_word):
    pos = first_word
    skel = "".join(ch for ch, _ in pos)
    if pos[0] in (("و", "فتحة"), ("ف", "فتحة")):
        return "C"
    if skel in JARR or (pos[0][0] in JPRE and pos[0][1] == "كسرة"):
        return "J"
    if len(skel) >= 2 and skel[0] == "ا" and skel[1] == "ل":
        return "A"
    if pos[-1][1] in TAN.values():
        return "T"
    if len(pos) >= 2 and pos[-2][1] == "تنوين فتح" and pos[-1][0] in ("ا", "ى") and pos[-1][1] == "عري":
        return "T"
    return "B"

# ---------- ٣) ستيرلنج: القانون المعدود + التوليد المستقل = البرهان ----------
def stirling(n, k):
    """S(n,k) بالعودة: تقسيم n عنصرًا إلى k أجزاء غير فارغة."""
    if n == k == 0: return 1
    if n == 0 or k == 0 or k > n: return 0
    return k * stirling(n - 1, k) + stirling(n - 1, k - 1)

def bell(n):
    return sum(stirling(n, k) for k in range(1, n + 1))

def partitions(n):
    """توليد كل التقسيمات (سلاسل نموّ مقيَّدة) — مستقلٌّ عن القانون، فيُصادَمان."""
    out = []
    def rec(r):
        if len(r) == n:
            out.append(tuple(r)); return
        for v in range(max(r) + 2):
            rec(r + [v])
    rec([0])
    return out

# ---------- ٤) فواتير الاستقراء: بيانات + خريطة + جدول ----------
ALPHA = 1  # سياسة موسومة

def split_alternating(pairs):
    return pairs[::2], pairs[1::2]

def ce_table(tab, prv, ps, m, alpha=ALPHA):
    return sum(-log2((tab[(a, b)] + alpha) / (prv[a] + alpha * m)) for a, b in ps)

def invoice_unigram(train, test, m):
    Ntr = len(train)
    ug = Counter(b for _, b in train)
    data = sum(-log2((ug[b] + ALPHA) / (Ntr + ALPHA * m)) for _, b in train)
    cell = log2(Ntr + 1)
    return data + m * cell, data, m * cell

def invoice_markov(train, test, m):
    Ntr = len(train)
    tab, prv = Counter(train), Counter(a for a, _ in train)
    data = ce_table(tab, prv, train, m)
    cell = log2(Ntr + 1)
    return data + m * m * cell, data, m * m * cell

def for_rows(train, assign, m):
    """من العناقيد تُشتقَّق الصفوف (FOR) — تجميع سوابق كل عنقود."""
    rows, row_tot = Counter(), Counter()
    for (a, b) in train:
        r = assign[a]
        rows[(r, b)] += 1; row_tot[r] += 1
    return rows, row_tot

def invoice_for(train, assign, m):
    """الفاتورة = بيانات بصفوف مشتقة + خريطة n·log2(n) + k·m خلية."""
    Ntr = len(train)
    rows, row_tot = for_rows(train, assign, m)
    data = sum(-log2((rows[(assign[a], b)] + ALPHA) / (row_tot[assign[a]] + ALPHA * m)) for a, b in train)
    k = len(set(assign.values())); cell = log2(Ntr + 1)
    model = m * log2(m) + k * m * cell
    return data + model, data, model, k

def greedy_path(train, symbols, m):
    """الجشع التدريجي: ادمج أزواج العناقيد بأفضل تحسّن فاتورة، حتى التثبّت."""
    clusters = {s: frozenset([s]) for s in symbols}
    def assign_of(cl):
        return {s: i for i, c in enumerate(sorted(cl.values(), key=lambda c: sorted(c))) for s in c}
    path = []
    while True:
        cur, _, _, _ = invoice_for(train, assign_of(clusters), m)
        uniq = list({c for c in clusters.values()})
        best = (cur, None)
        for i in range(len(uniq)):
            for j in range(i + 1, len(uniq)):
                merged = uniq[i] | uniq[j]
                trial = {s: (merged if clusters[s] in (uniq[i], uniq[j]) else clusters[s]) for s in clusters}
                inv, _, _, _ = invoice_for(train, assign_of(trial), m)
                if inv < best[0] - 1e-12:
                    best = (inv, trial)
        if best[1] is None:
            break
        clusters = best[1]; path.append(best[0])
    return assign_of(clusters), (path[-1] if path else cur), path

# ---------- ٥) التجربة الكاملة على تيار البوّابات ----------
def run_gates(verses):
    seq = [gate(v[0]) for v in verses]
    pairs = list(zip(seq, seq[1:]))
    Np = len(pairs)
    train, test = split_alternating(pairs)
    Ntr, Nte = len(train), len(test)
    m = 5
    inv_u, d_u, mod_u = invoice_unigram(train, test, m)
    inv_m, d_m, mod_m = invoice_markov(train, test, m)

    # الاستنفاد الكامل بحراسة ستيرلنج: Bell(5)=52 = Σ S(5,k)
    counts_k = Counter(len(set(p)) for p in partitions(m))
    stir_guard = all(counts_k[k] == stirling(m, k) for k in range(1, m + 1)) and sum(counts_k.values()) == bell(m)
    best = None
    for p in partitions(m):
        assign = dict(zip(GATES5, p))
        inv, data, model, k = invoice_for(train, assign, m)
        if best is None or inv < best[0] - 1e-12:
            best = (inv, data, model, k, assign)
    inv_o, d_o, mod_o, k_o, assign_o = best
    groups = defaultdict(list)
    for g in GATES5:
        groups[assign_o[g]].append(g)

    assign_g, inv_g, gpath = greedy_path(train, GATES5, m)

    # خارج العيّنة: أحاديّ / ماركوف / مدمج أمثل
    ug = Counter(b for _, b in train); tab = Counter(train); prv = Counter(a for a, _ in train)
    rows_o, row_tot_o = for_rows(train, assign_o, m)
    te_u = sum(-log2((ug[b] + ALPHA) / (Ntr + ALPHA * m)) for _, b in test) / Nte
    te_m = ce_table(tab, prv, test, m) / Nte
    te_o = sum(-log2((rows_o[(assign_o[a], b)] + ALPHA) / (row_tot_o[assign_o[a]] + ALPHA * m)) for a, b in test) / Nte

    # العكس: FOR ثم ON — العناقيد أولًا (تقريب الأبجدية)، ثم ماركوف على المسميات
    # استقراء FOR أوّلًا: عنقودان ثابتان من الشبه البنيوي المعلن (الجارّية C/J مقابل الاسمية A/T والعمياء B)
    coarse = {"C": 0, "J": 0, "A": 1, "T": 1, "B": 2}
    seq_c = [coarse[g] for g in seq]
    pairs_c = list(zip(seq_c, seq_c[1:]))
    tr_c, te_c = split_alternating(pairs_c)
    tab_c = Counter(tr_c); prv_c = Counter(a for a, _ in tr_c); m_c = 3
    d_c = ce_table(tab_c, prv_c, tr_c, m_c)
    inv_con = d_c + 3 * log2(3) + 3 * 3 * log2(Ntr + 1)  # خريطة + جدول العناقيد

    # H(تالي|سابق) باتفاقيةٍ واحدةٍ معلنة: **الجدولُ والمقاماتُ من الأزواج كلِّها** (وصفُ التيار
    # لا فاتورةُ نموذج، فلا تقسيمَ تدريبٍ هنا). وكان المودَعُ سابقًا يخلط نصفًا بكلّ — جدولُ
    # `train` على مقامات `pairs` — فتجمع كتلةُ كلِّ سابقةٍ ≈0.50 لا 1.0، فلا تكون إنتروبيا
    # شرطيةً أصلًا: Hc 1.20497 و«ربح عبور» 0.2133. السحبُ بحسابٍ معروض: Hc ≈ (Hc_صحيح+1)/2.
    prv_all = Counter(a for a, _ in pairs)
    tab_all = Counter(pairs)
    Hc = sum(prv_all[a] / Np * (-sum(v / prv_all[a] * log2(v / prv_all[a])
             for (x, _), v in tab_all.items() if x == a)) for a in GATES5)
    # حارسٌ يمنع عودةَ الخلط صامتًا: كتلةُ كلِّ سابقةٍ واحدٌ صحيح.
    for a in GATES5:
        mass = sum(v / prv_all[a] for (x, _), v in tab_all.items() if x == a)
        assert abs(mass - 1.0) < 1e-9, f"كتلةُ السابقة {a} = {mass} — جدولٌ ومقامٌ من مقامين"
    return dict(Nv=len(seq), Np=Np, Ntr=Ntr, Nte=Nte,
                marginal=Counter(seq), H_cond=Hc,
                # التسميةُ تحمل مقامَها: الجدولُ الأول نصفُ التدريب (3,118)، والثاني الأزواجُ كلُّها
                # (6,235) — وكان اسمٌ واحدٌ «transitions» يحمل الأوّلَ ويُقرَأ كأنه الثاني.
                transitions_train={f"{a}→{b}": v for (a, b), v in tab.items()},
                transitions_all={f"{a}→{b}": v for (a, b), v in tab_all.items()},
                unigram=(inv_u, d_u, mod_u), markov=(inv_m, d_m, mod_m),
                stirling={k: stirling(m, k) for k in range(1, m + 1)}, bell=bell(m),
                stir_guard=stir_guard,
                optimal=(inv_o, d_o, mod_o, k_o, {r: sorted(v) for r, v in groups.items()}),
                greedy=(inv_g, len(gpath), gpath),
                gap=inv_g - inv_o,
                test_ce=(te_u, te_m, te_o),
                for_then_on=(inv_con, d_c),
                orders_gap=inv_con - inv_o)

# ---------- ٦) الفحص المشغَّل ----------
def structural():
    # حراسة ستيرلنج/بيل على n=4 وn=5 بلا قياس
    g4 = Counter(len(set(p)) for p in partitions(4))
    g5 = Counter(len(set(p)) for p in partitions(5))
    ok4 = all(g4[k] == stirling(4, k) for k in range(1, 5)) and sum(g4.values()) == bell(4)
    ok5 = all(g5[k] == stirling(5, k) for k in range(1, 6)) and sum(g5.values()) == bell(5)
    assert ok4 and ok5, "حارس ستيرلنج صرخ — التوليد خالف القانون المعدود"
    return {"S4": {k: stirling(4, k) for k in range(1, 5)}, "Bell4": bell(4),
            "S5": {k: stirling(5, k) for k in range(1, 6)}, "Bell5": bell(5)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", nargs="?", const="results.json")
    ap.add_argument("--require-corpus", action="store_true")
    args = ap.parse_args()
    OUT = {"جذر": "induction_engine — مستقل من الصفر", "بنيوي": structural()}
    print("ستيرلنج: S(4,k)=1,7,6,1 (Bell=15) · S(5,k)=1,15,25,10,1 (Bell=52) — التوليد مطابقٌ للقانون ✓")
    if os.path.exists(CORPUS):
        verses = parse_verses(CORPUS)
        R = run_gates(verses)
        OUT["مقيس"] = R
        ug = R["marginal"]
        H = -sum(v / R["Nv"] * log2(v / R["Nv"]) for v in ug.values())
        Np = R["Np"]; Hc = R["H_cond"]
        iu, du, mu = R["unigram"]; im, dm, mm = R["markov"]
        io, do_, mo, ko, gr = R["optimal"]; ig, steps, gp = R["greedy"]
        te_u, te_m, te_o = R["test_ce"]; con_inv, con_data = R["for_then_on"]
        print(f"بوّابات {R['Nv']:,} آية · أزواج {Np:,} (عبور الحدّ معلن) · تدريب {R['Ntr']:,}/اختبار {R['Nte']:,} — α=1")
        print(f"الهامش: " + " · ".join(f"{k}={ug[k]:,}" for k in GATES5) +
              f" | H={H:.4f} · H(تالي|سابق)={Hc:.4f} — ربح العبور {H - Hc:.4f} بت/آية"
              f"  [التيار: بوّابات-الآيات-بالعبور · الدالة: run_gates ⟵ gate() · المقام: الأزواج كلُّها 6,235]")
        print(f"الاستقراء ON: أحاديّ فاتورة {iu:.1f} (بيانات {du:.1f}+نموذج {mu:.1f}) · ماركوف25 {im:.1f} ({dm:.1f}+{mm:.1f})")
        print(f"الاستقراء FOR (استنفاد 52 بحراسة ستيرلنج): أمثل {io:.1f} (بيانات {do_:.1f}+نموذج {mo:.1f}، k={ko}: " +
              " + ".join("/".join(v) for v in gr.values()) + ")")
        print(f"الجشع التدريجي: {ig:.1f} بعد {steps} دمجات — فارقه عن الأمثل {ig - io:+.2f} (معروضٌ لا مكتوم)")
        print(f"خارج العيّنة: أحاديّ {te_u:.4f} · ماركوف {te_m:.4f} · مدمج أمثل {te_o:.4f} بت/زوج")
        print(f"الترتيب المعكوس FOR→ON (عناقيد معلنة ثم ماركوف): فاتورة {con_inv:.1f} — فرقُ الترتيب {con_inv - io:+.1f} بت (الأسبوقية للأرخص معروضة)")
        F = run_field112(verses)
        OUT["مقيس"]["حقل112"] = F
        fl, fs = F["for_letter"], F["for_state_exhaustive"]
        fsg = F["for_state_greedy"]; st = F["stirling"]
        print(f"الحقل المشترك 112: مواضع مرخَّصة {F['n_pos']:,} · أبجدية مرصودة {F['alphabet']}/112 | "
              f"H(مشترك)={F['H_joint']:.4f} · H(مشترك|سابق)={F['Hc_joint']:.4f} — ربح ON {F['H_joint'] - F['Hc_joint']:.4f} · خارج العيّنة {F['te_joint']:.4f}")
        print(f"عوامله: H(حالة)={F['H_state']:.4f} · H(حرف)={F['H_letter']:.4f} · H(حالة|حرف)={F['H_state_letter']:.4f} · H(حرف|حالة)={F['H_letter_state']:.4f}")
        print(f"FOR على الحرف (28→4) جشعًا: k={fl['k']} فاتورة {fl['invoice']:.1f} — ثمن التقسيم من ستيرلنج log2 S(28,{fl['k']})≈{fl['log2_S28k']} بت: " +
              " + ".join("".join(g) for g in fl["groups"]))
        print(f"FOR بالعكس على الحالة (4→28): استنفاد Bell(4)=15 كاملًا {fs['invoice']:.1f} ⟷ جشع {fsg['invoice']:.1f} (فارق {fsg['gap']:+.2f}) — حارسا العدّ متطابقان")
        print(f"ستيرلنج (ثمن المقسِّمات): log2 Bell(28)≈{st['log2_Bell28']} · log2 S(112,2)≈{st['log2_S112_2']} · log2 Bell(112)≈{st['log2_Bell112']} بت")
        RC = reconcile_counts(verses)
        OUT["مقيس"]["مصالحة_العد"] = RC
        d = RC["تفكيكه"]
        print(f"مصالحة العد بالحرف: {RC['إقفال']} — همزات مركبة {d['همزات_مركبة_أإؤئ']:,} + "
              f"زائدون {d['الزائدون_الأربعة_ىةآء']:,} − تنوينات خارج الإطار {-d['ناقص_تنوينات_خارج_الـ28']:,} | {RC['تحقق_إضافي']}")
    else:
        msg = "مجمَّد غائب — وضع بنيوي موسوم؛ ‎--require-corpus‎ يفشل هنا"
        OUT["مجمَّد"] = {"موجود": False}
        if args.require_corpus:
            raise SystemExit(msg)
        print(msg)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(OUT, fh, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {args.json}")

# (الفحص المشغَّل في ذيل الملف بعد كل التعريفات)

# ---------- ٧) الحقل المشترك 112: 28 حرفًا × 4 حالات مرخَّصة — ماركوف ON وFOR بالاتجاهين ----------
L28 = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
LIC4 = ("فتحة", "ضمة", "كسرة", "سكون")

def field112(verses, cross):
    """تيار (حرف، حالة) المشترك على خانات 28×4 المرخَّصة فقط — الزائدون خارج الإطار مسمَّون."""
    big, prv, prev_last, n_pos = Counter(), Counter(), None, 0
    for words in verses:
        seq = [(ch, st) for w in words for ch, st in w if ch in L28 and st in LIC4]
        n_pos += len(seq)
        edges = list(zip(seq, seq[1:]))
        if cross and prev_last is not None and seq:
            edges = [(prev_last, seq[0])] + edges
        for a, b in edges:
            big[(a, b)] += 1; prv[a] += 1
        if seq:
            prev_last = seq[-1]
    return big, prv, n_pos

def cond_entropy(big, prv, symbols):
    N = sum(big.values())
    return sum(prv[a] / N * (-sum(v / prv[a] * log2(v / prv[a])
             for (x, _), v in big.items() if x == a)) for a in symbols)

def stirling_row_n(n):
    """سطر ستيرلنج S(n,1..n) بالبرمجة الديناميكية — أعدادٌ صحيحة كبيرة بلا حدّ."""
    S = [[0] * (n + 2) for _ in range(n + 1)]
    S[0][0] = 1
    for i in range(1, n + 1):
        for k in range(1, i + 1):
            S[i][k] = k * S[i - 1][k] + S[i - 1][k - 1]
    return S[n]

def greedy_for(rows, n_out, map_bits):
    """الجشع على سطور عدّ مسبقة (سلف × ناتج) — الفاتورة بمتجهاتٍ لا بمسح الخام.
    map_bits(k): ثمن خريطة التقسيم بأجزاءٍ k — من ستيرلنج لا من الهوى."""
    def inv(groups):
        data = 0.0
        for g in groups:
            tot = sum(rows[s][o] for s in g for o in range(n_out))
            for o in range(n_out):
                c = sum(rows[s][o] for s in g)
                if c:
                    data += -c * log2((c + ALPHA) / (tot + ALPHA * n_out))
        return data + map_bits(len(groups)), data
    groups = [[s] for s in rows]
    cur, _ = inv(groups)
    path = []
    while True:
        best = (cur, None)
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                trial = [g for t, g in enumerate(groups) if t not in (i, j)] + [groups[i] + groups[j]]
                v, _ = inv(trial)
                if v < best[0] - 1e-9:
                    best = (v, trial)
        if best[1] is None:
            break
        groups, cur = best[1], best[0]
        path.append(len(groups))
    return groups, cur, path

def exhaust_for(rows, n_out, map_bits, symbols):
    """استنفاد كامل (لأبجديةٍ صغيرة) بحراسة ستيرلنج — يُصادَم بالجشع."""
    best = None
    for p in partitions(len(symbols)):
        assign = dict(zip(symbols, p))
        groups = [[s for s in symbols if assign[s] == r] for r in sorted(set(p))]
        data = 0.0
        for g in groups:
            tot = sum(rows[s][o] for s in g for o in range(n_out))
            for o in range(n_out):
                c = sum(rows[s][o] for s in g)
                if c:
                    data += -c * log2((c + ALPHA) / (tot + ALPHA * n_out))
        v = data + map_bits(len(groups))
        if best is None or v < best[0] - 1e-12:
            best = (v, groups)
    counts = Counter(len(set(p)) for p in partitions(len(symbols)))
    assert all(counts[k] == stirling(len(symbols), k) for k in counts), "حارس ستيرلنج صرخ"
    return best

def run_field112(verses):
    big, prv, n_pos = field112(verses, cross=True)
    alphabet = sorted(prv)
    assert len(alphabet) <= 112, "الحقل المشترك تجاوز 112 خانة — صريخ"
    pairs = [(a, b) for (a, b), v in big.items() for _ in range(v)]
    train, test = split_alternating(pairs)
    Ntr, Nte = len(train), len(test)
    tab, prv_t = Counter(train), Counter(a for a, _ in train)
    m = len(alphabet)
    N = sum(big.values())
    H_j = -sum(v / N * log2(v / N) for v in big.values())
    Hc_j = cond_entropy(tab, prv_t, alphabet)              # ON: زوجي مشترك ⟵ زوجي مشترك
    te_j = ce_table(tab, prv_t, test, m) / Nte
    # عوامل الحقل وشرطياته المتبادلة
    st_of, lt_of = Counter(), Counter()
    cells_sl = Counter(); cells_ls = Counter()             # (حرف، حالة-تالية) و (حالة، حرف-تالٍ)
    prv_sl = Counter(); prv_ls = Counter()
    for (a, b), v in big.items():
        st_of[b[1]] += v; lt_of[b[0]] += v
        cells_sl[(a[0], b[1])] += v; prv_sl[a[0]] += v
        cells_ls[(a[1], b[0])] += v; prv_ls[a[1]] += v
    H_st = -sum(v / N * log2(v / N) for v in st_of.values())
    H_lt = -sum(v / N * log2(v / N) for v in lt_of.values())
    H_st_lt = cond_entropy(cells_sl, prv_sl, L28)
    H_lt_st = cond_entropy(cells_ls, prv_ls, LIC4)
    # FOR على الحرف (28 سلفًا × 4 نتائج): جشع + ثمن ستيرلنج للتقسيم المختار
    rows_l = {ch: [cells_sl.get((ch, st), 0) for st in LIC4] for ch in L28}
    Ntr_sl = sum(prv_sl.values())
    s28 = stirling_row_n(28)
    gl, inv_gl, path_l = greedy_for(rows_l, 4, lambda k: float((s28[k] - 1).bit_length()) if s28[k] > 1 else 1.0)
    # FOR بالعكس على الحالة (4 سوابق × 28 نتيجة): استنفاد 15 كامل + جشع — يتصادمان
    rows_s = {st: [cells_ls.get((st, ch), 0) for ch in L28] for st in LIC4}
    s4 = {k: stirling(4, k) for k in range(1, 5)}
    inv_s_opt, groups_s_opt = exhaust_for(rows_s, 28, lambda k: float(s4[k].bit_length()), LIC4)
    gs, inv_gs, path_s = greedy_for(rows_s, 28, lambda k: float(s4[k].bit_length()))
    s112 = stirling_row_n(112)
    return dict(n_pos=n_pos, alphabet=m,
                H_joint=round(H_j, 4), Hc_joint=round(Hc_j, 4), te_joint=round(te_j, 4),
                H_state=round(H_st, 4), H_letter=round(H_lt, 4),
                H_state_letter=round(H_st_lt, 4), H_letter_state=round(H_lt_st, 4),
                for_letter=dict(k=len(gl), invoice=round(inv_gl, 1),
                                groups=[sorted(g) for g in gl],
                                log2_S28k=int(s28[len(gl)].bit_length()) - 1),
                for_state_exhaustive=dict(invoice=round(inv_s_opt, 1),
                                          groups=[sorted(g) for g in groups_s_opt]),
                for_state_greedy=dict(invoice=round(inv_gs, 1),
                                      gap=round(inv_gs - inv_s_opt, 2)),
                stirling=dict(S28_k2_k6={k: s28[k] for k in (2, 3, 4, 5, 6)},
                              log2_Bell28=int(sum(s28).bit_length()) - 1,
                              log2_S112_2=int((s112[2] - 1).bit_length()) - 1 if s112[2] > 1 else 0,
                              log2_Bell112=int(sum(s112).bit_length()) - 1))

# ---------- ٨) مصالحة العد بالحرف: إطار 28 المغلق مقابل الأبجد الخام ----------
HAMZA4 = list("أإؤئ")      # همزات مركبة — رسمًا خارج الـ28، صوتًا داخل المقام
EXTRA4 = list("ىةآء")      # الزائدون الأربعة مسمَّون بالورقة

def reconcile_counts(verses):
    """يُعيد اشتقاق 223,611 + 20,186 = 243,797 بالحرف — لا فرقَ مكتوم ولا عطلَ في عدّ.
    الفارق فرقُ تعريفٍ لا خطأ: إطار 28×4 المغلق (§8) مقابل الأبجد الخام (§17-18)."""
    cell = Counter()
    for words in verses:
        for w in words:
            for ch, st in w:
                cell[(ch, st)] += 1
    def tally(letters, states=None):
        return sum(v for (ch, st), v in cell.items()
                   if ch in letters and (states is None or st in states))
    field112 = tally(L28, LIC4)                       # المرخَّص في إطار 28×4
    hamza = tally(HAMZA4)                             # الهمزات المركبة بكل حالاتها
    extra = tally(EXTRA4) - tally(EXTRA4, ("عري",))   # الزائدون بغير العري
    tanwin_out = sum(v for (ch, st), v in cell.items()
                     if ch in HAMZA4 + EXTRA4 and "تنوين" in st)
    raw = tally(L28 + HAMZA4 + EXTRA4, LIC4)          # الأبجد الخام بالحالات المرخَّصة
    gap = hamza + extra - tanwin_out
    hamza_bare = tally(["ء"])
    assert field112 == 223611, f"الحقل 112 خُولف: {field112} — صريخ"
    assert raw == 243797, f"الأبجد الخام خُولف: {raw} — صريخ"
    assert field112 + gap == raw, f"المصالحة لم تُقفل: {field112}+{gap}≠{raw} — صريخ"
    assert hamza_bare == 1578, f"همزة hamil خُولفت: {hamza_bare} — صريخ"
    return {
        "الحقل112_المرخص": field112,
        "مرخص_الكل_بالأبجد_الخام": raw,
        "الفارق_الكامل": gap,
        "تفكيكه": {"همزات_مركبة_أإؤئ": hamza,
                   "الزائدون_الأربعة_ىةآء": extra,
                   "ناقص_تنوينات_خارج_الـ28": -tanwin_out},
        "إقفال": f"{field112:,} + {gap:,} = {raw:,} بالحرف",
        "تحقق_إضافي": f"ء وحدها = {hamza_bare:,} = همزة hamil المؤكدة بassert — تطابق مستقل",
        "فحوى": "لا عطل في أيّ عدّ — فرقُ تعريف الحقل: إطار 28 المغلق (§8) مقابل "
                "الأبجد الخام (§17-18)، و«الزائدون مسمَّون» بالورقة",
    }

if __name__ == "__main__":
    main()
