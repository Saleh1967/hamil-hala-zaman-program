# burhan/run_all.py — المُشغِّل: يجمع الشهادات ويودعها، ولا يقيس بنفسه رقمًا واحدًا.
#
# الاستقلالُ محفوظ: الشهاداتُ تُشغَّل **عمليّاتٍ منفصلة** لا تُستورَد، فلا تُصادِق إحداها
# أختَها بمشاركةِ ذاكرة. وما يفعله المُشغِّلُ زيادةً على الجمع شيئان:
#   ① مصادمةُ الثوابت المكرَّرة عبر الملفّات بـ`ast` — فالاستقلالُ ثمنُه التكرار، وثمنُ
#      التكرارِ انزياحٌ صامت؛ فيُقتَل بالمصادمة لا بالرجاء.
#   ② ختمُ البيت: `SHA256SUMS.txt` يُولَّد ويُتحقَّق منه بـ`--check`، ويستثني نفسَه.
import argparse, ast, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUMS = os.path.join(HERE, "SHA256SUMS.txt")
DEPOSIT = os.path.join(HERE, "burhan_v0.json")
TOKENS = os.path.join(HERE, "TOKENS-112.json")

CERTS = [
    ("CERT-CORPUS", ["cert_corpus.py"]),
    ("CERT-PARTITION", ["cert_partition.py"]),
    ("CERT-GENERATIONS", ["cert_generations.py"]),
    ("CERT-FINGERPRINTS", ["cert_fingerprints.py", "--table", TOKENS]),
    ("CERT-INERTNESS", ["cert_inertness.py"]),
    ("CERT-NORMALIZE", ["cert_normalize.py"]),
    ("CERT-SUKUN", ["cert_sukun.py"]),
    ("CERT-W2", ["cert_boundary.py"]),
]

# ثوابتُ مكرَّرةٌ بالضرورة (الاستقلالُ يمنع الاستيراد) — فتُصادَم قيمُها هنا صفًّا إلى صفّ.
SHARED = ("BASE28", "SEAL_SHA256", "SUKUN", "SHADDA", "DAGGER", "BARE", "AR_RANGES",
          "VOWELS", "TANWIN", "STATES4", "LAM_AMR")


def literals(path):
    """قيمُ الثوابت المعلنةِ في أعلى الملفّ — بـ`ast` لا بمشطِ البايتات.

    وتُفَكُّ نداءاتُ `list/set/tuple` على قيمةٍ حرفيّة، وإلّا لأفلت `BASE28 = list("…")`
    من المصادمة فصار الحارسُ يعدّ ثوابتَ لا يقارنها — وهذا بابُ الانزياح الصامت بعينه.
    """
    tree = ast.parse(open(path, encoding="utf-8").read(), os.path.basename(path))
    wrap = {"list": list, "set": set, "tuple": tuple, "frozenset": frozenset}
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in SHARED:
            value = node.value
            fn = None
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) \
                    and value.func.id in wrap and len(value.args) == 1:
                fn, value = wrap[value.func.id], value.args[0]
            try:
                got = ast.literal_eval(value)
            except ValueError:
                continue
            out[node.targets[0].id] = fn(got) if fn else got
    return out


def canonical(value):
    """صورةٌ واحدةٌ للمقارنة — والترتيبُ محفوظٌ في المتسلسلات لأنّ التوكنَ موضعٌ في تعداد."""
    if isinstance(value, dict):
        return ("dict",) + tuple(sorted((str(k), str(v)) for k, v in value.items()))
    if isinstance(value, (set, frozenset)):
        return ("set",) + tuple(sorted(str(v) for v in value))
    if isinstance(value, (list, tuple)):
        return ("seq",) + tuple(canonical(v) for v in value)
    return value


def collide_constants():
    """انزياحُ نسخةٍ عن أختها صريخٌ — بالقيمة في صورتها الواحدة، لا بتشابه الاسم."""
    seen, problems = {}, []
    for fname in sorted(os.listdir(HERE)):
        if not fname.startswith("cert_") or not fname.endswith(".py"):
            continue
        for name, value in literals(os.path.join(HERE, fname)).items():
            key = canonical(value)
            if name in seen and seen[name][1] != key:
                problems.append(f"الثابتُ «{name}» انزاح بين {seen[name][0]} و{fname}")
            seen.setdefault(name, (fname, key))
    return problems, sorted(seen)


def write_sums():
    rows = []
    for base, _dirs, files in os.walk(HERE):
        for fn in sorted(files):
            if fn == os.path.basename(SUMS) or "__pycache__" in base:
                continue
            path = os.path.join(base, fn)
            rel = os.path.relpath(path, HERE)
            with open(path, "rb") as fh:
                rows.append(f"{hashlib.sha256(fh.read()).hexdigest()}  {rel}")
    rows.sort(key=lambda r: r.split("  ", 1)[1])
    with open(SUMS, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(rows) + "\n")
    return len(rows)


def check_sums():
    problems = []
    if not os.path.exists(SUMS):
        return ["لا ختمَ للبيت — SHA256SUMS.txt غائب"]
    declared = {}
    for ln in open(SUMS, encoding="utf-8"):
        if ln.strip():
            digest, rel = ln.rstrip("\n").split("  ", 1)
            declared[rel] = digest
    found = set()
    for base, _dirs, files in os.walk(HERE):
        for fn in files:
            if fn == os.path.basename(SUMS) or "__pycache__" in base:
                continue
            rel = os.path.relpath(os.path.join(base, fn), HERE)
            found.add(rel)
            with open(os.path.join(base, fn), "rb") as fh:
                got = hashlib.sha256(fh.read()).hexdigest()
            if rel not in declared:
                problems.append(f"ملفٌّ بلا ختم: {rel}")
            elif declared[rel] != got:
                problems.append(f"ختمٌ خُولِف: {rel}")
    for rel in sorted(set(declared) - found):
        problems.append(f"ختمٌ لملفٍّ غائب: {rel}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="يتحقّق من الختم ولا يُجدِّده")
    ap.add_argument("--json", default=DEPOSIT)
    args = ap.parse_args()

    shifts, shared = collide_constants()
    for p in shifts:
        print(f"::error::{p}")

    results, fails = {}, list(shifts)
    for name, argv in CERTS:
        tmp = os.path.join(HERE, f".{name}.tmp.json")
        run = subprocess.run([sys.executable, os.path.join(HERE, argv[0])] + argv[1:]
                             + ["--json", tmp], cwd=HERE, capture_output=True, text=True)
        sys.stdout.write(run.stdout)
        if run.stderr.strip():
            sys.stdout.write(run.stderr)
        if run.returncode != 0:
            fails.append(f"{name}: سقطت")
        with open(tmp, encoding="utf-8") as fh:
            results[name] = json.load(fh)
        os.remove(tmp)

    deposit = {
        "البرهان_v0": {
            "المدوّنة": "mujammad.txt — مختومةٌ، والتحقُّقُ قبل كلِّ عدّ",
            "شهادات": results,
            "ثوابتُ_مُصادَمةٌ_عبر_الملفّات": shared,
            "مقيس": {
                "شهاداتٌ_خضراء": sum(1 for r in results.values() if r["حكم"] == "خضراء"),
                "شهادات": len(results),
                "أعدادٌ_مُشتَقّةٌ_ههنا": sum(len(r.get("مقيس", {})) for r in results.values()),
            },
            "مفتوحات": [
                "رخصةُ Φ على المطبوع — مقيسةٌ لا مرخَّصة (CERT-SUKUN)",
                "اختيارُ الزائدين بين إصلاحَي القسمة — لسانيٌّ خارجَ الجبر، وخمولُه مُبرهَن",
                "الشرطُ الزمنيُّ «المتوقَّعُ قبل التشغيل» — تُثبته سجلاتُ الإيداع لا البصمات",
                "قيدُ «الخاتمةُ الساكنةُ شاذّةٌ صغيرة» ساقطٌ بعدده 8,843 (CERT-W2/③) — "
                "لا يُصحَّح صمتًا بل يُعاد إعلانُه بندًا متوقَّعًا جديدًا",
                "بندُ فصلِ الخاتمةِ عن موضع الإعراب معلَّقٌ (CERT-W2/⑤) — رقمٌ معروضٌ لا محتجٌّ به",
            ],
        }
    }
    with open(args.json, "w", encoding="utf-8") as fh:
        json.dump(deposit, fh, ensure_ascii=False, indent=1)

    if args.check:
        fails.extend(check_sums())
        print(f"— ختمُ البيت: تحقُّقٌ من {os.path.basename(SUMS)} —")
    else:
        n = write_sums()
        print(f"— ختمُ البيت: {n} ملفًّا مختومًا في {os.path.basename(SUMS)} —")

    green = sum(1 for r in results.values() if r["حكم"] == "خضراء")
    print(f"— البرهان: {green}/{len(results)} شهادةً خضراء · "
          f"{len(shared)} ثابتًا مُصادَمًا عبر الملفّات —")
    for f in fails:
        print(f"::error::{f}")
    print("    ✓ البيتُ مغلق" if not fails else "    ✗ البيتُ مفتوح")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
