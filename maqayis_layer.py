# maqayis_layer.py — طبقةُ إثراءٍ قرينيّة: جذورُ حلقة الأوزان مقابل «مقاييس اللغة».
# الحدُّ المعلن: هذا قاموسٌ دلاليّ-قرينيّ لا مصنِّفٌ صرفيّ — فلا يخفض ⚑ ولا يزيد الكلفة.
# غايتُه سؤالان معدودان: أمُدرَجٌ الجذرُ المستخرج في المقاييس؟ وبأيّ محاورَ دلالية؟
# البايتات لا تُودَع (5.5 م.ب، ومقامُها غيرُ مقامنا)؛ المودَع مِهرُها: البصمة والطول والمصدر.
# من خالف البصمة فليس الجدول، وغيابُه وضعٌ موسوم لا قياسٌ مؤجَّلٌ بصمت.
from collections import Counter
import csv, io, json, os, sys, hashlib, argparse

TABLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maqayis_by_root_csv_999.csv")
SEAL = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
SEAL_BYTES = 5539405
SOURCE = "Saleh1967/Alghanem@main:maqayis_by_root_csv_999.csv"
COLUMNS = ["root_full", "root_type", "entry_num", "root_display", "semantic_axes",
           "axes_count", "poetry_evidence", "body_text", "chapter_header"]
AWZAN_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "awzan_v0.json")
HAMZ = {"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا", "ى": "ا"}   # التسوية المعلنة بعينها في awzan_engine


def norm(root):
    return "".join(HAMZ.get(c, c) for c in root)


def read_table(path=TABLE):
    """البوّابة: الطولُ ثم البصمةُ من البايتات نفسها، قبل أيّ قراءةٍ أو عدّ."""
    data = open(path, "rb").read()
    if len(data) != SEAL_BYTES:
        raise SystemExit(f"صريخ: الطول {len(data)} ≠ {SEAL_BYTES} — ليس الجدول")
    got = hashlib.sha256(data).hexdigest()
    if got != SEAL:
        raise SystemExit(f"صريخ: البصمة {got} خالفت المختوم — ولا إثراء على بديلٍ صامت")
    rows = list(csv.DictReader(io.StringIO(data.decode("utf-8"), newline="")))
    if rows and list(rows[0]) != COLUMNS:
        raise SystemExit("صريخ: أعمدة الجدول خُولفت — بنيةٌ غيرُ المعلنة")
    return rows


def awzan_roots(path=AWZAN_JSON):
    """الجذور تُقرأ من وديعة حلقة الأوزان — لا استخراجَ ثانٍ يتخلّف عن الأول."""
    R = json.load(open(path, encoding="utf-8"))["الأوزان_v0"]
    return R["roots_widest"], R["widest"]


def run(table=TABLE, awzan=AWZAN_JSON):
    rows = read_table(table)
    roots, widest = awzan_roots(awzan)
    entries = {}
    for r in rows:
        entries.setdefault(r["root_full"], r)
    by_norm = {}
    for k, v in entries.items():
        by_norm.setdefault(norm(k), v)
    exact = [r for r in roots if r in entries]
    lenient = [r for r in roots if r not in entries and norm(r) in by_norm]
    missing = [r for r in roots if r not in entries and norm(r) not in by_norm]
    axes = Counter()
    for r in exact:
        a = (entries[r].get("semantic_axes") or "").strip()
        if a:
            axes[a] += 1
    return dict(
        note="طبقةُ إثراءٍ قرينيّة — لا تخفض ⚑ ولا تزيد الكلفة",
        source=SOURCE, sha256=SEAL, byte_length=SEAL_BYTES,
        table=dict(records=len(rows), distinct_roots=len(entries),
                   root_types=dict(Counter(r["root_type"] for r in rows).most_common())),
        awzan_layer=widest, awzan_roots=len(roots),
        matched_exact=len(exact),
        matched_lenient=len(lenient),                 # بتسوية الهمزات/الألفات المعلنة
        matched_total=len(exact) + len(lenient),
        pct_exact=round(len(exact) / len(roots) * 100, 2),
        pct_total=round((len(exact) + len(lenient)) / len(roots) * 100, 2),
        missing_count=len(missing),
        missing=missing,                              # النواقصُ بالاسم — لا عددٌ مجرّد
        axes_top=dict(axes.most_common(12)))


def main(argv=None):
    ap = argparse.ArgumentParser(description="طبقة الإثراء بالمقاييس — تدقيقٌ قرينيّ لا تصنيف")
    ap.add_argument("--json", help="مسار إيداع النتائج")
    ap.add_argument("--table", default=TABLE, help="مسار جدول المقاييس المختوم")
    a = ap.parse_args(argv)
    if not os.path.isfile(a.table):
        print(f"جدول المقاييس غائبٌ عن القرص — الإثراء مؤجَّلٌ ببصمته {SEAL[:12]}… "
              f"(المصدر {SOURCE} · ./fetch_maqayis.sh)")
        return 0
    R = run(a.table)
    print(f"جدول المقاييس بالبصمة ✓ — سجلّات {R['table']['records']:,} · "
          f"جذورٌ متمايزة {R['table']['distinct_roots']:,} · "
          + " · ".join(f"{k}={v:,}" for k, v in R["table"]["root_types"].items()))
    print(f"جذور حلقة الأوزان ({R['awzan_layer']}) = {R['awzan_roots']:,} | "
          f"مدرَجةٌ حرفيًّا {R['matched_exact']:,} ({R['pct_exact']}%) · "
          f"بتسوية الهمزات +{R['matched_lenient']:,} ⟹ {R['matched_total']:,} ({R['pct_total']}%)")
    print(f"⚑ قرينيّ — غيرُ مدرَجةٍ في المقاييس: {R['missing_count']:,} جذرًا "
          f"(أوّلها: {' · '.join(R['missing'][:10])})")
    print("المحاور الدلالية الأكثر: " + " · ".join(f"{k}={v}" for k, v in list(R["axes_top"].items())[:5]))
    print("الحدُّ المعلن: إثراءٌ وتدقيقٌ قرينيّ — ⚑ المعجم والكلفة لم تُمسّا")
    if a.json:
        json.dump({"المقاييس_v0": R}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2, sort_keys=True)
        print(f"JSON ⟵ {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
