# waqf_layer.py — المرحلة ٢ / الجولة الأولى: حدودُ الجملة بمقارنةٍ مقيسة لا برأي.
# ثلاثةُ مقترحاتٍ موسومة (§٢١) تُقاس هنا من مسبارٍ واحدٍ معلن، ثم يُبنى على الفائز وحده:
#   أ) الفاصلة        — ترقيمٌ في المتن (يُعَدّ موضعًا: متنٌ ⟷ ترويسة)
#   ب) وقف القارئ     — علاماتُ الوقف السبع في النسخة العثمانية بختمها (نظامُ حدودٍ مؤلَّف)
#   ج) الضابط النحوي  — «خاتمةٌ عاريةٌ + وصلةُ وَ/فَ» (توزيعيٌّ: طبقةُ تصادمٍ لا طبقةُ حكم)
#
# المقامان مختومان ولا يعبر بينهما رقمٌ إلا بمواءمةٍ معلنة:
#   المجمَّد  (quran-simple-enhanced) sha256 8b387ea8… — تقرؤه parse_verses بعينها
#   العثماني (quran-uthmani)          sha256 16d65358… — مُعلنٌ هنا مصدرَ حقيقةٍ واحدًا
# الكلفة معلنة، و⚑ والمعجم لا يُمسّان: هذا قياسُ حدودٍ لا تصنيفُ كلمات (assert في آخر run).
from collections import Counter, defaultdict
from functools import lru_cache
import argparse, hashlib, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "induction"))
from induction_engine import parse_verses                      # المجمَّد بختمه — لا نسخةَ ثانية
from dictionary_engine import classify_word, skel_of, CORPUS   # أصنافُ المعجم بعينها

UTHMANI = os.path.join(ROOT, "uthmani.txt")
UTHMANI_SHA256 = "16d65358f9a46f684a418fa8665aa8ac7b3a394222c81a3b38859ac58c28b37f"
UTHMANI_BYTES = 1352197
UTHMANI_SOURCE = "globalquran/data@Quran/quran-uthmani.txt (Tanzil)"

# ---------- علاماتُ الوقف السبع: نقطةُ الشيفرة هي الاسم، والتسميةُ العربيةُ معلنةٌ بإزائها ----------
WAQF = {0x06D6: "صلى", 0x06D7: "قلى", 0x06D8: "م", 0x06D9: "لا", 0x06DA: "ج",
        0x06DB: "معانقة", 0x06DC: "سكتة"}
WAQF_ORDER = [WAQF[c] for c in sorted(WAQF)]
PUNCT = "،؛؟.,:!?"                                   # مسبارُ المقترح (أ) — مجموعةٌ معلنة

# ---------- حروفُ الرسم والمواءمة (قاعدةٌ معلنةٌ بثلاث درجات، لا مواءمةَ بصمت) ----------
LETTER = lambda c: (0x0621 <= ord(c) <= 0x063A or 0x0641 <= ord(c) <= 0x064A
                    or ord(c) in (0x0670, 0x0671))
RASM = {0x0671: "ا", 0x0670: "ا", 0x0622: "ا", 0x0623: "ا", 0x0625: "ا",
        0x0649: "ي", 0x0624: "ء", 0x0626: "ء", 0x0629: "ه"}


def skeleton(word):
    """هيكلُ الكلمة للمواءمة: حروفٌ بلا تشكيلٍ ولا وقف، بتسوياتٍ مسمّاة —
    ألفُ الوصل والألفُ الخنجرية ⟵ ا · الهمزاتُ إلى كرسيٍّ واحدٍ ثم تُسقَط · ى⟵ي · ة⟵ه."""
    return "".join(RASM.get(ord(c), c) for c in word if LETTER(c)).replace("ء", "")


NO_ALEF = lambda s: s.replace("ا", "")               # الدرجة الثالثة: الألف المحذوفة رسمًا


def read_uthmani(path=UTHMANI):
    blob = open(path, "rb").read()
    assert len(blob) == UTHMANI_BYTES, f"ليست النسخة العثمانية — الطول {len(blob)}"
    assert hashlib.sha256(blob).hexdigest() == UTHMANI_SHA256, "ليست النسخة العثمانية — البصمة خُالفت"
    text = blob.decode("utf-8-sig")
    body = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    header = [ln for ln in text.splitlines() if ln.lstrip().startswith("#")]
    assert len(body) == 6236, f"بصمةُ الآيات خُولفت في العثماني: {len(body)}"
    return body, header


def uthmani_verse(line):
    """السطرُ العثمانيّ ⟵ (كلماتٌ بلا علاماتِ وقف، علاماتٌ موضوعةٌ بعد كلمةٍ مرقَّمة، زخارف).
    العلامةُ الواقفةُ رمزًا مستقلًّا حدٌّ بين كلمتين؛ والملتصقةُ داخل كلمةٍ تُسجَّل بموضع كلمتها
    و**لا تُعَدّ حدًّا** (السكتتان الموسومتان). والرمزُ الذي لا حرفَ فيه (علامةُ الحزب ۞
    وموضعُ السجدة ۩) **زخرفٌ لا كلمة**: يُعَدّ بالاسم ولا يأخذ رقمًا. لا علامةَ تُهمَل."""
    words, marks, inside, ornaments = [], [], [], 0
    for tok in line.split(" "):
        if not tok:
            continue
        m = [WAQF[ord(c)] for c in tok if ord(c) in WAQF]
        rest = "".join(c for c in tok if ord(c) not in WAQF)
        if not any(LETTER(c) for c in rest):
            if rest.strip():
                ornaments += 1
            for name in m:                           # حدٌّ بعد الكلمة الأخيرة المعدودة
                marks.append((len(words) - 1, name))
            continue
        words.append(rest)
        for name in m:
            inside.append((len(words) - 1, name))
    return words, marks, inside, ornaments


def align_verse(U, M):
    """مواءمةٌ معلنةٌ بين كلمات السطر العثماني (U) وكلمات آية المجمَّد (M) — هياكلُ لا تشكيل.
    الانتقالاتُ الأربعة مسمّاة: تطابقٌ · ضمٌّ (عثمانيةٌ = مجمَّدتان) · فصلٌ (عثمانيتان = مجمَّدة)
    · تسويةُ الألف المحذوفة رسمًا. والباقي **غيرُ مواءَم** يُعَدّ بالاسم ولا يُجسَر عليه.
    الاختيارُ أعظمُ عددٍ مُواءَم، وعند التساوي أقلُّ استعمالٍ للدرجات الأدنى — حتميٌّ لا جشعيّ."""
    n, m = len(U), len(M)

    @lru_cache(maxsize=None)
    def best(i, j):
        if i == n or j == m:
            return (0, 0, 0, ())
        opts = []
        if U[i] == M[j]:
            a, c, d, p = best(i + 1, j + 1)
            opts.append((a + 1, c, d, ((i, j, 1, 1),) + p))
        elif NO_ALEF(U[i]) == NO_ALEF(M[j]):
            a, c, d, p = best(i + 1, j + 1)
            opts.append((a + 1, c, d + 1, ((i, j, 1, 1),) + p))
        if j + 1 < m and NO_ALEF(U[i]) == NO_ALEF(M[j] + M[j + 1]):
            a, c, d, p = best(i + 1, j + 2)
            opts.append((a + 1, c + 1, d, ((i, j, 1, 2),) + p))
        if i + 1 < n and NO_ALEF(U[i] + U[i + 1]) == NO_ALEF(M[j]):
            a, c, d, p = best(i + 2, j + 1)
            opts.append((a + 1, c + 1, d, ((i, j, 2, 1),) + p))
        opts.append(best(i + 1, j))
        opts.append(best(i, j + 1))
        return max(opts, key=lambda r: (r[0], -r[1], -r[2]))

    a, c, d, pairs = best(0, 0)
    best.cache_clear()
    return a, c, d, pairs


def run(muj=CORPUS, uth=UTHMANI):
    verses = parse_verses(muj)
    body, header = read_uthmani(uth)

    # ---------- المقترح (أ): الفاصلة — ترقيمٌ في المتن، مقيسٌ موضعًا ----------
    punct_body = sum(1 for ln in body for c in ln if c in PUNCT)
    punct_head = sum(1 for ln in header for c in ln if c in PUNCT)

    # ---------- المقترح (ب): طبقةُ الوقف المعلنة ----------
    dist, sites, marked_verses, inside_n, ornaments = Counter(), [], 0, 0, 0
    for vi, ln in enumerate(body):
        words, marks, inside, orn = uthmani_verse(ln)
        ornaments += orn
        for wi, name in marks:
            dist[name] += 1
            sites.append(f"{vi}:{wi}:{name}")
        for wi, name in inside:
            dist[name] += 1
            inside_n += 1
            sites.append(f"{vi}:{wi}:{name}@داخل")
        if marks or inside:
            marked_verses += 1
    waqf_total = sum(dist.values())

    # ---------- المواءمة بين المقامين ----------
    u2m = {}                                          # (آية، كلمةٌ عثمانية) ⟵ كلمةٌ مجمَّدة
    al = comp = alef = utok = 0
    unaligned_u = Counter()
    for vi, (ln, mws) in enumerate(zip(body, verses)):
        U = tuple(skeleton(w) for w in uthmani_verse(ln)[0])
        M = tuple(skeleton("".join(ch for ch, _ in w)) for w in mws)
        utok += len(U)
        a, c, d, pairs = align_verse(U, M)
        al += a; comp += c; alef += d
        covered = set()
        for i, j, du, dm in pairs:
            for k in range(du):
                covered.add(i + k)
                u2m[(vi, i + k)] = j                  # الضمُّ/الفصلُ يشيران إلى أوّل المجمَّدة
        for i, s in enumerate(U):
            if i not in covered:
                unaligned_u[s] += 1

    # ---------- المقترح (ج): مرشّحات الضابط النحوي السطحي ----------
    sup = defaultdict(Counter)
    for ws in verses:
        for w in ws:
            sup[skel_of(w)][w[-1][1]] += 1
    cands, end_bare, q_only = [], 0, 0
    nwords = 0
    for vi, ws in enumerate(verses):
        for i, w in enumerate(ws):
            nwords += 1
            if w[-1][1] != "عري":                     # خاتمةٌ عارية: ق-فراغ ومعها ز-مزاح بالاسم
                continue
            if i + 1 == len(ws):
                end_bare += 1
                continue
            nxt = ws[i + 1][0]
            if nxt[0] in ("و", "ف") and nxt[1] == "فتحة":
                cands.append((vi, i))
                q_only += classify_word(w, sup)[0] == "ق"

    # ---------- التصادم: أين تقع المرشّحاتُ من علامات الوقف؟ ----------
    m2u = defaultdict(list)
    for (vi, ui), mj in u2m.items():
        m2u[(vi, mj)].append(ui)
    bound = defaultdict(set)                          # مواضعُ الحدّ العثمانيةِ الموقوفة
    for vi, ln in enumerate(body):
        for wi, _ in uthmani_verse(ln)[1]:
            bound[vi].add(wi)
    hit = before = after = miss = unmapped = 0
    for vi, i in cands:
        us = m2u.get((vi, i))
        if not us:
            unmapped += 1
            continue
        u = max(us)                                   # آخرُ كلمةٍ عثمانيةٍ تقابل المجمَّدة
        if u in bound[vi]:
            hit += 1
        elif u - 1 in bound[vi]:
            before += 1
        elif u + 1 in bound[vi]:
            after += 1
        else:
            miss += 1
    n_cand = len(cands)
    marked = sum(len(s) for s in bound.values())
    R = dict(
        seals=dict(mujammad_sha256_prefix="8b387ea8", uthmani_sha256=UTHMANI_SHA256,
                   uthmani_bytes=UTHMANI_BYTES, uthmani_source=UTHMANI_SOURCE),
        proposal_a_fasila=dict(punct_set=PUNCT, in_body=punct_body, in_header=punct_head,
                               verdict="غيابٌ معلن — لا حدَّ في المتن"),
        proposal_b_waqf=dict(total=waqf_total, verses=marked_verses,
                             verses_pct=round(marked_verses / len(body) * 100, 2),
                             per_marked=round(waqf_total / marked_verses, 2),
                             distribution={k: dist[k] for k in WAQF_ORDER},
                             inside_word=inside_n, ornaments=ornaments, boundary_sites=marked,
                             sites=sites, verdict="حدودٌ مؤلَّفةٌ مختومة"),
        proposal_c_nahwi=dict(candidates=n_cand, class_q_only=q_only,
                              bare_end_of_verse=end_bare,
                              density=round(n_cand / nwords, 4),
                              verdict="توزيعيٌّ — طبقةُ تصادمٍ لا حكم"),
        alignment=dict(uthmani_tokens=utok, mujammad_words=nwords, aligned=al,
                       aligned_pct=round(al / utok * 100, 2), composite=comp,
                       by_alef_rule=alef, unaligned=utok - al,
                       unaligned_top=[f"{s}×{n}" for s, n in unaligned_u.most_common(20)]),
        collision=dict(candidates=n_cand, on_mark=hit, mark_before=before, mark_after=after,
                       no_mark=miss, unmapped=unmapped,
                       on_mark_pct=round(hit / n_cand * 100, 2),
                       waqf_boundaries=marked,
                       recall_pct=round(hit / marked * 100, 2)),
        cost_bits=len(WAQF) * 8 * 4 + 4 * 8 * 4,      # سبعُ علاماتٍ مسمّاة + أربعُ درجاتِ مواءمة
    )
    assert nwords == 77801 and R["proposal_b_waqf"]["total"] == 4366, "مصالحةُ المقامين خُولفت — صريخ"
    return R


def main(argv=None):
    ap = argparse.ArgumentParser(description="طبقة الوقف — حدود الجملة بمقارنةٍ مقيسة")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    a = ap.parse_args(argv)
    if not os.path.isfile(UTHMANI):
        print("::warning::النسخة العثمانية غائبة — شغّل ./fetch_uthmani.sh؛ ولا قياس على بديلٍ صامت")
        return 1
    R = run()
    A, B, C = R["proposal_a_fasila"], R["proposal_b_waqf"], R["proposal_c_nahwi"]
    G, K = R["alignment"], R["collision"]
    print(f"المقترح (أ) الفاصلة: ترقيمٌ في المتن {A['in_body']} · في الترويسة {A['in_header']} — {A['verdict']}")
    print(f"المقترح (ب) وقف القارئ: {B['total']:,} علامة في {B['verses']:,} آية ({B['verses_pct']}%) · "
          f"{B['per_marked']}/معلَّمة — " + " · ".join(f"{k}={B['distribution'][k]:,}" for k in WAQF_ORDER))
    print(f"    حدودٌ بين الكلمات {B['boundary_sites']:,} · داخل الكلمة {B['inside_word']} (لا تُعَدّ حدًّا) · "
          f"زخارفُ الحزب/السجدة {B['ornaments']} (لا تأخذ رقمًا)")
    print(f"المقترح (ج) الضابط النحوي: مرشّحات «خاتمةٌ عارية + وَ/فَ» {C['candidates']:,} "
          f"(منها ق-فراغ خالصةً {C['class_q_only']:,}) · خاتمةٌ عاريةٌ آخرَ الآية {C['bare_end_of_verse']:,} · "
          f"كثافة {C['density']}/كلمة — {C['verdict']}")
    print(f"المواءمة: عثمانيٌّ {G['uthmani_tokens']:,} ⟷ مجمَّد {G['mujammad_words']:,} · "
          f"مُواءَم {G['aligned']:,} ({G['aligned_pct']}%) · ضمٌّ/فصل {G['composite']} · "
          f"بتسوية الألف {G['by_alef_rule']:,} · **غيرُ مواءَم {G['unaligned']:,}** بالاسم في JSON")
    print(f"التصادم: على العلامة {K['on_mark']:,} من {K['candidates']:,} ({K['on_mark_pct']}%) · "
          f"قبلها {K['mark_before']:,} · بعدها {K['mark_after']:,} · بلا علامة {K['no_mark']:,} · "
          f"غيرُ مواءَم {K['unmapped']:,} | استرجاعُ الحدود {K['recall_pct']}% من {K['waqf_boundaries']:,}")
    print(f"كلفةُ الطبقة معلنة: {R['cost_bits']} بت — ⚑ والمعجم لم يُمسّا (قياسُ حدودٍ لا تصنيفُ كلمات)")
    if a.json:
        json.dump({"الوقف_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
