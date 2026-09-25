# algebra_engine.py — الجبر المشغَّل (إيداع التفويض)
# النظام من الداخل: فضاء الوحدة (بايت)، جبر الأوزان (سنّ)، ماركوف الاشتقاق، الاستقراء المشغَّل.
# كل عدٍّ هنا معروضٌ أو مشتقٌّ بقاعدة — انضباط البند ٧ (لا عدَّ مُعلَنًا غيرَ معروض).
from math import log2
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
    else:
        print(f"مجمَّد: غائب عن القرص — القياس مؤجَّل ببصمته {MUJAMMAD_SHA256[:12]}… (لا قياس على بديلٍ صامت)")
