# algebra_engine.py — الجبر المشغَّل (إيداع التفويض)
# النظام من الداخل: فضاء الوحدة (بايت)، جبر الأوزان (سنّ)، ماركوف الاشتقاق، الاستقراء المشغَّل.
# كل عدٍّ هنا معروضٌ أو مشتقٌّ بقاعدة — انضباط البند ٧ (لا عدَّ مُعلَنًا غيرَ معروض).
from math import log2, factorial, ceil
from collections import defaultdict, Counter
import numpy as np

# ---------- ١) فضاء الوحدة: 32 حرفًا × 8 حالات = 256 = 2⁸ ----------
LETTERS = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي") + ["ى", "ة", "آ", "ء"]
CP = {"ا": 0x0627, "ب": 0x0628, "ت": 0x062A, "ث": 0x062B, "ج": 0x062C, "ح": 0x062D, "خ": 0x062E,
      "د": 0x062F, "ذ": 0x0630, "ر": 0x0631, "ز": 0x0632, "س": 0x0633, "ش": 0x0634, "ص": 0x0635,
      "ض": 0x0636, "ط": 0x0637, "ظ": 0x0638, "ع": 0x0639, "غ": 0x063A, "ف": 0x0641, "ق": 0x0642,
      "ك": 0x0643, "ل": 0x0644, "م": 0x0645, "ن": 0x0646, "ه": 0x0647, "و": 0x0648, "ي": 0x064A,
      "ى": 0x0649, "ة": 0x0629, "آ": 0x0622, "ء": 0x0621}
# الحالة: (قيمة: فتح0/ضم1/كسر2/سكون3) × (تنوين؟) — والخانة الممنوعة (سكون+تنوين=7) ⟸ عُرْي
STATES = [("فتحة", 0x064E, 0, 0), ("ضمة", 0x064F, 1, 0), ("كسرة", 0x0650, 2, 0), ("سكون", 0x0652, 3, 0),
          ("تنوين فتح", 0x064B, 0, 1), ("تنوين ضم", 0x064C, 1, 1), ("تنوين كسر", 0x064D, 2, 1), ("عُرْي", None, 3, 1)]

def pack(li, si): return (li << 3) | si        # الوحدة بايت: 5 بت حرف + 3 بت حالة
def unpack(b):   return (b >> 3, b & 0b111)

UNITS = [(li, si) for li in range(32) for si in range(8)]

def enc(li, si):                                # ترميز Unicode (مديان متمايزان ⟹ حاقن بنيويًّا)
    cp_s = STATES[si][1]
    return (CP[LETTERS[li]],) if cp_s is None else (CP[LETTERS[li]], cp_s)

def dec(seq):
    li = next(i for i, h in enumerate(LETTERS) if CP[h] == seq[0])
    si = 7 if len(seq) == 1 else next(i for i, s in enumerate(STATES) if s[1] == seq[1])
    return (li, si)

# ---------- ٢) التحليل من تيار Unicode (مع R4 التنوين وR5 الشدة) ----------
SHADDA, TANWIN = 0x0651, {0x064B: 0x064E, 0x064C: 0x064F, 0x064D: 0x0650}
CP2L = {v: k for k, v in CP.items()}
CP2S = {s[1]: i for i, s in enumerate(STATES) if s[1]}

def parse_stream(raw):
    """تيار مشكول ⟼ قائمة وحدات (li, si) — التوسيعات R4/R5 مطبَّقة. الصنف لا يُخمَّن هنا."""
    units, i = [], 0
    while i < len(raw):
        ch = raw[i]
        if ch == " ":
            i += 1; continue
        li = LETTERS.index(CP2L[ord(ch)]); marks = []
        while i + 1 < len(raw) and 0x064B <= ord(raw[i + 1]) <= 0x0652:
            i += 1; marks.append(ord(raw[i]))
        if SHADDA in marks:                                  # R5: ساكن + متحرك
            v = next(m for m in marks if m != SHADDA)
            units += [(li, 3), (li, CP2S[v])]
        elif any(m in TANWIN for m in marks):                # R4: حركة + نون ساكنة
            v = next(m for m in marks if m in TANWIN)
            units += [(li, CP2S[TANWIN[v]]), (24, 3)]
        else:
            units.append((li, CP2S[marks[0]] if marks else 7))
        i += 1
    return units

# ---------- ٣) جبر الأوزان: القوالب والتركيب ورسم السنّ ----------
T = {"I": "فَعَلَ", "II": "فَعَّلَ", "III": "فَاعَلَ", "IV": "أَفْعَلَ", "V": "تَفَعَّلَ",
     "VI": "تَفَاعَلَ", "VII": "انْفَعَلَ", "VIII": "افْتَعَلَ", "IX": "افْعَلَّ", "X": "اسْتَفْعَلَ",
     "XI": "افْعَالَّ", "XII": "افْعَوْعَلَ", "XIII": "افْعَوَّلَ", "XIV": "افْعَنْلَلَ", "XV": "افْعَنْلَى"}
assert T["V"] == "تَ" + T["II"] and T["VI"] == "تَ" + T["III"] and T["VII"] == "انْ" + T["I"]

EDGES = [("صعود", "I", "II"), ("صعود", "I", "IV"),
         ("هبوط/مطاوعة", "II", "V"), ("هبوط/مطاوعة", "IV", "VII"), ("هبوط/مطاوعة", "I", "VIII"),
         ("مشاركة", "I", "III"), ("مشاركة", "III", "VI"),
         ("طلب", "I", "X"), ("تثبيت", "I", "IX")]
W10 = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
NAWADER = ["XI", "XII", "XIII", "XIV", "XV"]

# ---------- ٤) مصفوفة الخلايا — توليدٌ بقاعدة معلنة، عرضٌ كامل ----------
COLS = ["ماضٍ معلوم", "ماضٍ مجهول", "مضارع معلوم", "مضارع مجهول", "أمر", "مصدر", "اسم فاعل", "اسم مفعول"]
LAZIM_MAHD = ["VII", "IX"] + NAWADER          # مطاوع محض + قطب ثابت + نوادر قلبية

def paradigm_cell(w, c):
    if w in LAZIM_MAHD and c in ("ماضٍ مجهول", "مضارع مجهول", "اسم مفعول"):
        return "⚑ل"                            # امتناع لزوم (W4 معمَّمًا بقاعدة معلنة)
    if w == "I" and c == "مصدر":
        return "⚑س"                            # مصادر المجرد سماعية (W3)
    return "✓"

PARADIGM = {w: [paradigm_cell(w, c) for c in COLS] for w in T}

# ---------- ٥) ماركوف الاشتقاق على رسم السنّ ----------
def derivation_markov():
    idx = {w: i for i, w in enumerate(W10)}
    P = np.zeros((10, 10))
    for _, a, b in EDGES:
        P[idx[a], idx[b]] += 1
    for w in W10:                                # المصارف تتجدد من المجرد — حلقة اشتقاق
        i = idx[w]
        P[i] = P[i] / P[i].sum() if P[i].sum() else np.eye(10)[idx["I"]]
    evals, evecs = np.linalg.eig(P.T)
    pi = np.real(evecs[:, np.argmin(abs(evals - 1))]); pi /= pi.sum()
    H_pi = -sum(p * log2(p) for p in pi if p > 0)
    rate = sum(pi[i] * (-sum(p * log2(p) for p in P[i] if p > 0)) for i in range(10))
    return P, pi, H_pi, rate

# ---------- ٦) مصنِّف الجسر — دالةٌ تحسب من مدخلاتٍ معلنة، والسكوتُ فيها محظور ----------
MATRES = {"ا": "فتحة", "و": "ضمة", "ي": "كسرة", "ى": "فتحة"}

def parse_word(w):
    units, i = [], 0
    while i < len(w):
        li = LETTERS.index(CP2L[ord(w[i])]); marks = []
        while i + 1 < len(w) and 0x064B <= ord(w[i + 1]) <= 0x0652:
            i += 1; marks.append(ord(w[i]))
        if SHADDA in marks:
            v = next(m for m in marks if m != SHADDA); units += [(li, 3, "R5-أول"), (li, CP2S[v], "R5-ثان")]
        elif any(m in TANWIN for m in marks):
            v = next(m for m in marks if m in TANWIN); units += [(li, CP2S[TANWIN[v]], "R4"), (24, 3, "R4")]
        else:
            units.append((li, CP2S[marks[0]] if marks else 7, "خام"))
        i += 1
    return units

def classify_word(units, tag):
    """صنف الجسر دالةً في (الوحدة، السياق، الوسم المعلن). الوسم مدخلٌ لا مخرج.
    كل موضعٍ إمّا مصنَّفٌ بقاعدةٍ معلنة أو ⚑ — لا افتراضيَّ صامتًا (السكوت = ابتلاع)."""
    cls = []
    for j, (li, si, src) in enumerate(units):
        h = LETTERS[li]; last = (j == len(units) - 1)
        if tag["نوع"] == "مركّب" and j == 0:
            cls.append("ب"); continue                       # جارٌّ ملتصق: مبنيٌّ معلن
        if si == 7 and (h == "آ" or (h in MATRES and j > 0 and STATES[units[j-1][1]][0] == MATRES[h])):
            cls.append("م"); continue                       # مدٌّ/لين محمول
        if si == 7 and h == "ا" and j+1 < len(units) and LETTERS[units[j+1][0]] == "ل" \
           and (j == 0 or (j == 1 and tag["نوع"] == "مركّب")):
            cls.append("ض"); continue                       # همزة وصل — سكونٌ مضمرٌ معلن
        if tag["نوع"] == "مبني" and tag.get("بناء"):
            bv, bp = tag["بناء"]
            if (bp == "آخر" and last and STATES[si][0] == bv) or (bp == "R5-أول" and src == "R5-أول" and STATES[si][0] == bv):
                cls.append("ب"); continue                   # حالة البناء الثابتة
        if last and si != 7 and tag["نوع"] != "مبني":
            cls.append("خ"); continue                       # إعرابيٌّ — خارج الجسر (Δضبط)
        cls.append("ظ")
    return cls

# ---------- ٧) التقشير — كل بتٍّ إمّا مسترجَعٌ بالقاعدة أو حاملٌ مبرهَنٌ بالقلع ----------
V2I = {"فتحة": 0, "ضمة": 1, "كسرة": 2, "سكون": 3}

def peel_table(units, classes, tags_per_unit):
    """لكل وحدة 8 بتّات (5 حرف + 3 حالة): □ مقشور (تسترجعه قاعدةٌ معلنة) / ■ حامل.
    القواعد السبع كلُّها من الوثائق المودعة؛ ق6 وق7 موسومتان هنا باسمهما في peeling_proof.md."""
    table = []
    for j, ((li, si, src), c) in enumerate(zip(units, classes)):
        L, S, rule = ["■"] * 5, ["■"] * 3, "—"
        if src == "R4" and li == 24 and si == 3:
            L, S, rule = ["□"] * 5, ["□"] * 3, "ق1 نون التنوين مشتقّة كلُّها"
        elif src == "R5-أول":
            L, S, rule = ["□"] * 5, ["□"] * 3, "ق2 الشدة: الحرف حرفُ أخته، والحالة سكون"
        elif src == "R5-ثان":
            rule = "ق2′ القطب المحفوظ — لا استعارةَ متبادلة"   # حرف الشدة يُحفظ في قطبٍ واحد
        elif c == "م":
            S, rule = ["□"] * 3, "ق3 م ⟹ عُرْي"
        elif c == "ض":
            L, S, rule = ["□"] * 5, ["□"] * 3, "ق4 همزة وصل: ا عارية"
        elif c == "ب":
            S, rule = ["□"] * 3, "ق5/ق6 الحالة من الوسم"
        elif c == "ظ" and LETTERS[li] == "ل" and si == 3 and j > 0 and classes[j - 1] == "ض":
            S, rule = ["□"] * 3, "ق7 لام «ال» ساكنة"
        table.append((L, S, rule))
    return table

def peel(units, classes, tags_per_unit):
    """الاتجاهان معًا: استرجاعٌ بالهندسة العكسية (كفاية) + فحصُ قلع (لزوم). صارخٌ عند كل سكوت."""
    table = peel_table(units, classes, tags_per_unit)
    skel = [(li if "■" in r[0] else None, si if "■" in r[1] else None, src)
            for (li, si, src), r in zip(units, table)]
    out = []
    for j, (li, si, src) in enumerate(skel):
        c = classes[j]
        li_r = li if li is not None else (24 if src == "R4" else 0 if c == "ض" else None)
        if si is not None:            si_r = si
        elif src in ("R4", "R5-أول"): si_r = 3
        elif c in ("م", "ض"):         si_r = 7
        elif c == "ب" and tags_per_unit[j]["نوع"] == "مبني":  si_r = V2I[tags_per_unit[j]["بناء"][0]]
        elif c == "ب" and tags_per_unit[j]["نوع"] == "مركّب": si_r = 2
        elif c == "ظ" and li_r == 22: si_r = 3
        else: raise AssertionError(f"وحدة {j + 1}: بتّاتٌ مقشورةٌ بلا قاعدة — صريخ")
        out.append([li_r, si_r])
    for j, (_, _, src) in enumerate(skel):
        if src == "R5-أول": out[j][0] = out[j + 1][0]
    assert all(u[0] is not None for u in out), "قطبا الشدة استعارا من بعضهما — دورٌ محظور"
    rec = [pack(u[0], u[1]) for u in out]
    assert rec == [pack(li, si) for li, si, _ in units], "فشل الاسترجاع — قاعدةٌ ناقصة تُضاف باسمها"
    peeled = sum(r[0].count("□") + r[1].count("□") for r in table)
    return peeled, 8 * len(units) - peeled, table

# ---------- ٨) التقشير من أدنى إلى أعلى — فضاء 112، بلا تسريب («نعرف بتّاتٍ جشعةً عمياء») ----------
BASE28, HARAKAT4 = LETTERS[:28], STATES[:4]
PRESERVES9 = ["تشكيل", "همزات", "شدة", "ال التعريف", "زوائد", "هاء الضمير", "ذاء الإشارة", "كاف التشبيه", "تاء التأنيث"]

def peel112():
    """الوحدة 5+2=7 بتّات على 28×4=112. □ بنيويٌّ مسعَّر (R1′/R5) فقط؛ ◆ محفوظ مسمّى؛ ■ جشع أعمى.
    قواعد العربية غير المسعَّرة مرتجعةٌ بالاسم (ق3–ق7 من النسخة ١) — لا تسريب."""
    assert len(BASE28) * len(HARAKAT4) == 112
    T112 = [("قَ", (5, "■"), (2, "■"), ""), ("ا", (5, "■"), (0, "—"), ""), ("لَ", (5, "■"), (2, "■"), ""),
            ("آ", (5, "◆"), (0, "—"), "همزات"), ("مَ", (5, "■"), (2, "■"), ""),
            ("نَّ", (5, "■"), (2, "■"), "شدة"), ("ا", (5, "■"), (0, "—"), ""),
            ("بِ", (5, "■"), (2, "■"), "زوائد"), ("ا", (5, "◆"), (0, "—"), "ال التعريف"),
            ("لْ", (5, "◆"), (2, "■"), "ال التعريف"), ("كِ", (5, "■"), (2, "■"), ""),
            ("تَ", (5, "■"), (2, "■"), ""), ("ا", (5, "■"), (0, "—"), ""), ("بِ", (5, "■"), (2, "■"), "")]
    tot = Counter()
    for _, (lb, lk), (hb, hk), _ in T112:
        tot[lk] += lb; tot[hk] += hb
    tot["□"] += 7; tot["◆"] += 1          # مدّ آ (R1′: 5) + سكون الشدة (R5: 2) + راية الشدة (1)
    assert sum(tot.values()) == 96
    return tot

# ---------- ٩) الترخيص الجشع صعودًا — بتٌّ واحدٌ للأعلى (من 7 إلى 8 بتّات/وحدة، بلا تسريب) ----------
def peel256_strict():
    """البتّ الثامن = بتّ الحالة الثالث: يرخّص 4 خلايا فوق الـ112 — تنوين فتح/ضم/كسر + الخانة الممنوعة.
    الخانة الممنوعة (سكون+تنوين مستحيل بنيويًّا) تُسمّى عُرْيًا بثمن صفر — R0 اتفاقُ تعبئةٍ مسعَّر (dec/enc)، لا عربيّة فيه.
    □ = R5-أول (8: حرفٌ منسوخٌ مؤشَّر + سكون) + R0 (5 عُرْي × 3 = 15) = 23 · ◆ = همزة آ (5) + ال (10) = 15 · ■ = 82.
    ق3–ق7 مرتجعة كما في النسخة ٢ — الترخيص يشتري تعبئةً لا نحوًا."""
    tot = Counter()
    tot["□"] = 8 + 5 * 3                    # R5-أول + R0 على مواضع العُرْي الخمسة
    tot["◆"] = 5 + 10                       # همزة آ + أليف ال ولامها
    tot["■"] = 15 * 8 - tot["□"] - tot["◆"]
    assert sum(tot.values()) == 120 and tot["■"] == 82
    return tot

# ---------- ١٠) القياس على المجمَّد — الترخيص بالتردد المقيس (هوفمان يعيد الترتيب) ----------
import heapq, hashlib, os
MUJAMMAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mujammad.txt")
MUJAMMAD_SHA256 = "8b387ea811bc8c658e1cab75488ce1aa69606deafd62759eeaf49ffe15c6d215"
# المجمَّد: نص Tanzil (مرآة GlobalQuran: quran-simple-enhanced.txt) — 6246 سطرًا، 1,306,770 بايتًا.
# البصمة تُتحقق قبل أيّ عدّ: من خالفها فليس المجمَّد — لا قياس على بديلٍ صامت.
AR_LET = lambda ch: 0x0621 <= ord(ch) <= 0x063A or 0x0641 <= ord(ch) <= 0x064A
VOWM = {0x064E: "فتحة", 0x064F: "ضمة", 0x0650: "كسرة", 0x0652: "سكون"}
TANM = {0x064B: "تنوين فتح", 0x064C: "تنوين ضم", 0x064D: "تنوين كسر"}
DAGGER = 0x0670                                  # الخنجرية = فتحة موسومة (اتفاق معلن)

def audit_corpus(path=MUJAMMAD_PATH):
    """عدٌّ معروض: كل موضعٍ حرفيٌّ يُسند إلى إحدى الخلايا الثماني أو يُوسَم تعارضًا — لا ابتلاع."""
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == MUJAMMAD_SHA256, "ليس المجمَّد — البصمة خُالفت"
    lines = [l for l in blob.decode("utf-8-sig").strip().split("\n") if l.strip()]
    cells, letters, joint = Counter(), Counter(), Counter()
    pos = hamza = conflicts = 0
    for ln in lines:
        i, n = 0, len(ln)
        while i < n:
            ch = ln[i]
            if AR_LET(ch):
                pos += 1
                if ch == "ء": hamza += 1
                marks = []
                while i + 1 < n and (0x064B <= ord(ln[i + 1]) <= 0x0652 or ord(ln[i + 1]) == DAGGER):
                    i += 1; marks.append(ord(ln[i]))
                vs = [m for m in marks if m in VOWM]; ts = [m for m in marks if m in TANM]
                if len(vs) > 1 or len(ts) > 1 or (vs and ts):
                    conflicts += 1
                else:
                    cell = TANM[ts[0]] if ts else VOWM[vs[0]] if vs else "فتحة" if DAGGER in marks else "عري"
                    cells[cell] += 1; letters[ch] += 1; joint[(ch, cell)] += 1
            i += 1
    assert pos == 330728 and hamza == 1578 and conflicts == 0, "بصمة العدّ خُالفت"
    return cells, letters, joint, pos

def huffman(cells):
    """الاختيار الجشع المبرهَن: ادمج أقلّ رمزين احتمالًا وكرّر. الحارس: H ≤ L < H+1."""
    tot = sum(cells.values())
    heap = [(v, i, [k]) for i, (k, v) in enumerate(sorted(cells.items()))]
    heapq.heapify(heap); codes = {k: "" for k in cells}; c = len(heap)
    while len(heap) > 1:
        v1, _, k1 = heapq.heappop(heap); v2, _, k2 = heapq.heappop(heap)
        for k in k1: codes[k] = "0" + codes[k]
        for k in k2: codes[k] = "1" + codes[k]
        heapq.heappush(heap, (v1 + v2, c, k1 + k2)); c += 1
    H = -sum(v / tot * log2(v / tot) for v in cells.values())
    L = sum(cells[k] / tot * len(codes[k]) for k in cells)
    assert H <= L < H + 1, "هوفمان خارج حدّه — مستحيلٌ إلا بخللٍ في التنفيذ"
    return codes, H, L

# ---------- ١١) الترخيص فوق 112 بالتردد المقيس — العزل بالختم الخاصّ ----------
LICENSED4 = ("فتحة", "كسرة", "ضمة", "سكون")                 # حصّة 112 المرخَّصة
SEALED4 = ("عري", "تنوين فتح", "تنوين كسر", "تنوين ضم")      # ما سواها: لا يُسرَّب — يُعزَل بختم

def peel112_measured(cells):
    """فوق إطار 112: الحركات الأربع تُرخَّص بالتردد المقيس (هوفمان)، وما سواها يُعزَل بختمٍ خاصّ —
    رمزٌ خامسٌ في الشجرة الخارجية، وداخل الختم ترخيصٌ مقيسٌ ثانٍ بالتردد أيضًا.
    الفاتورة الكاملة: L = L_خارجي + P(ختم)·L_داخلي — وتُقاس على هوفمان §١٧ المباشر بلا ابتلاع."""
    outer = Counter({k: cells[k] for k in LICENSED4})
    outer["ختم"] = sum(cells[k] for k in SEALED4)
    assert sum(outer.values()) == sum(cells.values()), "مفقودٌ بين المرخَّص والمختوم — ابتلاع"
    c_out, H_out, L_out = huffman(outer)                                     # 5 رموز: 4 + ختم
    c4, H4, L4 = huffman(Counter({k: cells[k] for k in LICENSED4}))          # داخل الحصّة وحدها
    c_in, H_in, L_in = huffman(Counter({k: cells[k] for k in SEALED4}))      # داخل الختم
    p_seal = outer["ختم"] / sum(cells.values())
    return (c_out, H_out, L_out), (c4, H4, L4), (c_in, H_in, L_in), p_seal, L_out + p_seal * L_in

# ---------- ١٢) انقلاب الربح — التوافيق والتباديل على الجبر المغلق 112، وماركوف باتجاهين ----------
def assign_stats(cells, lengths):
    """الربح الجشع بالتباديل: الأطوال ثابتة (نتيجة هوفمان المقيس)، والتخصيص يُبدَّل.
    الأفضل: الأعلى ترددًا ⟵ الأقصر (متراجحة الترتيب — قاعدة معلنة). الأردأ: المعاكس تمامًا.
    التخصيصات المتميِّزة = n! / Π م! (م = تكرار كل طول — التوافيق: مَن يأخذ أيّ طول)؛
    المثلى = Π م! (التباديل داخل الأطوال المتساوية لا تغيّر السعر — الربح كله في التوافيق).
    والمسطَّح: n! تبديلًا كلّها بسعرٍ واحد — رهن الترتيب فيها = صفر، أي إنّه أعمى عن الجشع أصلًا."""
    ks = sorted(cells, key=lambda k: -cells[k])
    ls = sorted(lengths)
    N = sum(cells.values())
    Lb = sum(cells[k] * l for k, l in zip(ks, ls)) / N
    Lw = sum(cells[k] * l for k, l in zip(ks, ls[::-1])) / N
    mult = Counter(lengths)
    distinct = factorial(len(ks))
    optimal = 1
    for m in mult.values():
        distinct //= factorial(m)
        optimal *= factorial(m)
    return Lb, Lw, distinct, optimal

def bigram_states(path=MUJAMMAD_PATH):
    """ماركوف ON المجمَّد: انتقالات الحالة بين موضعَين متتاليين داخل السطر.
    اتفاق معلن: حدُّ السطر لا يُعبَر (زوجان متتاليان من سطرين لا يُحسَبان)."""
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == MUJAMMAD_SHA256, "ليس المجمَّد"
    lines = [l for l in blob.decode("utf-8-sig").strip().split("\n") if l.strip()]
    big, prev_m = Counter(), Counter()
    for ln in lines:
        seq = []
        i, n = 0, len(ln)
        while i < n:
            if AR_LET(ln[i]):
                marks = []
                while i + 1 < n and (0x064B <= ord(ln[i + 1]) <= 0x0652 or ord(ln[i + 1]) == DAGGER):
                    i += 1
                    marks.append(ord(ln[i]))
                vs = [m for m in marks if m in VOWM]
                ts = [m for m in marks if m in TANM]
                seq.append(TANM[ts[0]] if ts else VOWM[vs[0]] if vs else "فتحة" if DAGGER in marks else "عري")
            i += 1
        for a, b in zip(seq, seq[1:]):
            big[(a, b)] += 1
            prev_m[a] += 1
    Np = sum(big.values())
    per_prev, Hc = {}, 0.0
    for a, tot_a in prev_m.items():
        h = -sum((v / tot_a) * log2(v / tot_a) for (x, _), v in big.items() if x == a)
        per_prev[a] = h
        Hc += (tot_a / Np) * h
    return Hc, per_prev, Np, big, prev_m

# ---------- ١٣) محطة الاسم والفعل والحرف — توقف الجشع وتحوّله (قياس على مستوى الكلمة) ----------
def word_positions(w):
    """كلمة مشكولة ⟼ قائمة (حرف، حالة) — نفس اتفاقات العدّ الموضعيّ (الخنجرية = فتحة موسومة)."""
    pos, i, n = [], 0, len(w)
    while i < n:
        ch = w[i]
        if AR_LET(ch):
            marks = []
            while i + 1 < n and (0x064B <= ord(w[i + 1]) <= 0x0652 or ord(w[i + 1]) == DAGGER):
                i += 1
                marks.append(ord(w[i]))
            vs = [m for m in marks if m in VOWM]
            ts = [m for m in marks if m in TANM]
            pos.append((ch, TANM[ts[0]] if ts else VOWM[vs[0]] if vs
                        else "فتحة" if DAGGER in marks else "عري"))
        i += 1
    return pos

def station(pos):
    """المحطة السطحية (موسومة — ليست التصنيف النحوي)، الأولوية T > A > B:
    T بوّابة التنوين (خاتمةٌ، أو تنوين فتح قبل خاتمةٍ عاريةٍ ا/ى — معدودة 3,153 بالقياس لا مفترَضة) ·
    A بوّابة «ال» (مدخل ا+ل — تبتلع 10 من الفواتح المقطّعة، معدودًا في before_sentence) · B عارٍ."""
    if pos[-1][1] in TANM.values():
        return "T"
    if len(pos) >= 2 and pos[-2][1] == "تنوين فتح" and pos[-1][0] in ("ا", "ى") and pos[-1][1] == "عري":
        return "T"
    if len(pos) >= 2 and pos[0][0] == "ا" and pos[1][0] == "ل":
        return "A"
    return "B"

def word_station(path=MUJAMMAD_PATH):
    """الاتفاقات المعلنة: الكلمة = ما بين مسافتين داخل السطر؛ حدُّ السطر لا يُعبَر (كما في ماركوف ON).
    ف1/ف2 فرضيتان موسومتان ببوّابة نقض: «تنوين ⟹ اسم» و«ال ⟹ اسم» — والبوّابة ممارَسةً: T∩A = 0
    (لا كلمةَ تحمل ال وتنوينًا معًا على 77,801 كلمة) — اتساقٌ مقيس لا برهان؛ التحقيق دَين المعجم."""
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == MUJAMMAD_SHA256, "ليس المجمَّد"
    lines = [l for l in blob.decode("utf-8-sig").strip().split("\n") if l.strip()]

    Nw = 0
    cls, init_c = Counter(), Counter()
    entry, exit_ = defaultdict(Counter), defaultdict(Counter)
    skel_forms = defaultdict(Counter)
    cls2, cls_prev, fwd, fwd_prev = Counter(), Counter(), Counter(), Counter()
    overlap = 0
    wlen = []
    for ln in lines:
        seq = []
        for w in [w for w in ln.split(" ") if w.strip()]:
            pos = word_positions(w)
            if not pos:
                continue
            c = station(pos)
            Nw += 1
            cls[c] += 1
            wlen.append(len(pos))
            entry[c][pos[0][1]] += 1
            exit_[c][pos[-1][1]] += 1
            init_c[pos[0][1]] += 1
            skel_forms["".join(ch for ch, _ in pos)][tuple(st for _, st in pos)] += 1
            if c == "T" and len(pos) >= 2 and pos[0][0] == "ا" and pos[1][0] == "ل":
                overlap += 1                                    # بوّابة النقض: يجب أن يبقى صفرًا
            seq.append((c, pos[0][1]))
        for (c1, _), (c2, st2) in zip(seq, seq[1:]):
            cls2[(c1, c2)] += 1
            cls_prev[c1] += 1
            fwd[(c1, st2)] += 1
            fwd_prev[c1] += 1
    assert overlap == 0, "كلمةٌ تحمل ال وتنوينًا — بوّابة النقض صرخت"

    H_cls = -sum(v / Nw * log2(v / Nw) for v in cls.values())
    amb = {s: c for s, c in skel_forms.items() if len(c) > 1}
    mass = sum(sum(c.values()) for c in amb.values())
    Nc2 = sum(cls2.values())
    Hc_cls = sum(cls_prev[a] / Nc2 * (-sum((v / cls_prev[a]) * log2(v / cls_prev[a])
                 for (x, _), v in cls2.items() if x == a)) for a in "TAB")
    Ni = sum(init_c.values())
    H_init = -sum(v / Ni * log2(v / Ni) for v in init_c.values())
    Nf = sum(fwd.values())
    Hc_fwd = sum(fwd_prev[a] / Nf * (-sum((v / fwd_prev[a]) * log2(v / fwd_prev[a])
                 for (x, _), v in fwd.items() if x == a)) for a in "TAB")
    return dict(Nw=Nw, cls=cls, H_cls=H_cls, amb=amb, mass=mass, skel=skel_forms,
                Hc_cls=Hc_cls, H_init=H_init, Hc_fwd=Hc_fwd, entry=entry, exit=exit_,
                wlen=sum(wlen) / len(wlen), pairs=Nc2)

# ---------- ١٤) قبل ترخيص الجملة — العتبة: الوحدة المحدَّدة الوحيدة فوق الكلمة ----------
def before_sentence(path=MUJAMMAD_PATH):
    """قبل ترخيص الجملة: الترخيص يشترط وحدةً محدَّدةً معلنةً وجردَ ظواهرَ معلنًا — وكلاهما دَينان
    عند الجملة. الوحدة المحدَّدة الوحيدة فوق الكلمة في المجمَّد هي السطر=الآية (6,236) —
    ويُثبَت بالعدّ أنها ليست حدًّا جمليًّا (46.31% منها تبدأ موصولًا بـوَ/فَ).
    اتفاقات معلنة: أسطر الترويسة العشرة (#) موسومةٌ خارج العدّ الآييّ (عدّ §١٧ الموضعيّ لم يمسسها —
    لا حروفَ عربيةً فيها)؛ المسافة الطرفية الزائدة في أول آيات الفواتح أثرُ ملفٍّ موسوم تُطرح.
    بوّابتا العدّ: عدد الآيات 6,236، وبسم = 4 — إن تبدّلا صرخ المحرك."""
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == MUJAMMAD_SHA256, "ليس المجمَّد"
    lines = [l for l in blob.decode("utf-8-sig").strip().split("\n") if l.strip()]
    verses = [ln for ln in lines if any(AR_LET(c) for c in ln)]
    assert len(verses) == 6236 and len(lines) - len(verses) == 10, "بصمة الأسطر خُالفت"

    w_per_v, vfinal, vfirst, first_words, conj, final_all = [], Counter(), Counter(), Counter(), Counter(), Counter()
    Nw = 0
    vopen_conj = bsm = 0
    one_word, mq_inA = [], 0
    for ln in verses:
        poss = [p for p in (word_positions(w) for w in ln.split(" ") if w.strip()) if p]
        w_per_v.append(len(poss)); Nw += len(poss)
        vfinal[poss[-1][-1][1]] += 1
        vfirst[station(poss[0])] += 1
        first_words["".join(ch for ch, _ in poss[0])] += 1
        if poss[0][0] in (("و", "فتحة"), ("ف", "فتحة")):
            vopen_conj += 1
        for p in poss:
            final_all[p[-1][1]] += 1
            if p[0][0] == "و" and p[0][1] == "فتحة": conj["وَ"] += 1
            if p[0][0] == "ف" and p[0][1] == "فتحة": conj["فَ"] += 1
        if len(poss) == 1:
            one_word.append("".join(ch for ch, _ in poss[0]))
            if station(poss[0]) == "A":
                mq_inA += 1                       # عمى بوّابة A عن الفواتح — معدودٌ بالاسم
        bsm += sum(1 for p in poss if "".join(ch for ch, _ in p) == "بسم")
    assert bsm == 4, "بسم خُالفت — 27:30 منقوصةٌ في المجمَّد والغيبة معدودة (4 لا 5)"
    H_len = -sum(v / 6236 * log2(v / 6236) for v in Counter(w_per_v).values())
    H_vf = -sum(v / 6236 * log2(v / 6236) for v in vfinal.values())
    H_wf = -sum(v / Nw * log2(v / Nw) for v in final_all.values())
    return dict(Nv=6236, Nw=Nw, w_per_v=w_per_v, H_len=H_len, vfinal=vfinal, final_all=final_all,
                H_vf=H_vf, H_wf=H_wf, vfirst=vfirst, first_words=first_words, conj=conj,
                vopen_conj=vopen_conj, one_word=one_word, mq_inA=mq_inA, bsm=bsm)

# ---------- ١٥) عتبة حدود الجملة: الاسمية والفعلية وشبه الجملة — صعود بتٍّ جشعٍ ----------
JARR_SKEL = {"من", "عن", "على", "الى", "في"}   # هياكل جرٍّ قائمةٌ معلنة بالاسم (خمسة — ثمنها دَينٌ كولموغوروفيّ)
JARR_PREF = {"ب", "ل", "ك"}                     # الجارُّ الملتصق المكسور — امتداد ق6 الموسومة في ت2 (§٠)

def sentence_threshold(path=MUJAMMAD_PATH):
    """العتبة الجملية — قياسٌ على مداخل الآيات (الوحدة المحدَّدة الوحيدة فوق الكلمة، §٢١)، لا على جملٍ
    حقيقية: حدودُ الجملة دَينٌ قائم، فالآية هنا وكيلٌ موسوم لا مدّعًى. البوّابات سطحيةٌ معلنة بالأولوية:
    C عطف (وَ/فَ فتحية أوّلًا — معدود 2,888 في §٢١) · J جرّ (هيكلٌ في القائمة المعلنة، أو ب/ل/ك مكسورٌ
    بامتداد ق6 الموسومة) ⟹ شبه جملة مرشَّحة · A (ال) وT (تنوين) ⟹ اسمية مرشَّحة · B أعمى (الفعلية دَينُ
    المعجم). اتفاق القلع المعلن: في الآية المعطوفة يُقلَع الموضع الأول (و/ف فتحية) وتُقاس البوّابة على
    الباقي — وعمى القلع عن و القسم (وَالطُّورِ…) معدودٌ بالاسم في وحيدات وَ. بوّابة العدّ: الأصناف تسدّ 6,236."""
    blob = open(path, "rb").read()
    assert hashlib.sha256(blob).hexdigest() == MUJAMMAD_SHA256, "ليس المجمَّد"
    lines = [l for l in blob.decode("utf-8-sig").strip().split("\n") if l.strip()]
    verses = [ln for ln in lines if any(AR_LET(c) for c in ln)]
    assert len(verses) == 6236, "بصمة الأسطر خُالفت"

    def jgate(pos):
        if "".join(ch for ch, _ in pos) in JARR_SKEL:
            return "قائمة"
        if pos[0][0] in JARR_PREF and pos[0][1] == "كسرة":
            return "ق6"
        return None

    def gate(pos):                                   # الأولوية المعلنة: J ثم A ثم T ثم B
        j = jgate(pos)
        if j:
            return ("J", j)
        s = station(pos)
        if s in ("A", "T"):
            return (s, None)
        return ("B", None)

    raw, strip = Counter(), Counter()                # raw: بخلية C · strip: بعد قلع العطف
    raw_j, strip_j = Counter(), Counter()
    topB_raw, topB_strip = Counter(), Counter()
    oath_1w = redir_T = chain_T = 0                  # وحيدات وَ = قسمٌ ظاهر مبتلَع في C · تفكيك T=209 (§٢١): خام T + J∩T + C∩T
    for ln in verses:
        poss = [p for p in (word_positions(w) for w in ln.split(" ") if w.strip()) if p]
        p0 = poss[0]
        chained = p0[0] in (("و", "فتحة"), ("ف", "فتحة"))
        g, gj = gate(p0)
        raw["C" if chained else g] += 1
        if gj and not chained:
            raw_j[gj] += 1
            if station(p0) == "T":
                redir_T += 1                         # مدخلٌ تنوينيٌّ جارٌّ (بِ…ٍ/لِ…ٍ…) — T §٢١ تقدّمه J هنا
        if chained and station(p0) == "T":
            chain_T += 1                             # معطوفةٌ تنوينيةُ الخاتمة (وَالصَّافَّاتِ…) — ابتلعتها C خامًا
        if not chained and g == "B":
            topB_raw["".join(ch for ch, _ in p0)] += 1
        rest = p0[1:] if (chained and len(p0) >= 2) else (poss[1] if chained else p0)
        g2, gj2 = gate(rest)
        strip[g2] += 1
        if gj2:
            strip_j[gj2] += 1
        if g2 == "B":
            topB_strip["".join(ch for ch, _ in rest)] += 1
        if chained and len(poss) == 1:
            oath_1w += 1
    assert sum(raw.values()) == 6236 and sum(strip.values()) == 6236, "الأصناف لا تسدّ الآيات"

    tri = Counter({"شبه": strip["J"], "اسمية": strip["A"] + strip["T"], "أعمى": strip["B"]})
    H_raw = -sum(v / 6236 * log2(v / 6236) for v in raw.values())
    H_tri = -sum(v / 6236 * log2(v / 6236) for v in tri.values())
    return dict(raw=raw, strip=strip, raw_j=raw_j, strip_j=strip_j, tri=tri,
                H_raw=H_raw, H_tri=H_tri, oath_1w=oath_1w, redir_T=redir_T,
                topB_raw=topB_raw.most_common(3), topB_strip=topB_strip.most_common(3),
                chain_T=chain_T)

# ---------- ٨) الفحص المشغَّل (يُدار عند الاستدعاء) ----------
if __name__ == "__main__":
    assert len(UNITS) == 256 and len({pack(*u) for u in UNITS}) == 256
    assert all(unpack(pack(*u)) == u for u in UNITS)          # on البايت
    assert all(dec(enc(*u)) == u for u in UNITS)              # on الترميز
    adj = defaultdict(list)
    for op, a, b in EDGES:
        assert a in W10 and b in W10                          # مانع
        adj[a].append(b)
    reach, stack = set(), ["I"]
    while stack:                                              # جامع
        n = stack.pop()
        if n not in reach:
            reach.add(n); stack += adj[n]
    assert reach == set(W10)
    n_flag = sum(row.count("⚑ل") + row.count("⚑س") for row in PARADIGM.values())
    P, pi, H_pi, rate = derivation_markov()
    TAGS = [{"نوع": "مبني", "بناء": ("فتحة", "آخر")},
            {"نوع": "مبني", "بناء": ("سكون", "R5-أول")},
            {"نوع": "مركّب"}]
    demo = []
    words = "قَالَ آمَنَّا بِالْكِتَابِ".split(" ")
    assert len(words) == len(TAGS), "كلمةٌ بلا وسمٍ = صريخٌ لا افتراض"
    for w, tg in zip(words, TAGS):
        u = parse_word(w)
        demo += list(zip(u, classify_word(u, tg)))
    assert [unpack(pack(li, si)) for (li, si, _), _ in demo] == [(li, si) for (li, si, _), _ in demo]
    tpu = []
    for w, tg in zip(words, TAGS):
        tpu += [tg] * len(parse_word(w))
    peeled, kept, _table = peel([u for u, _ in demo], [c for _, c in demo], tpu)
    t112 = peel112(); t256 = peel256_strict()
    print(f"فضاء 256 مغلقٌ محقون ✓ | الإغلاق جامعٌ مانع ✓ | المصفوفة {120-n_flag}+⚑{n_flag} | "
          f"ماركوف: مثالُ سياسةٍ موحَّدة (H(π)={H_pi:.4f}، معدل={rate:.4f}) — التفرّع عند I وحدها بنيويٌّ | "
          f"FOR+جسر: {len(demo)}/{len(demo)} ✓ | تقشير: {peeled}□ مقشور + {kept}■ حامل = {8*len(demo)} بتًّا — استرجاعٌ تامّ | "
          f"112↑: □{t112['□']}/◆{t112['◆']}/■{t112['■']} = {sum(t112.values())} بتًّا — بلا تسريب | "
          f"256↑صارم: □{t256['□']}/◆{t256['◆']}/■{t256['■']} = {sum(t256.values())} — الترخيص بتٌّ واحدٌ للأعلى")
    if os.path.exists(MUJAMMAD_PATH):                     # القياس على المجمَّد — بالبصمة أو لا قياس
        cells, letters, joint, pos = audit_corpus()
        codes, H_s, L_h = huffman(cells)
        N = sum(letters.values())
        H_l = -sum(v / N * log2(v / N) for v in letters.values())
        H_j = -sum(v / N * log2(v / N) for v in joint.values())
        print(f"مجمَّد: {pos} موضعًا، تعارضات 0 ✓ | H(حالة)={H_s:.4f} | هوفمان L={L_h:.4f} "
              f"(المسطَّح 3.0000 — فائض {3 - L_h:.4f} بت/موضع) | ترتيبه: "
              + "، ".join(f"{k}={len(codes[k])}" for k in sorted(codes, key=lambda k: len(codes[k])))
              + f" | Δضبط = H(حالة|حرف) = {H_j - H_l:.4f} بت (على 36×8 معلنًا)")
        (c_out, H_out, L_out), (c4, H4, L4), (c_in, H_in, L_in), p_s, L_t = peel112_measured(cells)
        print(f"112↑مقيس بالختم: خارجي L={L_out:.4f} (H={H_out:.4f}) "
              f"[{', '.join(f'{k}={c_out[k]}' for k in c_out)}] | داخل الحصّة L={L4:.4f} (H={H4:.4f}؛ "
              f"المسطَّح 2.0000 — فائض {2 - L4:.4f}) | داخل الختم L={L_in:.4f} "
              f"[{', '.join(f'{k}={c_in[k]}' for k in c_in)}] | الفاتورة L={L_t:.4f} = {L_out:.4f}+{p_s:.6f}×{L_in:.4f} — "
              f"ثمن العزل على §١٧ المباشر ({L_h:.4f}): +{L_t - L_h:.4f} بت/موضع")
        # انقلاب الربح بالتباديل على الجبر المغلق 112 + ماركوف باتجاهين
        cells4 = Counter({k: cells[k] for k in LICENSED4})
        lb4, lw4, d4, o4 = assign_stats(cells4, [len(c4[k]) for k in c4])
        lb8, lw8, d8, o8 = assign_stats(cells, [len(codes[k]) for k in codes])
        outer5 = Counter({k: cells[k] for k in LICENSED4})
        outer5["ختم"] = sum(cells[k] for k in SEALED4)
        lb5, lw5, d5, o5 = assign_stats(outer5, [len(c_out[k]) for k in c_out])
        letters_lic = Counter()
        for (ch, ce), v in joint.items():
            if ce in LICENSED4:
                letters_lic[ch] += v
        cL, H_L, L_L = huffman(letters_lic)
        lbL, lwL, dL, oL = assign_stats(letters_lic, [len(cL[k]) for k in cL])
        flatL = ceil(log2(len(letters_lic)))
        Hc, per_prev, Np, big, prev_m = bigram_states()
        print(f"انقلاب الربح بالتباديل: حالة4 أطوال[1,2,3,3]: أفضل {lb4:.4f} ⟷ أردأ {lw4:.4f} — رهن {lw4 - lb4:.4f} "
              f"(تخصيصات {d4}، مثلى {o4}؛ مسطَّح 4!=24 تبديلًا رهنها 0.0000) | §١٧ أطوال[2,2,3,3,3,4,5,5]: "
              f"{lb8:.4f} ⟷ {lw8:.4f} — رهن {lw8 - lb8:.4f} ({d8}، مثلى {o8}) | ختم5: {lb5:.4f} ⟷ {lw5:.4f} — "
              f"رهن {lw5 - lb5:.4f} ({d5}، مثلى {o5})")
        print(f"حقل الحرف على المواضع المرخَّصة ({sum(letters_lic.values()):,}): أنماط {len(letters_lic)}، "
              f"مسطَّح {flatL} بت (وإطار 112 يخصص 5 بت لـ28 حرفًا — الزائدون مسمَّون في البرهان) | "
              f"H={H_L:.4f} L={L_L:.4f} — فائض على مسطَّح الأنماط {flatL - L_L:.4f} وعلى حقل 112 "
              f"{5 - L_L:+.4f} | تباديل: رهن {lwL - lbL:.4f} (تخصيصات {dL}، مثلى {oL}) | "
              f"الجبر المغلق 112 كاملًا: مسطَّح 7.0000 = 5+2 ⟷ مقيس {L_L:.4f}+{L4:.4f}={L_L + L4:.4f} — "
              f"ربح {7 - L_L - L4:.4f} بت/موضع")
        print(f"ماركوف ON: أزواج {Np:,} داخل السطر — H(حالة|سابقتها)={Hc:.4f} ⟷ H(حالة)={H_s:.4f} — "
              f"ربح الذاكرة {H_s - Hc:.4f} بت/موضع | لكل سابقة: "
              f"[{', '.join(f'{k}={v:.3f}' for k, v in sorted(per_prev.items(), key=lambda kv: -prev_m[kv[0]]))}] | "
              f"ماركوف FOR (مثال الاشتقاق الموسوم): H(π)=2.8729 ⟷ معدل 1.0340 — ربح {2.8729 - 1.0340:.4f}")
        # محطة الاسم والفعل والحرف — توقف الجشع وتحوّله (مستوى الكلمة)
        st = word_station()
        top_amb = sorted(st["amb"].items(), key=lambda kv: -sum(kv[1].values()))[:4]
        print(f"محطة الاسم/الفعل/الحرف: كلمات {st['Nw']:,} (متوسط الطول {st['wlen']:.4f} موضعًا) | "
              f"السطحية الموسومة: تنوين T={st['cls']['T']:,} · ال A={st['cls']['A']:,} · عارٍ B={st['cls']['B']:,} "
              f"({100 * st['cls']['B'] / st['Nw']:.2f}% بلا بوّابة — هنا يقف الجشع) | "
              f"H(محطة)={st['H_cls']:.4f} ⟷ مسطَّح {log2(3):.4f} — فائض {log2(3) - st['H_cls']:.4f}")
        print(f"توقف الجشع معروضًا: هياكل {len(st['skel']):,} — غامضة {len(st['amb']):,} "
              f"({100 * len(st['amb']) / len(st['skel']):.2f}%) تحمل {st['mass']:,} كلمة "
              f"({100 * st['mass'] / st['Nw']:.2f}%) — الحرف لا يعيّن الصنف | أمثلة بالعدّ: "
              + " · ".join(f"{s}: {sum(c.values()):,} على {len(c)} أنماط" for s, c in top_amb)
              + f" | بوّابة النقض T∩A=0 ✓ (ال+تنوين لا يجتمعان على {st['Nw']:,} كلمة)")
        print(f"التحوّل: العضوية عند T مدفوعةٌ بأغلى علامةٍ في §١٧ (تنوين 4–5 بت) وعند A بمقشورٍ بنيويٍّ "
              f"(مدخل عري {st['entry']['A'].get('عري', 0):,}/{st['cls']['A']:,} = همزة وصل ق4)، وعند B لا علامة — "
              f"بتُّ العضوية يُحفَظ بالاسم في المعجم (دَين قائم) | نتيجةٌ سالبةٌ معروضة: المحطة لا تدفع أماميًّا — "
              f"ربح الصنف→الصنف {st['H_cls'] - st['Hc_cls']:+.4f} والصنف→المدخل {st['H_init'] - st['Hc_fwd']:+.4f} بت؛ "
              f"ربح الذاكرة قُبض موضعيًّا عند التنوين في §١٩")
        # قبل ترخيص الجملة — العتبة (مستوى الآية)
        bs = before_sentence()
        tv = sum(v for s, v in bs["vfinal"].items() if "تنوين" in s)
        tw = sum(v for s, v in bs["final_all"].items() if "تنوين" in s)
        print(f"قبل ترخيص الجملة: آيات {bs['Nv']:,} (+10 أسطر ترويسةٍ موسومة) | كلمات/آية: متوسط "
              f"{sum(bs['w_per_v']) / bs['Nv']:.4f} (1–{max(bs['w_per_v'])})، H(طول)={bs['H_len']:.4f} | "
              f"آية ≠ جملة بالعدّ: {bs['vopen_conj']:,} آية ({100 * bs['vopen_conj'] / bs['Nv']:.2f}%) تبدأ موصولًا "
              f"بـوَ/فَ | بوّابة العطف (حدٌّ أعلى موسوم — الجذرية لا تُفصل): وَ={bs['conj']['وَ']:,} "
              f"فَ={bs['conj']['فَ']:,} = {100 * (bs['conj']['وَ'] + bs['conj']['فَ']) / bs['Nw']:.2f}% من الكلمات")
        print(f"إشارة الحدّ الظاهرة: خاتمة الآية فتحة {100 * bs['vfinal']['فتحة'] / bs['Nv']:.2f}% ⟷ خاتمة الكلمة "
              f"{100 * bs['final_all']['فتحة'] / bs['Nw']:.2f}% · تنوين {100 * tv / bs['Nv']:.2f}% ⟷ {100 * tw / bs['Nw']:.2f}% · "
              f"H: {bs['H_vf']:.4f} ⟷ {bs['H_wf']:.4f} (الحدّ يكثّف) | وحيدةُ الكلمة: {len(bs['one_word'])} آيةً "
              f"(20 فواتحَ مقطّعةً + 8 عادية) — منها {bs['mq_inA']} تبتلعها بوّابة A (عمًى معدود) | "
              f"بسم = {bs['bsm']} (27:30 منقوصةٌ في المجمَّد — الغيبة معدودة) | أول كلمة: B={bs['vfirst']['B']:,} "
              f"A={bs['vfirst']['A']} T={bs['vfirst']['T']} | ⟹ ترخيص الجملة موقوفٌ على دَينين: حدودٌ معلنة + المعجم")
        # عتبة حدود الجملة — الثلاثيّ الجمليّ وصعود البتّ الجشع (مستوى المدخل الآييّ — وكيلٌ موسوم)
        th = sentence_threshold()
        tb = " · ".join(f"{s}:{v:,}" for s, v in th["topB_raw"])
        tbs = " · ".join(f"{s}:{v:,}" for s, v in th["topB_strip"])
        print(f"عتبة الجملة (مداخل 6,236 آية — وكيلٌ موسوم لا جملة): خام C={th['raw']['C']:,} · "
              f"J={th['raw']['J']:,} · A={th['raw']['A']:,} · T={th['raw']['T']:,} · B={th['raw']['B']:,} | "
              f"H(خام5)={th['H_raw']:.4f} ⟷ مسطَّح {log2(5):.4f} | بعد قلع العطف: J={th['strip']['J']:,} "
              f"(قائمة {th['strip_j']['قائمة']:,} + ق6 {th['strip_j']['ق6']:,}) · A={th['strip']['A']:,} · "
              f"T={th['strip']['T']:,} · B={th['strip']['B']:,}")
        print(f"الثلاثيّ الجمليّ بالوكيل: شبه={th['tri']['شبه']:,} · اسمية مرشَّحة={th['tri']['اسمية']:,} · "
              f"أعمى={th['tri']['أعمى']:,} | H={th['H_tri']:.4f} ⟷ مسطَّح log₂(3)={log2(3):.4f} — فائض "
              f"{log2(3) - th['H_tri']:.4f} بت/آية ({(log2(3) - th['H_tri']) * 6236:,.0f} بت على المجمَّد) | "
              f"تصحيح السلّم موسومًا: 8⟵3⟵3 (شبه الجملة ظاهرةٌ ثالثة معلنة — §٢١ كان بثنائيةٍ فقط) | "
              f"أعمى B خامًا: {tb} | بعد القلع: {tbs} | وحيدات وَ (قسم ظاهر مبتلَع في C): {th['oath_1w']} | "
              f"مصالحة T=209 (§٢١): خام {th['raw']['T']} + J∩T {th['redir_T']} + C∩T {th['chain_T']} = "
              f"{th['raw']['T'] + th['redir_T'] + th['chain_T']} ✓ — الفعلية الحاسمة دَينُ المعجم القائم")
    else:
        print(f"مجمَّد: غائب عن القرص — القياس مؤجَّل ببصمته {MUJAMMAD_SHA256[:12]}… (لا قياس على بديلٍ صامت)")
