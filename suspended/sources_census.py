# sources_census.py — الوصلةُ بين التقشير والأختام: أوّلُ مقدارٍ مختومٍ مقيسٍ على غير المجمَّد.
#
# العلّةُ التي يقتلها هذا الملفّ: `normalize.py` تقشِّر الشهودَ المختومين، ولا محرّكَ يقرأ
# مقشورَها فيختم عليه — فكانت الأختامُ كلُّها مقيسةً على `mujammad.txt` وحدَه، و«البرنامجُ
# يتعلّم من المصادر» بنيةً منتظرةً لا دعوى جارية. وهذا الملفُّ يُغلق الوصلةَ بأصغرِ ما يُغلقها:
# يعدّ ما تُعطيه الطبقةُ الأولى بعد تقشير الثانية، ويُودِعه وديعةً لها أختامُها الحيّة.
#
# — وثلاثةُ قيودٍ لا يُطوى واحدٌ منها في الصمت —
#   ① **لا قياسَ على بايتةٍ غيرِ مصادَمة**: بصمةُ كلِّ شاهدٍ وطولُه يُقرآن من
#      `sources_manifest.tsv` ويُصادَمان بالملفّ الحاضر قبل تقشيره. مخالفةٌ ⟵ مخرجٌ 4.
#   ② **والغيابُ يُسمّى لا يُطوى**: شاهدٌ مُعلَنٌ في التعداد وبايتاتُه غائبةٌ عن الصندوق
#      يُسقط التشغيلَ بالمخرج 3 ويُدلّ على جلبه — ولا يُقاس على الحاضرين وحدَهم صامتًا،
#      فيصير العددُ دالّةَ ما صادف التنزيلُ بدل أن يكون دالّةَ التعداد المُعلَن.
#   ③ **ولا عدَّ هنا**: القياسُ كلُّه بـ`normalize.measure` — فلا نسخةَ ثانيةً للتصنيف
#      تتخلّف عن الطبقة الأولى صامتةً. وما لا تعدُّه تلك الدالّةُ لا يُدَّعى في وديعة.
#
# والتعدادُ مُعلَنٌ في `CENSUS` أدناه: شاهدان من الستّةَ عشرَ — لا «كلُّ ما في البيان»،
# فالقائمةُ المفتوحةُ تجعل الوديعةَ تتغيّر بزيادةِ سطرٍ في البيان بلا قرارٍ معلَن.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بايتاتُ شاهدٍ غائبةٌ عن الصندوق
#          · 4 بصمةٌ أو طولٌ خالف البيان.
# (المخرجُ 4 هو مخرجُ `fetch_source.sh` نفسُه للختم المخالف عمدًا: المخالفةُ واحدةٌ
#  في الطبقتين، وسمُّها واحدٌ — وما سواه مخارجُ هذه الطبقة وحدَها.)
#
# التشغيل:
#   python sources_census.py                    تقريرٌ معدودٌ على stdout
#   python sources_census.py --json <ملفّ>      الوديعةُ إلى ملفّ (مولِّدُ الأختام)
#   bash fetch_source.sh --fetch <معرِّف>        جلبُ البايتات (شبكةٌ — مرّةً واحدة)
import argparse
import hashlib
import json
import os
import sys

import normalize

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "sources_manifest.tsv")
SOURCES_DIR = os.path.join(ROOT, "corpora", "sources")

E_USAGE = 2
E_MISSING = 3
E_SEAL = 4

# الشهودُ المعدودون — معلَنون بأسمائهم لا بمسحِ البيان.
#   النحّاسُ أوّلًا لأنّه المقصود: إعرابُ القرآن شاهدًا نحويًّا لا قرآنًا مُجمَّدًا.
#   والألفيةُ معه شاهدًا ثانيًا مخالفًا في كلِّ شيء (97,798 بايتةً · بلا بوم · بلا «وصل»)
#   فلا يكون العدُّ مقيسًا على هيئةٍ واحدةٍ تُظَنُّ قانونًا.
CENSUS = ("nahhas_icrab_shamay", "ibnmalik_alfiyya")


class CensusError(Exception):
    """خطأٌ بمخرجٍ معلوم — يُصرَخ به ولا يُبتلَع."""

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def manifest_rows():
    """بيانُ الحقيقة الوحيد: عشرةُ حقولٍ في كلِّ سطرٍ غيرِ مُعلَّق."""
    rows = {}
    with open(MANIFEST, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            cells = line.rstrip("\n").split("\t")
            if len(cells) != 10:
                raise CensusError(
                    E_USAGE,
                    f"سطرٌ في البيان بـ{len(cells)} حقلًا لا عشرة: {cells[0]!r}")
            rows[cells[0]] = cells
    return rows


def sealed_bytes(source_id, rows):
    """البايتاتُ مصادَمةً: الطولُ ثمّ sha256 — ولا يُقشَّر ما لم يُصادَم."""
    row = rows.get(source_id)
    if row is None:
        raise CensusError(E_USAGE, f"معرِّفٌ ليس في البيان: «{source_id}»")
    length, digest = int(row[6]), row[7]
    path = os.path.join(SOURCES_DIR, f"{source_id}.txt")
    if not os.path.exists(path):
        raise CensusError(
            E_MISSING,
            f"«{source_id}»: بايتاتُه غائبةٌ عن الصندوق ({path}) — "
            f"تُجلَب بـ«bash fetch_source.sh --fetch {source_id}» ولا يُقاس على غيابٍ مطويّ")
    raw = open(path, "rb").read()
    if len(raw) != length:
        raise CensusError(
            E_SEAL,
            f"«{source_id}»: الطولُ {len(raw)} والبيانُ يعلن {length} — ختمٌ مخالف")
    got = hashlib.sha256(raw).hexdigest()
    if got != digest:
        raise CensusError(
            E_SEAL, f"«{source_id}»: البصمةُ {got} والبيانُ يعلن {digest} — ختمٌ مخالف")
    return path, got


def census_of(source_id, rows):
    """شاهدٌ ⟵ سجلُّه المعدود. القياسُ كلُّه بـnormalize.measure لا بعَدٍّ ثانٍ هنا."""
    path, digest = sealed_bytes(source_id, rows)
    try:
        m = normalize.measure(path)
    except normalize.NormalizeError as exc:
        # مخارجُ التقشير الخمسة تعبر كما هي: طبقتُها تحكم على نصِّها، ولا تُترجَم هنا.
        raise CensusError(exc.code, exc.message) from exc
    return {
        "بصمة": digest,
        "بايتات": m["بايتات"],
        "محارف": m["محارف"],
        "بوم": m["بوم"],
        "حقولُ الترويسة": len(m["ترويسة"]),
        "أسطر": m["أسطر"],
        "أصناف": m["أصناف"],
        "درجاتُ العناوين": {str(d): n for d, n in m["درجاتُ العناوين"].items()},
        "ترقيم": m["ترقيم"],
        "أوّلُ ترقيم": m["أوّلُ ترقيم"],
        "آخرُ ترقيم": m["آخرُ ترقيم"],
        "بلا ترقيم": m["بلا ترقيم"],
    }


def run(ids=CENSUS):
    """التعدادُ كلُّه — والشاهدُ الغائبُ يُسقط التشغيلَ ولا يُطرَح من المقام."""
    rows = manifest_rows()
    witnesses = {sid: census_of(sid, rows) for sid in ids}
    return {
        "تعدادُ_الشهود": witnesses,
        "الكلّ": {
            "شهود": len(witnesses),
            "بايتات": sum(w["بايتات"] for w in witnesses.values()),
            "محارف": sum(w["محارف"] for w in witnesses.values()),
            "أسطر": sum(w["أسطر"] for w in witnesses.values()),
            "ترقيم": sum(w["ترقيم"] for w in witnesses.values()),
        },
    }


def report(doc):
    for sid, w in doc["تعدادُ_الشهود"].items():
        print(f"— {sid} · {w['بصمة'][:12]}…")
        print(f"  بايتات {w['بايتات']:,} · محارف {w['محارف']:,} · "
              f"بوم {'نعم' if w['بوم'] else 'لا'} · أسطرُ متنٍ {w['أسطر']:,}")
        print("  أصناف: " + " · ".join(f"{k} {w['أصناف'][k]:,}" for k in normalize.KINDS))
        if w["بلا ترقيم"]:
            print("  الترقيم: **بلا ترقيم**")
        else:
            print(f"  الترقيم: {w['ترقيم']:,} موضعًا · "
                  f"من {w['أوّلُ ترقيم']} إلى {w['آخرُ ترقيم']}")
    k = doc["الكلّ"]
    print(f"\nالتعداد: {k['شهود']} شاهدًا · {k['بايتات']:,} بايتةً مصادَمةً · "
          f"{k['أسطر']:,} سطرَ متنٍ مقشورًا ✓")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="sources_census.py",
        description="تعدادُ الشهود المختومين بعد تقشيرهم — أوّلُ قياسٍ على غير المجمَّد",
    )
    ap.add_argument("--json", metavar="ملفّ", help="الوديعةُ إلى ملفّ")
    args = ap.parse_args(argv)
    try:
        doc = run()
    except CensusError as exc:
        print(f"صريخ: {exc.message}", file=sys.stderr)
        return exc.code
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    report(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
