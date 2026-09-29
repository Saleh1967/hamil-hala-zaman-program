import os, sys, json, random
from collections import Counter
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "induction"))
import ta3allum_gate as TG
import aqsam_gate as AG
import awzan_engine as AE
import maqayis_layer as ML
import mihwar_gate as MG

verses, stream, _ = TG.corpus_surfaces()
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
print("field", len(field))

# form -> axis (a form may map to >1 axis? check)
f2a = {}
conflict = 0
for i in field:
    s = stream[i]
    if s in f2a and f2a[s] != axis[i]:
        conflict += 1
    f2a.setdefault(s, axis[i])
print("forms with wad3:", len(f2a), "conflicts:", conflict)

cnt = Counter(stream)
n0 = TG.SPACE["أدنى_تكرار"]
cands = sorted(s for s in f2a if cnt[s] >= n0)
print("candidates freq>=", n0, ":", len(cands))
print(cands[:40])

# surface-only candidate space overlap
sc, _ = TG.hypothesis_space(stream)
print("surface candidates:", len(sc), "overlap:", len(set(sc) & set(cands)))

# semantic tadammun fire counts with substring rule
def axis_of(s): return f2a.get(s)
for k in (8, 16, 32):
    if len(cands) < k: print("too few for k", k); continue
    ranked = AG.imam_ranking(cands, AG.imam_folded())
    F = sorted(cands, key=lambda c: (-ranked[c], c))[:k]
    Fax = {f2a[f] for f in F}
    fire_s = {i for i, s in enumerate(stream) if s not in set(F) and any(f in s for f in F)}
    fire_m = {i for i in field if stream[i] not in set(F)
              and any(f2a[f] in axis[i] and f2a[f] != axis[i] for f in F)}
    print("k", k, "F", F)
    print("   fire surface", len(fire_s), "fire madlul", len(fire_m))
