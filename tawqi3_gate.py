# tawqi3_gate.py — بابُ التوقيع: «بتوقيعِ مَن خُتم ما رفعه المالك؟»
#
# العلّةُ التي يقتلها هذا الملفّ: طريقُ `self` في `fetch_source.sh` يَختِم بايتاتِ
# ما رفعه المالكُ ختمًا ثلاثيًّا (بصمةُ كائنٍ · طولٌ · sha256)، ويشترط في الختم
# `SOURCES_SEAL_OWNER=1`. وهذا الشرطُ **دعوى المُشغِّل لا توقيعُ المالك**: متغيّرُ
# بيئةٍ يكتبه كلُّ من يشغّل السكربت. فالختمُ يُثبت أنّ البايتاتِ هي هي، ولا يُثبت
# أنّ المالكَ هو الذي أدخلها.
#
# والتوقيعُ الحقيقيُّ موجودٌ ومهمَلٌ في الوقت نفسِه: إيداعاتُ الرفع في هذه الشجرة
# موقَّعةٌ معمّاةً (`gpgsig` في كائن الإيداع). فهذا البابُ يقرأ ذلك التوقيعَ
# ويتحقَّق منه بالحساب، ويصِل به السلسلةَ إلى البايتات المختومة.
#
# — والقيودُ التي لا يُطوى واحدٌ منها في الصمت —
#
#   ① **السلسلةُ موصولةٌ حلقةً حلقة**: التوقيعُ لا يقع على الملفّ، بل على كائن
#      الإيداع. فلا يُقبَل «موقَّعٌ» حكمًا على مصدرٍ حتى تُقاس الحلقاتُ الخمسُ
#      كلُّها: توقيعٌ صحيح ⟵ إيداعٌ ⟵ شجرتُه عند المسار المختوم ⟵ كائنٌ بصمتُه
#      هي المختومة ⟵ بايتاتٌ sha256‑ها هي المختومة. وانقطاعُ حلقةٍ يُسقِط الحكمَ
#      كلَّه، ولا يُرقَّع بالباقي.
#
#   ② **الحمولةُ تُبنى بالقاعدة لا بالنمط**: حمولةُ التوقيع في git هي كائنُ
#      الإيداع منزوعًا منه ترويسةُ `gpgsig` وأسطرُها التابعة (المبدوءةُ بفراغ).
#      تُبنى ههنا سطرًا سطرًا لا بتعبيرٍ نمطيٍّ يُصيب ويُخطئ.
#
#   ③ **المفتاحُ مودَعٌ في الشجرة مثبَّتًا**: لا يُجلَب من شبكةٍ عند التحقُّق —
#      فيُتحقَّق ولو حُجبت الشبكةُ كلُّها. وهو مثبَّتٌ بوجهَين: sha256 بايتاته
#      وبصمةُ المفتاح الكاملة. وتبدُّلُ أيِّهما صريخٌ **قبل** أن يُستعمَل.
#
#   ④ **الحكمُ أربعٌ لا اثنتان**: «موقَّعٌ موصولٌ · موقَّعٌ مقطوع · غيرُ موقَّع
#      · إيداعٌ غائب». وثلاثتُها بعد الأولى تُسقِط البابَ، وتُسمّى مفترقةً لأنّ
#      علاجَها مفترق: المقطوعُ ختمٌ خالف، وغيرُ الموقَّع بابُ المالك دخل منه ما
#      لا يحمل توقيعَه، والغائبُ بيانٌ يذكر إيداعًا ليس في التاريخ. ولا يُخلَط
#      الغيابُ عن التاريخ بالغياب عن التوقيع.
#
#   ⑤ **والدَّينُ الأثقل يُسمّى في صدر الوديعة**: مفتاحُ التوقيع مفتاحُ GitHub
#      (`web-flow`) لا مفتاحُ المالك. فالتوقيعُ **وكالةٌ لا أصالة**: تشهد به
#      GitHub أنّ صاحبَ الحساب أدخل البايتاتِ من جلسةٍ موثَّقة، ولا يشهد أنّ
#      مفتاحًا في يد المالك وقّعها. والفرقُ لا يُطوى: من ملكَ الحسابَ ملكَ
#      التوقيعَ. ورفعُ هذا الدَّين عملٌ بيد المالك وحدَه — أن يوقّع بمفتاحه.
#
# المخارج: 0 نجاح · 2 خطأُ استعمال · 3 بيانٌ أو مفتاحٌ أو أداةٌ غائبة
#          · 4 ختمٌ خالف · 5 سلسلةٌ انقطعت وادُّعي وصلُها.
#
# التشغيل:
#   python tawqi3_gate.py                     تقريرٌ معدودٌ على stdout
#   python tawqi3_gate.py --json <ملفّ>       الوديعةُ إلى ملفّ
#   python tawqi3_gate.py --doc [ملفّ]        الوثيقةُ المولَّدة (TAWQI3.md)
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "sources_manifest.tsv")
KEYRING = os.path.join(ROOT, "keys", "github-web-flow.asc")
DOC = os.path.join(ROOT, "TAWQI3.md")
CONTRACT = "SOURCES.md"

E_USAGE = 2
E_MISSING = 3
E_SEAL = 4
E_CHAIN = 5

# ① المفتاحُ مثبَّتٌ بوجهَين — بايتاتُه وبصمتُه. لا يُستعمَل قبل أن يُصادَما.
KEYRING_SHA256 = "6e8af687f60cf3f403151c8fb1b26e95e6f9e424ca60cc8f3787bd4466a3ef84"
KEYRING_BYTES = 2483
# بصمةُ المفتاح الموقِّع الكاملةُ — أربعون محرفًا، لا مُعرِّفٌ قصيرٌ يُصطدَم به.
SIGNING_FPR = "968479A1AFF927E37D1A566BB5690EEEBB952194"
SIGNING_UID = "GitHub <noreply@github.com>"

# ⑤ الدَّينُ الأثقلُ مكتوبٌ قبل القياس، لا يُستنتَج من نتيجةٍ بعدَه.
WAKALA = ("مفتاحُ التوقيع مفتاحُ GitHub لا مفتاحُ المالك — فالتوقيعُ وكالةٌ لا "
          "أصالة: يشهد أنّ البايتاتِ دخلت من جلسةِ حسابٍ موثَّقة، ولا يشهد أنّ "
          "مفتاحًا في يد المالك وقّعها")

FIELDS = ("id", "repo", "ref", "pattern", "path", "blob", "bytes", "sha256",
          "state", "note")


class TawqiError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ═══ أدواتٌ صغيرة ═══════════════════════════════════════════════════════════

def _git(*args, binary=True):
    out = subprocess.run(("git", "-C", ROOT) + args,
                         capture_output=True)
    if out.returncode != 0:
        return None
    return out.stdout if binary else out.stdout.decode("utf-8", "replace")


def manifest_rows():
    if not os.path.exists(MANIFEST):
        raise TawqiError(E_MISSING, f"البيانُ غائب: {MANIFEST}")
    rows = []
    with open(MANIFEST, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != len(FIELDS):
                raise TawqiError(E_SEAL,
                                 f"سطرٌ بـ{len(parts)} حقلًا لا {len(FIELDS)}")
            rows.append(dict(zip(FIELDS, parts)))
    return rows


def split_commit(raw):
    """② الحمولةُ والتوقيعُ — سطرًا سطرًا بقاعدة git لا بنمط."""
    lines = raw.split(b"\n")
    payload, sig, i, n = [], [], 0, len(lines)
    while i < n:
        line = lines[i]
        if line.startswith(b"gpgsig ") and not sig:
            sig.append(line[len(b"gpgsig "):])
            i += 1
            while i < n and lines[i].startswith(b" "):
                sig.append(lines[i][1:])
                i += 1
            continue
        payload.append(line)
        i += 1
    return b"\n".join(payload), (b"\n".join(sig) + b"\n" if sig else b"")


def keyring_station():
    """③ المفتاحُ يُصادَم بوجهَين قبل أن يُستعمَل."""
    if not os.path.exists(KEYRING):
        raise TawqiError(E_MISSING, f"المفتاحُ غائب: {KEYRING}")
    raw = open(KEYRING, "rb").read()
    got_sha = hashlib.sha256(raw).hexdigest()
    if len(raw) != KEYRING_BYTES:
        raise TawqiError(E_SEAL,
                         f"طولُ المفتاح {len(raw)} خالف الختمَ {KEYRING_BYTES}")
    if got_sha != KEYRING_SHA256:
        raise TawqiError(E_SEAL, f"بصمةُ المفتاح {got_sha} خالفت الختمَ")
    if shutil.which("gpg") is None or shutil.which("gpgv") is None:
        raise TawqiError(E_MISSING, "gpg/gpgv غيرُ موجودَين — لا يُحزَر التحقُّق")
    fprs = []
    show = subprocess.run(("gpg", "--show-keys", "--with-colons", KEYRING),
                          capture_output=True)
    for line in show.stdout.decode("utf-8", "replace").splitlines():
        if line.startswith("fpr:"):
            fprs.append(line.split(":")[9])
    if SIGNING_FPR not in fprs:
        raise TawqiError(E_SEAL,
                         f"بصمةُ الموقِّع {SIGNING_FPR} ليست في حلقة المفاتيح")
    return {"بايتات": len(raw), "sha256": got_sha,
            "مفاتيحُ الحلقة": len(fprs), "بصمةُ الموقِّع": SIGNING_FPR,
            "هويّةُ الموقِّع": SIGNING_UID}


def dearmor(dest):
    raw = open(KEYRING, "rb").read()
    out = subprocess.run(("gpg", "--dearmor"), input=raw, capture_output=True)
    if out.returncode != 0 or not out.stdout:
        raise TawqiError(E_MISSING, "تعذَّر فكُّ درع المفتاح")
    with open(dest, "wb") as fh:
        fh.write(out.stdout)
    return dest


def verify(payload, sig, keyring):
    """يُرجِع (صحيح?، معرِّفُ المفتاح، السطرُ الأخير من gpgv)."""
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "payload.bin")
        s = os.path.join(tmp, "sig.asc")
        with open(p, "wb") as fh:
            fh.write(payload)
        with open(s, "wb") as fh:
            fh.write(sig)
        out = subprocess.run(("gpgv", "--keyring", keyring, s, p),
                             capture_output=True)
    text = out.stderr.decode("utf-8", "replace")
    keyid = ""
    for line in text.splitlines():
        if "using" in line and "key" in line:
            keyid = line.strip().split()[-1]
    return out.returncode == 0, keyid, text.strip().splitlines()[-1:]


# ═══ ① السلسلةُ حلقةً حلقة ═══════════════════════════════════════════════════

def chain_of(row, keyring):
    """توقيعٌ ⟵ إيداعٌ ⟵ شجرةٌ ⟵ كائنٌ ⟵ بايتات. كلُّ حلقةٍ مقيسةٌ مسمّاة."""
    links, ref, path = [], row["ref"], row["path"]

    raw = _git("cat-file", "commit", ref)
    links.append({"حلقة": "الإيداعُ حاضرٌ في التاريخ",
                  "موصولة": raw is not None,
                  "قيمة": ref})
    if raw is None:
        return links, None

    payload, sig = split_commit(raw)
    links.append({"حلقة": "الإيداعُ يحمل توقيعًا",
                  "موصولة": bool(sig), "قيمة": f"{len(sig)} بايتَ درع"})
    if not sig:
        return links, None

    ok, keyid, tail = verify(payload, sig, keyring)
    links.append({"حلقة": "التوقيعُ صحيحٌ بالمفتاح المثبَّت",
                  "موصولة": ok, "قيمة": keyid or "—"})

    # الحلقةُ الرابعة: شجرةُ الإيداع عند المسار المختوم تُعطي بصمةَ الكائن.
    got = _git("rev-parse", f"{ref}:{path}", binary=False)
    got = got.strip() if got else ""
    links.append({"حلقة": "المسارُ في شجرة الإيداع يُعطي الكائنَ المختوم",
                  "موصولة": got == row["blob"],
                  "قيمة": got or "—"})

    # الحلقةُ الخامسة: بايتاتُ الكائن sha256‑ها هي المختومة، وطولُها المختوم.
    blob = _git("cat-file", "blob", f"{ref}:{path}") if got else None
    sha = hashlib.sha256(blob).hexdigest() if blob is not None else ""
    links.append({"حلقة": "بايتاتُ الكائن تُعطي الطولَ وsha256 المختومَين",
                  "موصولة": (blob is not None
                             and str(len(blob)) == row["bytes"]
                             and sha == row["sha256"]),
                  "قيمة": f"{len(blob) if blob is not None else 0} · {sha or '—'}"})
    return links, keyid


def verdict(links):
    # الإيداعُ المعدومُ ينهي السلسلةَ عند حلقةٍ واحدة، فلا يُفهرَس ما لم يُقَس.
    # وغيابُ الإيداع ليس «غيرَ موقَّع»: ذاك دَينٌ مسمًّى وهذا بيانٌ معطوب.
    if not links or not links[0]["موصولة"]:
        return "إيداعٌ غائب"
    if len(links) < 2 or not links[1]["موصولة"]:
        return "غيرُ موقَّع"
    return "موقَّعٌ موصول" if all(x["موصولة"] for x in links) else "موقَّعٌ مقطوع"


# ═══ محاولاتُ التكذيب — تُشغَّل ولا تُقرَأ ════════════════════════════════════

def falsify(keyring, sample):
    """كلُّ محاولةٍ تُنتظَر أن تُردَّ؛ ونجاحُ واحدةٍ يُسقِط البابَ."""
    T = []
    payload, sig = sample

    def add(name, succeeded):
        T.append({"محاولة": name, "نجحت": bool(succeeded)})

    # ① بايتةٌ مقلوبةٌ في الحمولة تمرُّ
    bad = bytearray(payload)
    bad[len(bad) // 2] ^= 0x01
    add("بايتةٌ مقلوبةٌ في الحمولة تمرُّ",
        verify(bytes(bad), sig, keyring)[0])

    # ② حمولةٌ خاويةٌ تمرُّ
    add("حمولةٌ خاويةٌ تمرُّ", verify(b"", sig, keyring)[0])

    # ③ توقيعٌ مبتورٌ يمرُّ
    add("توقيعٌ مبتورٌ يمرُّ", verify(payload, sig[:len(sig) // 2], keyring)[0])

    # ④ حلقةُ مفاتيحَ خاويةٌ تمرُّ
    with tempfile.TemporaryDirectory() as tmp:
        empty = os.path.join(tmp, "empty.kbx")
        with open(empty, "wb") as fh:
            fh.write(b"")
        add("حلقةُ مفاتيحَ خاويةٌ تمرُّ", verify(payload, sig, empty)[0])

    # ⑤ الترويسةُ المنزوعةُ تُعاد فتمرُّ (الحمولةُ بترويسة gpgsig)
    add("الحمولةُ بترويسة gpgsig تمرُّ",
        verify(payload + b"\ngpgsig x", sig, keyring)[0])

    # ⑥ مفتاحٌ مختلَقٌ في التثبيت يمرُّ بلا صريخ
    global SIGNING_FPR
    keep = SIGNING_FPR
    SIGNING_FPR = "0" * 40
    try:
        keyring_station()
        add("بصمةُ موقِّعٍ مختلَقةٌ تمرُّ بلا صريخ", True)
    except TawqiError:
        add("بصمةُ موقِّعٍ مختلَقةٌ تمرُّ بلا صريخ", False)
    finally:
        SIGNING_FPR = keep

    # ⑦ ختمُ المفتاح المخالفُ يمرُّ بلا صريخ
    global KEYRING_SHA256
    keep_sha = KEYRING_SHA256
    KEYRING_SHA256 = "f" * 64
    try:
        keyring_station()
        add("sha256 مفتاحٍ مخالفةٌ تمرُّ بلا صريخ", True)
    except TawqiError:
        add("sha256 مفتاحٍ مخالفةٌ تمرُّ بلا صريخ", False)
    finally:
        KEYRING_SHA256 = keep_sha

    # ⑧ كائنٌ خارجَ شجرة الإيداع يُقبَل في السلسلة
    forged = {"ref": "HEAD", "path": "SOURCES.md", "blob": "0" * 40,
              "bytes": "0", "sha256": "0" * 64}
    lk, _ = chain_of(forged, keyring)
    add("كائنٌ لا تُعطيه الشجرةُ يُقبَل موصولًا", verdict(lk) == "موقَّعٌ موصول")

    # ⑨ مسارٌ معدومٌ يُقبَل موصولًا
    ghost = dict(forged, path="لا-وجود-له.txt")
    lk, _ = chain_of(ghost, keyring)
    add("مسارٌ معدومٌ يُقبَل موصولًا", verdict(lk) == "موقَّعٌ موصول")

    # ⑩ إيداعٌ مختلَقٌ يُقرأ
    lk, _ = chain_of(dict(forged, ref="0" * 40), keyring)
    add("إيداعٌ مختلَقٌ يُقرأ", lk[0]["موصولة"])

    # ⑪ الفاصلُ سطريٌّ لا نمطيّ: سطرُ متنٍ يبدأ بـgpgsig لا يُبتلَع مع الترويسة
    fake = (b"tree " + b"0" * 40 + b"\ngpgsig -----BEGIN-----\n"
            b" armor\n\nmatn\ngpgsig fi-l-matn\n")
    p2, s2 = split_commit(fake)
    add("سطرُ متنٍ يبدأ بـgpgsig يُبتلَع مع الترويسة",
        b"gpgsig fi-l-matn" not in p2)

    # ⑫ الدرعُ يُنتزَع بأسطره التابعة: لا يبقى سطرُ درعٍ في الحمولة
    add("سطرُ درعٍ يبقى في الحمولة", b"armor" in p2)

    return T


# ═══ التشغيل ═══════════════════════════════════════════════════════════════

def contract_count(name):
    path = os.path.join(ROOT, CONTRACT)
    if not os.path.exists(path):
        raise TawqiError(E_MISSING, f"سطرُ العقد غائب: {CONTRACT}")
    for line in open(path, encoding="utf-8"):
        if line.startswith(f"| {name} |"):
            cell = line.split("|")[2].strip()
            if cell.isdigit():
                return int(cell)
    return None


def run():
    key = keyring_station()
    rows = manifest_rows()
    selves = [r for r in rows if r["repo"] == "self"]
    if not selves:
        raise TawqiError(E_MISSING, "لا سطرَ على طريق self في البيان")

    with tempfile.TemporaryDirectory() as tmp:
        keyring = dearmor(os.path.join(tmp, "ring.kbx"))

        sources, sample = [], None
        for row in selves:
            links, keyid = chain_of(row, keyring)
            v = verdict(links)
            if sample is None and len(links) > 1 and links[1]["موصولة"]:
                sample = split_commit(_git("cat-file", "commit", row["ref"]))
            sources.append({
                "مصدر": row["id"], "ملفّ": row["path"], "إيداع": row["ref"],
                "مفتاحٌ موقِّع": keyid or "—", "حكم": v,
                "حلقات": links,
                "حلقاتٌ موصولة": sum(1 for x in links if x["موصولة"]),
                "حلقاتٌ مقيسة": len(links),
            })

        if sample is None:
            raise TawqiError(E_MISSING, "لا إيداعَ موقَّعًا تُبنى منه المحاولات")
        trials = falsify(keyring, sample)

    joined = [s for s in sources if s["حكم"] == "موقَّعٌ موصول"]
    cut = [s for s in sources if s["حكم"] == "موقَّعٌ مقطوع"]
    unsigned = [s for s in sources if s["حكم"] == "غيرُ موقَّع"]
    absent = [s for s in sources if s["حكم"] == "إيداعٌ غائب"]

    # ④ الانقطاعُ لا يُطوى: مقطوعٌ واحدٌ يُسقِط البابَ بـE_CHAIN.
    fails = []
    if cut:
        fails.append("① سلسلةٌ انقطعت: "
                     + " · ".join(s["مصدر"] for s in cut))
    if unsigned:
        fails.append("③ سطرٌ على طريق self بإيداعٍ بلا توقيع: "
                     + " · ".join(s["مصدر"] for s in unsigned))
    if absent:
        fails.append("④ إيداعٌ مذكورٌ في البيان غائبٌ من التاريخ: "
                     + " · ".join(s["مصدر"] for s in absent))
    passed = [t for t in trials if t["نجحت"]]
    if passed:
        fails.append("② محاولةُ تكذيبٍ نجحت: "
                     + " · ".join(t["محاولة"] for t in passed))

    sealed = contract_count("شهودٌ مختومون")
    debts = [
        {"دَين": "التوقيعُ وكالةٌ لا أصالة", "بيان": WAKALA,
         "الطريق": "أن يوقّع المالكُ بمفتاحٍ في يده، ويُثبَّت هنا بصمتُه"},
        {"دَين": "التوقيعُ لا يُؤرِّخ المتن",
         "بيان": "التوقيعُ يشهد لوقتِ الرفع لا لوقتِ التأليف — فتاريخُ الكتاب "
                 "في متنه خبرٌ غيرُ مختوم",
         "الطريق": "شاهدٌ خارجيٌّ مختومٌ يُصادَم به التاريخُ المكتوب"},
        {"دَين": "طريقا local والبعيدِ بلا توقيع",
         "بيان": "هذا البابُ يقيس طريقَ self وحدَه — وما جاء من شبكةٍ أو من "
                 "صندوق الوارد لا توقيعَ عليه أصلًا، فلا يُقاس ولا يُدَّعى",
         "الطريق": "لا طريقَ ما دام المصدرُ بلا إيداعٍ موقَّعٍ في هذه الشجرة"},
    ]

    return {
        "التوقيع_v0": {
            "المفتاح": key,
            "مقيس": {
                "سطورٌ على طريق self": len(selves),
                "موقَّعٌ موصول": len(joined),
                "موقَّعٌ مقطوع": len(cut),
                "غيرُ موقَّع": len(unsigned),
                "إيداعٌ غائب": len(absent),
                "حلقاتٌ مقيسةٌ لكلِّ مصدر": 5,
                "محاولاتُ_تكذيب": len(trials),
                "محاولاتٌ نجحت": len(passed),
                "شهودٌ مختومون في سطر العقد": sealed,
                "ديونٌ مسمّاة": len(debts),
            },
            "المصادر": sources,
            "الديون": debts,
            "محاولاتُ_التكذيب": trials,
            "سقوط": fails,
        }
    }


def show(R):
    A = R["التوقيع_v0"]
    M = A["مقيس"]
    print("بابُ التوقيع — بتوقيعِ مَن خُتم ما رفعه المالك؟")
    k = A["المفتاح"]
    print(f"  المفتاحُ المثبَّت: {k['بصمةُ الموقِّع']} · {k['هويّةُ الموقِّع']}")
    print(f"    بايتاتُه {k['بايتات']} · sha256 {k['sha256'][:16]}…")
    print("  ① السلسلةُ حلقةً حلقة (خمسُ حلقاتٍ لكلِّ مصدر):")
    for s in A["المصادر"]:
        print(f"    {s['مصدر']} — {s['حكم']} "
              f"({s['حلقاتٌ موصولة']}/{s['حلقاتٌ مقيسة']}) · {s['مفتاحٌ موقِّع']}")
        for lk in s["حلقات"]:
            mark = "✓" if lk["موصولة"] else "✗"
            print(f"        {mark} {lk['حلقة']}: {lk['قيمة']}")
    print(f"  ② موصولٌ {M['موقَّعٌ موصول']} · مقطوعٌ {M['موقَّعٌ مقطوع']} "
          f"· غيرُ موقَّعٍ {M['غيرُ موقَّع']} · إيداعٌ غائبٌ {M['إيداعٌ غائب']}")
    print(f"  ③ الديون — تُسمّى ولا تُسعَّر ({M['ديونٌ مسمّاة']}):")
    for d in A["الديون"]:
        print(f"      • {d['دَين']}")
    print(f"  محاولاتُ تكذيبٍ رُدَّت: "
          f"{M['محاولاتُ_تكذيب'] - M['محاولاتٌ نجحت']}/{M['محاولاتُ_تكذيب']}")
    for f in A["سقوط"]:
        print(f"::error::{f}")
    if A["سقوط"]:
        print(f"    ✗ موصولٌ {M['موقَّعٌ موصول']} من {M['سطورٌ على طريق self']}")
    else:
        print(f"    ✓ موصولٌ {M['موقَّعٌ موصول']} من "
              f"{M['سطورٌ على طريق self']} · محاولاتٌ رُدَّت كلُّها")


def write_doc(R, path):
    A = R["التوقيع_v0"]
    M = A["مقيس"]
    k = A["المفتاح"]
    L = ["# بابُ التوقيع — بتوقيعِ مَن خُتم ما رفعه المالك؟", "",
         "> وثيقةٌ **مولَّدة**. أرقامُها كلُّها مقروءةٌ من `tawqi3_v0.json`، "
         "وتُعاد كتابتُها بـ`python tawqi3_gate.py --doc`. لا يُحرَّر رقمٌ "
         "منها بيد.", "",
         "## ① العلّة", "",
         "ختمُ `fetch_source.sh` على طريق `self` يشترط `SOURCES_SEAL_OWNER=1`. "
         "وهذا **دعوى المُشغِّل لا توقيعُ المالك**: متغيّرُ بيئةٍ يكتبه كلُّ من "
         "شغّل السكربت. فالختمُ يُثبت أنّ البايتاتِ هي هي، ولا يُثبت من أدخلها.",
         "", "والتوقيعُ الحقيقيُّ كان حاضرًا مهمَلًا: إيداعاتُ الرفع موقَّعةٌ "
         "معمّاةً في ترويسة `gpgsig`. فهذا البابُ يقرؤه ويتحقَّق منه بالحساب.",
         "", "## ② المفتاحُ — مودَعٌ مثبَّتٌ بوجهَين", "",
         "| البند | القيمة |", "|---|---|",
         f"| الملفّ | `keys/github-web-flow.asc` |",
         f"| بايتات | {k['بايتات']} |",
         f"| sha256 | `{k['sha256']}` |",
         f"| بصمةُ الموقِّع | `{k['بصمةُ الموقِّع']}` |",
         f"| هويّتُه | {k['هويّةُ الموقِّع']} |",
         f"| مفاتيحُ الحلقة | {k['مفاتيحُ الحلقة']} |", "",
         "مودَعٌ في الشجرة فلا شبكةَ في التحقُّق، ومثبَّتٌ بوجهَين فلا يُبدَّل "
         "صامتًا: تبدُّلُ بايتةٍ أو غيابُ البصمة صريخٌ **قبل** أن يُستعمَل.", "",
         "## ③ السلسلةُ — خمسُ حلقاتٍ لا حلقةٌ واحدة", "",
         "التوقيعُ لا يقع على الملفّ بل على كائن الإيداع. فلا يُقال «موقَّعٌ» "
         "حكمًا على مصدرٍ حتى تُقاس الخمسُ كلُّها، وانقطاعُ واحدةٍ يُسقِط الحكمَ "
         "ولا يُرقَّع بالباقي:", ""]
    for s in A["المصادر"]:
        L += [f"### `{s['مصدر']}` — {s['حكم']} "
              f"({s['حلقاتٌ موصولة']}/{s['حلقاتٌ مقيسة']})", "",
              f"الملفّ: `{s['ملفّ']}` · الإيداع: `{s['إيداع']}` · "
              f"المفتاح: `{s['مفتاحٌ موقِّع']}`", "",
              "| الحلقة | موصولة | القيمة |", "|---|---|---|"]
        for lk in s["حلقات"]:
            L.append(f"| {lk['حلقة']} | {'✓' if lk['موصولة'] else '✗'} "
                     f"| `{lk['قيمة']}` |")
        L.append("")
    L += ["## ④ الحكمُ أربعٌ لا اثنتان", "",
          f"- **موقَّعٌ موصول**: {M['موقَّعٌ موصول']}",
          f"- **موقَّعٌ مقطوع**: {M['موقَّعٌ مقطوع']} — يُسقِط البابَ بـ`5`",
          f"- **غيرُ موقَّع**: {M['غيرُ موقَّع']} — يُسقِط البابَ بـ`5`: "
          "طريقُ `self` بابُ المالك، فلا يدخل منه ما لا يحمل توقيعَه",
          f"- **إيداعٌ غائب**: {M['إيداعٌ غائب']} — بيانٌ معطوبٌ لا دَين، "
          "يُسقِط البابَ بـ`5`",
          "",
          f"وسطرُ العقد يقول `شهودٌ مختومون` = "
          f"{M['شهودٌ مختومون في سطر العقد']}؛ والموقَّعُ الموصولُ منها "
          f"{M['موقَّعٌ موصول']}. **والختمُ غيرُ التوقيع**: الأوّلُ يَحفظ "
          "البايتات، والثاني يَشهد للمُدخِل. فلا يُقرأ أحدُهما مكانَ الآخر.", "",
          "## ⑤ الديون — تُسمّى ولا تُسعَّر", "",
          f"**{M['ديونٌ مسمّاة']} ديونٍ، بلا رقمٍ واحدٍ فيها.**", ""]
    for d in A["الديون"]:
        L.append(f"- **{d['دَين']}** — {d['بيان']}. *الطريق*: {d['الطريق']}.")
    L += ["", "وأثقلُها الأوّل، ويُقال بحرفه: **من ملكَ الحسابَ ملكَ التوقيعَ**. "
          "فهذا البابُ يرفع الختمَ من «دعوى مُشغِّل» إلى «شهادةِ GitHub لحساب "
          "المالك»، ولا يبلغ به «مفتاحًا في يد المالك». والفرقُ معلَنٌ ولا يُطوى.",
          "", "## ⑥ محاولاتُ التكذيب", "",
          f"**{M['محاولاتُ_تكذيب']}** محاولةً تُشغَّل ولا تُقرَأ، ونجاحُ واحدةٍ "
          "يُسقِط البابَ:", ""]
    for x in A["محاولاتُ_التكذيب"]:
        L.append(f"- {x['محاولة']} — {'**نجحت ✗**' if x['نجحت'] else 'رُدَّت ✓'}")
    L += ["", "---", "",
          "`python tawqi3_gate.py --json tawqi3_v0.json --doc`  ·  "
          "الأختامُ في `induction/seals.py`، والمصادمةُ في "
          "`.github/workflows/ci.yml`.", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(argv=None):
    ap = argparse.ArgumentParser(description="بابُ التوقيع")
    ap.add_argument("--json", metavar="ملفّ", help="وديعةُ الباب إلى ملفّ")
    ap.add_argument("--doc", nargs="?", const=DOC, metavar="ملفّ",
                    help="الوثيقةُ المولَّدة (TAWQI3.md ما لم يُسمَّ غيرُها)")
    a = ap.parse_args(argv)
    try:
        R = run()
        if a.json:
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(R, fh, ensure_ascii=False, indent=2, sort_keys=True)
            print(f"JSON ⟵ {a.json}")
        if a.doc:
            write_doc(R, a.doc)
            print(f"الوثيقة ⟵ {a.doc}")
        show(R)
        if R["التوقيع_v0"]["سقوط"]:
            return E_CHAIN
    except TawqiError as exc:
        print(f"صريخ: {exc.message}", file=sys.stderr)
        return exc.code
    return 0


if __name__ == "__main__":
    sys.exit(main())
