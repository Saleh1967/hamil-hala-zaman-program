#!/usr/bin/env bash
# test_fetch_source.sh — مصادمةُ عقد fetch_source.sh: مخارجُه الخمسةُ وطرقُه
# الثلاثةُ، بلا شبكة.
#
# العقدُ المصادَمُ مكتوبٌ في ترويسة fetch_source.sh:
#   0 نجاح · 1 تعذُّرُ جلب · 2 خطأُ استعمال · 3 بيانٌ معطوب · 4 مخالفةُ ختم.
# ودعوى «يخرج بكذا» لا تُصدَّق بقراءة الشيفرة، بل تُشغَّل ويُقاس مخرجُها.
#
# لا شبكةَ أصلًا: البياناتُ مصنوعةٌ في مجلّدٍ مؤقَّت، والطريقان المجرَّبان
# المحلّيُّ (corpora/inbox) والمستودعُ نفسُه (git cat-file على إيداع HEAD)؛
# والطريقُ البعيدُ يُجرَّب بمضيفٍ معدومٍ (OPENITI_HOST=file:///…) فيسقط بـ1
# كما يسقط بحجب OpenITI سواءً بسواء.
#
# البيئة: SOURCES_MANIFEST · SOURCES_DIR · SOURCES_INBOX — كلُّها إلى المؤقَّت،
# فلا يُمَسُّ sources_manifest.tsv ولا corpora/ في الشجرة.
#
# التشغيل:  bash test_fetch_source.sh
# المخرج:   0 إن طابق كلُّ مخرجٍ عقدَه · 1 إن خالف واحد.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$ROOT/fetch_source.sh"
[ -f "$SCRIPT" ] || { echo "صريخ: لا fetch_source.sh في $ROOT" >&2; exit 2; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
INBOX="$TMP/inbox"; OUT="$TMP/out"
mkdir -p "$INBOX" "$OUT"

PASS=0; FAIL=0

tab() { printf '%s\n' "$*" | tr '|' '\t'; }

# ــ المصادمة ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# expect <المخرج المنتظر> <العنوان> <أمرٌ…> — يُشغَّل ويُقاس مخرجُه لا يُدَّعى.
expect() {
  local want="$1" label="$2"; shift 2
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" = "$want" ]; then
    PASS=$((PASS + 1)); printf '  ✓ %s (خرج %s)\n' "$label" "$rc"
  else
    FAIL=$((FAIL + 1))
    printf '  ✗ %s: خرج %s والمنتظر %s\n' "$label" "$rc" "$want" >&2
    printf '%s\n' "$out" | sed 's/^/      /' >&2
  fi
}

# fetch_source.sh يُستدعى بالبيئة وحدَها؛ لا حالَ مشتركةً بين مصادمةٍ وأخرى.
fs() { # fs <manifest> <args…>
  local m="$1"; shift
  env SOURCES_MANIFEST="$m" SOURCES_DIR="$OUT" SOURCES_INBOX="$INBOX" \
      bash "$SCRIPT" "$@"
}

# ــ البايتاتُ المقيسة ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# شاهدٌ محلّيٌّ مصنوعٌ هنا، وبصماتُه الثلاثُ تُقاس من بايتاته لا تُنسَخ عن تقرير.
printf 'شاهدٌ محلّيٌّ للمصادمة\n' > "$INBOX/witness.txt"
W_BLOB="$(git hash-object "$INBOX/witness.txt")"
W_LEN="$(wc -c < "$INBOX/witness.txt" | tr -d ' ')"
W_SHA="$(sha256sum "$INBOX/witness.txt" | cut -d' ' -f1)"

# شاهدٌ من تاريخ هذا المستودع: إيداعُ HEAD بأربعين محرفًا وملفٌّ في شجرته.
SELF_REF="$(git -C "$ROOT" rev-parse HEAD)"
SELF_PATH="fetch_source.sh"
SELF_BLOB="$(git -C "$ROOT" rev-parse "$SELF_REF:$SELF_PATH")"
SELF_BYTES="$(git -C "$ROOT" cat-file blob "$SELF_BLOB" | wc -c | tr -d ' ')"
SELF_SHA="$(git -C "$ROOT" cat-file blob "$SELF_BLOB" | sha256sum | cut -d' ' -f1)"

# ــ البيانات ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
GOOD="$TMP/good.tsv"
{
  echo "# بيانٌ للمصادمة — عشرةُ حقولٍ بالجدولة"
  tab "witness|local|-|-|witness.txt|$W_BLOB|$W_LEN|$W_SHA|مختوم|شاهدٌ_محلّيٌّ_مختوم"
  tab "unsealed|local|-|-|witness.txt|-|-|-|مرشَّح|شاهدٌ_محلّيٌّ_بلا_ختم"
  tab "selfwitness|self|$SELF_REF|-|$SELF_PATH|$SELF_BLOB|$SELF_BYTES|$SELF_SHA|مختوم|كائنٌ_في_تاريخ_المستودع"
  tab "absent|local|-|-|nothing-here.txt|-|-|-|مرشَّح|لا_ملفَّ_في_الصندوق"
  tab "excused|-|-|-|-|-|-|-|معذور|لا_يُجلَب_من_OpenITI"
} > "$GOOD"

BAD_SEAL="$TMP/bad_seal.tsv"
{
  # ختمٌ مخالفٌ: البايتاتُ حاضرةٌ والرقمُ المكتوبُ ليس رقمَها.
  tab "witness|local|-|-|witness.txt|$W_BLOB|$W_LEN|$(printf '%064d' 0)|مختوم|ختمٌ_مخالف"
  tab "selfwitness|self|$SELF_REF|-|$SELF_PATH|$(printf '%040d' 0)|$SELF_BYTES|$SELF_SHA|مختوم|بصمةُ_كائنٍ_مخالفة"
  tab "shortlen|local|-|-|witness.txt|$W_BLOB|999999|$W_SHA|مختوم|طولٌ_مخالف"
} > "$BAD_SEAL"

FEW_FIELDS="$TMP/few.tsv";  tab "x|local|-|-|witness.txt|-|-|-|مرشَّح"        > "$FEW_FIELDS"
BAD_STATE="$TMP/state.tsv"; tab "x|local|-|-|witness.txt|-|-|-|حالٌ_مجهولة|ملحوظة" > "$BAD_STATE"
DUP_ID="$TMP/dup.tsv"
{
  tab "x|local|-|-|witness.txt|-|-|-|مرشَّح|أوّل"
  tab "x|local|-|-|witness.txt|-|-|-|مرشَّح|ثانٍ"
} > "$DUP_ID"
NO_PATH="$TMP/nopath.tsv"; tab "x|local|-|-|-|-|-|-|مرشَّح|محلّيٌّ_بلا_اسمِ_ملف" > "$NO_PATH"
REMOTE="$TMP/remote.tsv"
tab "far|OpenITI/0325AH|master|nothing-matches-this\$|-|-|-|-|مرشَّح|مضيفٌ_معدوم" > "$REMOTE"

# ــ 0: النجاح ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
echo "‹0› النجاح — الطريقان بلا شبكة:"
expect 0 "--list يعرض البيان"                 fs "$GOOD" --list
expect 0 "--check على ختمٍ مطابقٍ (محلّيّ)"     fs "$GOOD" --check witness
expect 0 "--fetch على ختمٍ مطابقٍ (محلّيّ)"     fs "$GOOD" --fetch witness
expect 0 "--resolve على المحلّيِّ الحاضر"        fs "$GOOD" --resolve witness
expect 0 "--check على كائنِ المستودع نفسِه"     fs "$GOOD" --check selfwitness
expect 0 "--fetch على كائنِ المستودع نفسِه"     fs "$GOOD" --fetch selfwitness
expect 0 "--check على غير المختوم لا يُصادَم"   fs "$GOOD" --check unsealed
expect 0 "المعذورُ لا يُجلَب ولا يُسقِط"          fs "$GOOD" --fetch excused

# الختمُ بيد المالك: يُقاس من البايتات ويُكتب في البيان، ثمّ يُصادَم فيَثبُت.
SEALABLE="$TMP/sealable.tsv"
tab "unsealed|local|-|-|witness.txt|-|-|-|مرشَّح|بلا_ختم" > "$SEALABLE"
expect 0 "--seal بيد المالك يكتب الختم" \
  env SOURCES_SEAL_OWNER=1 SOURCES_MANIFEST="$SEALABLE" SOURCES_DIR="$OUT" \
      SOURCES_INBOX="$INBOX" bash "$SCRIPT" --seal unsealed
expect 0 "المختومُ حديثًا يُصادَم فيطابق"        fs "$SEALABLE" --check unsealed
if grep -q "$W_SHA" "$SEALABLE"; then
  PASS=$((PASS + 1)); echo "  ✓ الختمُ المكتوبُ هو المقيسُ من البايتات"
else
  FAIL=$((FAIL + 1)); echo "  ✗ الختمُ المكتوبُ ليس sha256 المقيسة" >&2
fi

# ــ 1: تعذُّرُ الجلب ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
echo "‹1› تعذُّرُ الجلب:"
expect 1 "لا ملفَّ في صندوق الوارد"             fs "$GOOD" --fetch absent
SEALED_FAR="$TMP/sealed_far.tsv"
tab "far|OpenITI/0325AH|master|x\$|data/x|$(printf '%040d' 0)|1|$(printf '%064d' 0)|مختوم|لا_نسخة" \
  > "$SEALED_FAR"
expect 1 "لا نسخةَ حاضرةً لمختومٍ بعيد" \
  env SOURCES_MANIFEST="$SEALED_FAR" SOURCES_DIR="$TMP/empty" \
      SOURCES_INBOX="$INBOX" bash "$SCRIPT" --check far
expect 1 "المضيفُ المعدومُ يسقط كما يسقط الحجب" \
  env SOURCES_MANIFEST="$REMOTE" SOURCES_DIR="$OUT" SOURCES_INBOX="$INBOX" \
      OPENITI_HOST="file://$TMP/no-such-host" bash "$SCRIPT" --fetch far
SELF_GONE="$TMP/selfgone.tsv"
tab "ghost|self|$(printf '%040d' 0)|-|$SELF_PATH|-|-|-|مرشَّح|إيداعٌ_معدوم" > "$SELF_GONE"
expect 1 "إيداعٌ معدومٌ في المستودع نفسِه"       fs "$SELF_GONE" --fetch ghost

# ــ 2: خطأُ الاستعمال ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
echo "‹2› خطأُ الاستعمال:"
expect 2 "بلا طورٍ أصلًا"                       fs "$GOOD"
expect 2 "--help يعرض الترويسة"                 fs "$GOOD" --help
expect 2 "طورٌ مجهول"                           fs "$GOOD" --نزِّل
expect 2 "معرِّفٌ ليس في البيان"                 fs "$GOOD" --fetch لا-وجودَ-له
expect 2 "الختمُ بلا يدٍ معلَنة"                 fs "$GOOD" --seal unsealed
expect 2 "--seal --all مرفوضٌ: مصدرًا مصدرًا"    fs "$GOOD" --seal --all

# ــ 3: بيانٌ معطوب ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
echo "‹3› البيانُ المعطوب:"
expect 3 "لا بيانَ في المسار المعلَن"            fs "$TMP/no-such-manifest.tsv" --list
expect 3 "تسعةُ حقولٍ لا عشرة"                  fs "$FEW_FIELDS" --list
expect 3 "حالٌ مجهولةٌ في الحقل التاسع"          fs "$BAD_STATE" --list
expect 3 "معرِّفٌ مكرَّر"                        fs "$DUP_ID" --list
expect 3 "محلّيٌّ بلا اسمِ ملفٍّ في حقل path"     fs "$NO_PATH" --fetch x

# ــ 4: مخالفةُ الختم ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
echo "‹4› مخالفةُ الختم:"
expect 4 "sha256 مخالفةٌ على بايتاتٍ حاضرة"      fs "$BAD_SEAL" --fetch witness
expect 4 "sha256 مخالفةٌ تُصادَم في --check"     fs "$BAD_SEAL" --check witness
expect 4 "بصمةُ كائنٍ مخالفةٌ (المستودعُ نفسُه)"  fs "$BAD_SEAL" --fetch selfwitness
expect 4 "طولٌ مخالف"                           fs "$BAD_SEAL" --fetch shortlen
expect 4 "لا يُعاد ختمُ مختوم" \
  env SOURCES_SEAL_OWNER=1 SOURCES_MANIFEST="$GOOD" SOURCES_DIR="$OUT" \
      SOURCES_INBOX="$INBOX" bash "$SCRIPT" --seal witness

# ــ 5: عقدُ الطرق الثلاثة ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# ترويسةُ fetch_source.sh تعلن ثلاثةَ طرقٍ لا رابعَ لها. وقد كانت تعلن «طريقان لا
# ثالثَ لهما» وفي جسدها ثلاثةٌ، وعليها ثلاثةُ مصادرَ مختومةٍ بطريق self — فشاخ
# العقدُ صادقًا في ظاهره كاذبًا في عدَّته. ولا يُرأَب ذلك بكتابةِ الصواب مرّةً، بل
# بمصادمةِ الترويسة بجهتين: فروعِ fetch_one وحقلِ repo في البيان الحقيقيّ.
echo "‹5› عقدُ الطرق الثلاثة:"

# المعلَنُ: أسماءُ الطرق من كتلة الترويسة وحدَها — تُنتزَع من البايتات لا تُنسَخ هنا.
DECLARED="$(awk '/ثلاثةُ طرقٍ لا رابعَ لها/{f=1; next}
                 f && /^#   [^ ]/{print $2; next}
                 f && /^#    +[^ ]/{next}
                 f{exit}' "$SCRIPT" \
            | sed 's|^owner/name$|remote|' | sort -u)"

# المصنوعُ في الجسد: فروعُ fetch_one تقارن حقلَ repo بسلسلتين، وما عداهما else.
BODY="$(sed -n '/^fetch_one() {/,/^}/p' "$SCRIPT" \
        | sed -n 's/.*field "\$row" 2)" = "\([a-z]*\)".*/\1/p' | sort -u)"
BODY="$(printf '%s\nremote\n' "$BODY" | grep -v '^$' | sort -u)"

# المستعمَلُ في البيان الحقيقيّ: قيمةُ repo لغير المعذورين — والمعذورُ لا طريقَ له
# أصلًا (حقلُه «-»)، فهو غيابٌ مسمًّى لا طريقٌ رابعٌ مطويّ.
USED="$(grep -v '^[[:space:]]*#' "$ROOT/sources_manifest.tsv" | grep -v '^[[:space:]]*$' \
        | awk -F'\t' '$9 != "معذور" {print $2}' | sed 's|.*/.*|remote|' | sort -u)"

if [ "$DECLARED" = "$BODY" ]; then
  PASS=$((PASS + 1)); echo "  ✓ الترويسةُ تطابق فروعَ fetch_one ($(printf '%s' "$DECLARED" | paste -sd' ' -))"
else
  FAIL=$((FAIL + 1))
  echo "  ✗ الترويسةُ خالفت الجسد: معلَنٌ [$(printf '%s' "$DECLARED" | paste -sd' ' -)] ⟷ مصنوعٌ [$(printf '%s' "$BODY" | paste -sd' ' -)]" >&2
fi

# البيانُ لا يلزمه أن يستعمل كلَّ طريق، لكن لا يستعمل طريقًا غيرَ معلَن.
UNDECLARED="$(comm -23 <(printf '%s\n' "$USED") <(printf '%s\n' "$DECLARED"))"
if [ -z "$UNDECLARED" ]; then
  PASS=$((PASS + 1)); echo "  ✓ لا طريقَ في البيان خارجَ العقد المعلَن"
else
  FAIL=$((FAIL + 1))
  echo "  ✗ البيانُ يستعمل طريقًا غيرَ معلَنٍ في الترويسة: $(printf '%s' "$UNDECLARED" | paste -sd' ' -)" >&2
fi

# والعدَّةُ تُقاس لا تُكتَب: «ثلاثةُ طرقٍ لا رابعَ لها» يسقط إن صارت أربعًا بلا إعلان.
N_ROUTES="$(printf '%s\n' "$DECLARED" | grep -c .)"
if [ "$N_ROUTES" = "3" ]; then
  PASS=$((PASS + 1)); echo "  ✓ الطرقُ المعلَنةُ ثلاثٌ معدودةً من الترويسة"
else
  FAIL=$((FAIL + 1)); echo "  ✗ الترويسةُ تقول ثلاثةً والمعدودُ $N_ROUTES" >&2
fi

# ــ صيانةُ الحريم ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# المخالفُ لا تُودَع بايتاتُه في مجلّد المخرجات، والمحلّيُّ لا يُنسَخ مرّةً ثانية.
if [ ! -e "$OUT/witness.txt" ] && [ ! -e "$OUT/witness.txt.txt" ]; then
  PASS=$((PASS + 1)); echo "  ✓ المحلّيُّ لم يُنسَخ إلى $OUT"
else
  FAIL=$((FAIL + 1)); echo "  ✗ المحلّيُّ نُسخ إلى $OUT" >&2
fi
if git -C "$ROOT" diff --quiet -- sources_manifest.tsv; then
  PASS=$((PASS + 1)); echo "  ✓ sources_manifest.tsv لم يُمَسّ"
else
  FAIL=$((FAIL + 1)); echo "  ✗ sources_manifest.tsv تغيّر بالاختبار" >&2
fi

echo
echo "المطابقُ $PASS · المخالفُ $FAIL"
[ "$FAIL" = "0" ] || { echo "صريخ: عقدُ الجلب مخروقٌ — لا يُدمَج" >&2; exit 1; }
echo "عقدُ المخارج الخمسة وعقدُ الطرق الثلاثة محروسان ✓"
