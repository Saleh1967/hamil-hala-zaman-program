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
from deposit_law import ALPHA
print("ALPHA", ALPHA, "MIN_N", QG.MIN_N)

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
field = {i for i, a in enumerate(axis) if a}
forms_field = sorted({stream[i] for i in field})
print("صور الميدان", len(forms_field), "ثمن إعلانها", round(TG.declaration_cost(forms_field), 1))
p = MG.reference_price()
print("ثمن الخريطة", p["ثمنُ_الخريطة_بتًّا"], "مخرطة", p["مخرَّطة"])
AW = json.load(open("awzan_v0.json", encoding="utf-8"))["الأوزان_v0"]
print("ثمن جدول الأوزان", AW["table_cost_bits"])

hija, lafz, ma3na = QG.lafz_names()
lafzforms = {DG.fold(n) for n in set(hija) | set(lafz)}
lafzpos = {i for i, s in enumerate(stream) if s in lafzforms}
print("مواضع اللفظ", len(lafzpos), "تقاطع مع الميدان", len(lafzpos & field))

def bill(forms, fire, tag):
    try:
        b = TG.rule_bill(stream, tuple(forms), fire, random.Random(TG.CONTROL_SEED))
        print(f"  {tag:<34} إطلاق {b['إطلاق']:>6} نصيب {b['نصيب']:<8} Δ {b['Δ']:>12,.1f} ضابط {b['ضابط']:>12,.1f}  {b['حكم']}")
        return b
    except TG.Ta3allumError as e:
        print(f"  {tag:<34} صريخ: {e.message}")
        return None

print("— فصلُ المعنى واللفظ بمكيال الوضع —")
bill(forms_field, set(field), "خانةُ «مدلولُه معنًى»")
bill(forms_field, set(lafzpos), "خانةُ «مدلولُه لفظ»")
print("— فصلُ المستعمَلِ والمهمَل بمكيال الوضع —")
usedfire = set(field)
print("   قاطعُ المستعمَلِ == قاطعُ المعنى ?", usedfire == field)
bill(forms_field, {i for i in range(len(stream)) if i not in field}, "خانةُ «مهمَل» (لا وضعَ له)")
print("— مكيالٌ مصنوع: مدلولٌ يبدأ بأوّل حرفٍ من إحدى الصور —")
ranked = AG.imam_ranking(cands, AG.imam_folded())
for k in AG.RUNGS:
    F = sorted(cands, key=lambda c: (-ranked[c], c))[:k]
    Fs = set(F)
    heads = {f[0] for f in F if f}
    fk = {i for i in field if stream[i] not in Fs and axis[i] and axis[i][0] in heads}
    bill(F, fk, f"المصطنعةُ بالمدلول درج {k}")
    fs = AG.fire_of_rank(AG.FABRICATED_RANK["رتبة"], stream, F)
    bill(F, fs, f"المصطنعةُ بالصورة درج {k}")
