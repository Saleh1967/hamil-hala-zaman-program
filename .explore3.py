import os, sys, json, random
from collections import Counter
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "induction"))
import ta3allum_gate as TG
import aqsam_gate as AG
import qisma_gate as QG
import madlul_gate as MDG
import dalalat_gate as DG
import awzan_engine as AE
import maqayis_layer as ML
import mihwar_gate as MG

verses, stream, _ = TG.corpus_surfaces()
cands, counts = TG.hypothesis_space(stream)
rich = AE.tokenize_rich()
flat = [w for v in rich for w in v]
L = AE.LAYERS[-1]
roots = [(lambda h: h[1] if h else None)(AE.hit(w, L)) for w in flat]
rows = ML.read_table()
entries = {}
for r in rows:
    entries.setdefault(r["root_full"], r)
awz, widest = ML.awzan_roots()
mapped = {r: (entries[r].get("semantic_axes") or "").strip()
          for r in awz if r in entries and (entries[r].get("semantic_axes") or "").strip()}
axis = [mapped.get(r) if r else None for r in roots]
field = [i for i, a in enumerate(axis) if a]
withroot = [i for i, r in enumerate(roots) if r]
print("مقام", len(stream), "| له وضع", len(field), "| له جذر بلا وضع",
      len(withroot) - len(field), "| لا جذر", len(stream) - len(withroot))

faw = {DG.fold(f) for f in MDG.FAWATIH}
fawpos = [i for i, s in enumerate(stream) if s in faw]
fawwad = [i for i in fawpos if axis[i]]
print("مواضع الفواتح", len(fawpos), "منها نُسب إليها وضع", len(fawwad),
      "صورها:", sorted({stream[i] for i in fawwad}))

hija, lafz, ma3na = QG.lafz_names()
lafzforms = {DG.fold(n) for n in set(hija) | set(lafz)}
lafzpos = [i for i, s in enumerate(stream) if s in lafzforms]
print("مواضع طائفة أسماء اللفظ", len(lafzpos))

ranked = AG.imam_ranking(cands, AG.imam_folded())
F8 = sorted(cands, key=lambda c: (-ranked[c], c))[:8]
print("F8", F8)

def bill(forms, fire, tag):
    try:
        b = TG.rule_bill(stream, tuple(forms), fire, random.Random(TG.CONTROL_SEED))
        print(f"  {tag:<28} إطلاق {b['إطلاق']:>6} نصيب {b['نصيب']:<8} Δ {b['Δ']:>12,.1f} ضابط {b['ضابط']:>12,.1f}  {b['حكم']}")
        return b
    except TG.Ta3allumError as e:
        print(f"  {tag:<28} صريخ: {e.message}")
        return None

for k in AG.RUNGS:
    F = sorted(cands, key=lambda c: (-ranked[c], c))[:k]
    Fs = set(F)
    print("درج", k)
    bill(F, AG.fire_of_rank("التضمّن", stream, F), "التضمّن بالصورة")
    fm = {i for i in field if stream[i] not in Fs and any(f in axis[i] for f in F)}
    bill(F, fm, "التضمّن بالمدلول (تضمين)")
    fw = {i for i in field if stream[i] not in Fs and any(f in axis[i].split() for f in F)}
    bill(F, fw, "التضمّن بالمدلول (قائم)")
    # rival: random forms same count from candidates
    R = random.Random(TG.CONTROL_SEED).sample(sorted(cands), k)
    Rs = set(R)
    fr = {i for i in field if stream[i] not in Rs and any(f in axis[i] for f in R)}
    bill(R, fr, "مدلول بصورٍ عشوائية")
