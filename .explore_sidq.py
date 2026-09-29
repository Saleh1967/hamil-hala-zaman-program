import os, sys, json
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "induction"))
import ta3allum_gate as TG
import awzan_engine as AE
import maqayis_layer as ML
import mihwar_gate as MG

verses, stream, _ = TG.corpus_surfaces()
rich = AE.tokenize_rich()
print("verses(parse_marked)", len(verses), "verses(rich)", len(rich))
print("words stream", len(stream), "words rich", sum(len(v) for v in rich))
flat = [w for v in rich for w in v]
print("align head:", [AE_s for AE_s in [ "".join(c for c,_,_ in w) for w in flat[:5]]], stream[:5])

# root per position at widest layer
L = AE.LAYERS[-1]
roots = []
for w in flat:
    h = AE.hit(w, L)
    roots.append(h[1] if h else None)
print("positions with root:", sum(1 for r in roots if r))
rows = ML.read_table()
entries = {}
for r in rows:
    entries.setdefault(r["root_full"], r)
awz, widest = ML.awzan_roots()
mapped = {r: (entries[r].get("semantic_axes") or "").strip()
          for r in awz if r in entries and (entries[r].get("semantic_axes") or "").strip()}
print("mapped roots:", len(mapped))
inmap = [i for i, r in enumerate(roots) if r in mapped]
print("positions in semantic field:", len(inmap))
print("distinct axes in field:", len({mapped[roots[i]] for i in inmap}))
print("distinct roots in field:", len({roots[i] for i in inmap}))
p = MG.reference_price()
print("price:", p["ثمنُ_الخريطة_بتًّا"], "mapped", p["مخرَّطة"])
import collections
print("top axes:", collections.Counter(mapped[roots[i]] for i in inmap).most_common(8))
