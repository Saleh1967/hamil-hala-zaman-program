#!/usr/bin/env bash
# fetch_source.sh — جلبُ نصوص المصادر بالبصمة، على نمط fetch_corpus.sh.
#
# الملفّاتُ لا تُودَع في المستودع؛ المودَعُ مِهرُها: بصمةُ كائن git + الطول + sha256،
# وكلُّها في sources_manifest.tsv — مصدرُ حقيقةٍ واحد. من خالف واحدًا منها فليس
# المصدرَ، ولا يُقاس على بديلٍ صامت.
#
# طريقان لا ثالثَ لهما، يُميَّزان بحقل repo في البيان:
#   owner/name  مستودعُ git (OpenITI) — استنساخٌ blobless وحلُّ المسار على الشجرة
#   local       ملفٌّ يضعه المالكُ في corpora/inbox/ بحرف اسمِه المكتوبِ في حقل path
# والبصماتُ الثلاثُ تُقاس في الطريقين من البايتات الحاضرة، لا تُنقَل عن تقرير.
#
# الأطوار:
#   --list                عرضُ البيان كما هو
#   --resolve <id|--all>  في الطريق البعيد: حلُّ النمط على الشجرة بلا تنزيل بايتة؛
#                         وفي المحلّيّ: عرضُ القياس الثلاثيّ للملف الحاضر
#   --fetch   <id|--all>  إحضارُ الملف والتحقّقُ الثلاثيّ (البعيدُ يُودَع corpora/sources/)
#   --check   <id|--all>  التحقّقُ من نسخةٍ حاضرةٍ دون شبكة
#   --seal    <id>        كتابةُ الختم المقيس في البيان — بيد المالك وحدَه
#
# المخارج: 0 نجاح · 1 تعذُّرُ جلب · 2 خطأُ استعمال · 3 بيانٌ معطوب · 4 مخالفةُ ختم.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SOURCES_MANIFEST:-$ROOT/sources_manifest.tsv}"
STORE="${SOURCES_DIR:-$ROOT/corpora/sources}"
INBOX="${SOURCES_INBOX:-$ROOT/corpora/inbox}"
HOST="${OPENITI_HOST:-https://github.com}"

E_FETCH=1; E_USAGE=2; E_MANIFEST=3; E_SEAL=4

die() { echo "صريخ: $1" >&2; exit "${2:-$E_USAGE}"; }
digest() { sha256sum "$1" | cut -d' ' -f1; }
size() { wc -c < "$1" | tr -d ' '; }

[ -f "$MANIFEST" ] || die "لا بيانَ مصادر في $MANIFEST" "$E_MANIFEST"

# ــ قراءةُ البيان ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# rows: أسطرُ البيان بلا تعليقٍ ولا فراغ. الحقولُ عشرةٌ بالجدولة، ومن خالف سقط.
rows() { grep -v '^[[:space:]]*#' "$MANIFEST" | grep -v '^[[:space:]]*$'; }

field() { # field <row> <n>
  printf '%s\n' "$1" | cut -f"$2"
}

row_of() { # row_of <id>
  local want="$1" line
  while IFS= read -r line; do
    [ "$(field "$line" 1)" = "$want" ] && { printf '%s\n' "$line"; return 0; }
  done < <(rows)
  return 1
}

ids() { rows | cut -f1; }

validate() {
  local line n bad=0 i=0
  while IFS= read -r line; do
    i=$((i + 1))
    n="$(printf '%s\n' "$line" | awk -F'\t' '{print NF}')"
    [ "$n" = "10" ] || { echo "سطرٌ $i: $n حقلًا لا 10" >&2; bad=1; }
    case "$(field "$line" 9)" in
      مرشَّح|محلول|مختوم|معذور) ;;
      *) echo "سطرٌ $i: حالٌ مجهولة «$(field "$line" 9)»" >&2; bad=1 ;;
    esac
  done < <(rows)
  [ "$(ids | sort | uniq -d | wc -l | tr -d " ")" = "0" ] || { echo "معرِّفٌ مكرَّر في البيان" >&2; bad=1; }
  [ "$bad" = "0" ] || exit "$E_MANIFEST"
}

# ــ الاستنساخ الأجوف ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
# blobless: الشجرةُ كاملةٌ والبايتاتُ عند الطلب. فحلُّ المسار وقراءةُ بصمة الكائن
# والطولِ تتمّ بلا تنزيل نصٍّ أصلًا.
clone_blobless() { # clone_blobless <repo> <ref> <dir>
  local repo="$1" ref="$2" dir="$3"
  [ -d "$dir/.git" ] && return 0
  GIT_TERMINAL_PROMPT=0 git clone --filter=blob:none --no-checkout --depth=1 \
    --branch "$ref" -q "$HOST/$repo.git" "$dir" 2>/dev/null && return 0
  echo "تعذّر استنساخُ $HOST/$repo.git على $ref" >&2
  return 1
}

resolve_one() { # resolve_one <dir> <pattern> → «path<TAB>blob<TAB>bytes» أو سقوط
  local dir="$1" pat="$2" hits n
  hits="$(git -C "$dir" ls-tree -r --name-only HEAD | grep -E "$pat" || true)"
  n="$(printf '%s' "$hits" | grep -c . || true)"
  if [ "$n" = "0" ]; then
    echo "النمطُ «$pat» لم يُطابق شيئًا في الشجرة — لا يُجلَب بديلٌ صامت" >&2
    return 1
  fi
  if [ "$n" != "1" ]; then
    echo "النمطُ «$pat» طابق $n مسارًا؛ اختر واحدًا بحرفه في حقل path:" >&2
    printf '%s\n' "$hits" | sed 's/^/  /' >&2
    return 1
  fi
  git -C "$dir" ls-tree -l HEAD -- "$hits" | awk -v p="$hits" '{print p "\t" $3 "\t" $4}'
}

# ــ الأطوار ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
do_list() {
  printf '%-18s %-16s %-8s %s\n' "المعرِّف" "المستودع" "الحال" "الملحوظة"
  local line
  while IFS= read -r line; do
    printf '%-18s %-16s %-8s %s\n' \
      "$(field "$line" 1)" "$(field "$line" 2)" "$(field "$line" 9)" "$(field "$line" 10)"
  done < <(rows)
}

# الطريقان بلا شبكة: المحلّيُّ (ملفٌّ بيد المالك) والمستودعُ نفسُه (كائنٌ في تاريخه).
offline_route() { # offline_route <row>
  case "$(field "$1" 2)" in local|self) return 0 ;; *) return 1 ;; esac
}

excused_guard() { # excused_guard <row>
  [ "$(field "$1" 9)" = "معذور" ] || return 0
  echo "«$(field "$1" 1)» معذورٌ بالاسم: $(field "$1" 10) — لا يُجلَب من OpenITI" >&2
  return 1
}

do_resolve() { # do_resolve <id>
  local row dir out
  row="$(row_of "$1")" || die "لا معرِّفَ «$1» في البيان"
  excused_guard "$row" || return 0

  if offline_route "$row"; then
    FETCHED=""; MEASURED=""
    fetch_one "$row" || return $?
    echo "$1 حاضرٌ ($(field "$row" 2)):"
    echo "  المسار: $(printf '%s' "$MEASURED" | cut -f1)"
    echo "  بصمةُ الكائن: $(printf '%s' "$MEASURED" | cut -f2)"
    echo "  الطول: $(printf '%s' "$MEASURED" | cut -f3) بايتًا"
    echo "  sha256: $(printf '%s' "$MEASURED" | cut -f4)"
    return 0
  fi

  dir="$WORK/$(field "$row" 1)"
  clone_blobless "$(field "$row" 2)" "$(field "$row" 3)" "$dir" || return "$E_FETCH"
  out="$(resolve_one "$dir" "$(field "$row" 4)")" || return "$E_FETCH"
  echo "$1 محلولٌ:"
  echo "  المسار: $(printf '%s' "$out" | cut -f1)"
  echo "  بصمةُ الكائن: $(printf '%s' "$out" | cut -f2)"
  echo "  الطول: $(printf '%s' "$out" | cut -f3) بايتًا"
  echo "  (البايتاتُ لم تُنزَّل بعد؛ sha256 يُقاس عند --fetch)"
}

# fetch_one يُخرج الملفَّ وحدَه ويُرجع مساره المؤقَّت في FETCHED، وقياساتِه في MEASURED.
fetch_one() { # fetch_one <row>
  local row="$1" dir path ref obj blob bytes out got_blob got_len

  if [ "$(field "$row" 2)" = "local" ]; then
    # الطريقُ المحلّيّ: لا استنساخَ ولا شبكة. الملفُّ يضعه المالكُ في INBOX بحرف
    # اسمِه المكتوبِ في حقل path، والبصماتُ الثلاثُ تُقاس من بايتاته حاضرةً.
    path="$(field "$row" 5)"
    [ "$path" = "-" ] && { echo "«$(field "$row" 1)» محلّيٌّ بلا اسمِ ملفٍّ في حقل path" >&2; return "$E_MANIFEST"; }
    FETCHED="$INBOX/$path"
    [ -f "$FETCHED" ] || {
      echo "لا ملفَّ محلّيًّا: $FETCHED" >&2
      echo "  ضعه بحرف اسمِه هناك (أو أعلن مجلّدًا: SOURCES_INBOX=<مسار>)" >&2
      return "$E_FETCH"
    }
  elif [ "$(field "$row" 2)" = "self" ]; then
    # طريقُ المستودع نفسِه: البايتاتُ في تاريخ هذا المستودع عند إيداعٍ مثبَّتٍ
    # بالاسم في حقل ref. تُقرأ بـcat-file بلا شبكةٍ ولا صندوقِ وارد، فتبقى
    # مستردَّةً لكلِّ من استنسخ المستودعَ ولو حُذف الملفُّ من الرأس بعدُ.
    path="$(field "$row" 5)"; ref="$(field "$row" 3)"
    if [ "$path" = "-" ] || [ "$ref" = "-" ]; then
      echo "«$(field "$row" 1)» من المستودع نفسِه بلا ref أو path" >&2
      return "$E_MANIFEST"
    fi
    git -C "$ROOT" rev-parse --verify -q "$ref^{commit}" >/dev/null \
      || { echo "لا إيداعَ «$ref» في هذا المستودع — جرّب: git fetch origin" >&2; return "$E_FETCH"; }
    obj="$(git -C "$ROOT" rev-parse --verify -q "$ref:$path" 2>/dev/null)" \
      || { echo "لا «$path» في شجرة $ref" >&2; return "$E_FETCH"; }
    FETCHED="$WORK/$(field "$row" 1).bytes"
    git -C "$ROOT" cat-file blob "$obj" > "$FETCHED" \
      || { echo "تعذّرت قراءةُ الكائن $obj" >&2; return "$E_FETCH"; }
  else
    dir="$WORK/$(field "$row" 1)"
    clone_blobless "$(field "$row" 2)" "$(field "$row" 3)" "$dir" || return "$E_FETCH"

    path="$(field "$row" 5)"
    if [ "$path" = "-" ]; then
      out="$(resolve_one "$dir" "$(field "$row" 4)")" || return "$E_FETCH"
      path="$(printf '%s' "$out" | cut -f1)"
    fi

    git -C "$dir" checkout -q HEAD -- "$path" 2>/dev/null \
      || { echo "تعذّر إخراجُ «$path» من $(field "$row" 2)" >&2; return "$E_FETCH"; }
    FETCHED="$dir/$path"
    [ -f "$FETCHED" ] || { echo "لا ملفَّ بعد الإخراج: $FETCHED" >&2; return "$E_FETCH"; }
  fi

  # التحقُّق الثلاثيّ: بصمةُ كائن git أوّلًا (هي شهادةُ المصدر)، ثمّ الطول، ثمّ sha256.
  got_blob="$(git hash-object "$FETCHED")"
  got_len="$(size "$FETCHED")"
  blob="$(field "$row" 6)"; bytes="$(field "$row" 7)"
  MEASURED="$path	$got_blob	$got_len	$(digest "$FETCHED")"

  if [ "$blob" != "-" ] && [ "$got_blob" != "$blob" ]; then
    echo "بصمةُ كائنٍ مخالفة لـ$(field "$row" 1): $got_blob ≠ $blob — يُرفض" >&2
    return "$E_SEAL"
  fi
  if [ "$bytes" != "-" ] && [ "$got_len" != "$bytes" ]; then
    echo "طولٌ مخالفٌ لـ$(field "$row" 1): $got_len ≠ $bytes — يُرفض" >&2
    return "$E_SEAL"
  fi
  return 0
}

do_fetch() { # do_fetch <id>
  local row sha got rc dest
  row="$(row_of "$1")" || die "لا معرِّفَ «$1» في البيان"
  excused_guard "$row" || return 0

  FETCHED=""; MEASURED=""
  fetch_one "$row" || { rc=$?; return "$rc"; }

  sha="$(field "$row" 8)"
  got="$(printf '%s' "$MEASURED" | cut -f4)"
  if [ "$sha" != "-" ] && [ "$got" != "$sha" ]; then
    echo "بصمةُ sha256 مخالفةٌ لـ$1: $got ≠ $sha — يُرفض ولا يُقاس عليه" >&2
    return "$E_SEAL"
  fi

  # المحلّيُّ يبقى حيث وضعه المالك؛ لا تُنسَخ بايتاتُه مرّةً ثانيةً في الشجرة.
  if offline_route "$row"; then
    dest="$(printf '%s' "$MEASURED" | cut -f1)"
  else
    dest="$STORE/$1.txt"
    mkdir -p "$STORE"
    cp "$FETCHED" "$dest"
  fi

  if [ "$sha" = "-" ]; then
    echo "$1 حاضرٌ غيرَ مختوم → $dest"
    echo "  القياسُ الطازج: بصمةُ الكائن $(printf '%s' "$MEASURED" | cut -f2) · $(printf '%s' "$MEASURED" | cut -f3) بايتًا · sha256 $got"
    echo "  الختمُ بيد المالك: SOURCES_SEAL_OWNER=1 bash fetch_source.sh --seal $1"
  else
    echo "$1 مطابقُ الختم ✓ → $dest ($sha)"
  fi
}

do_check() { # do_check <id> — بلا شبكة
  local row f sha bytes blob bad=0
  row="$(row_of "$1")" || die "لا معرِّفَ «$1» في البيان"
  excused_guard "$row" || return 0
  [ "$(field "$row" 9)" = "مختوم" ] || { echo "$1: غيرُ مختومٍ بعد — لا شيءَ يُصادَم"; return 0; }
  if offline_route "$row"; then
    # لا نسخةَ تُفتَّش: البايتاتُ تُقرأ من موضعها الأصليِّ ويُصادَم الختمُ عليها.
    FETCHED=""; MEASURED=""
    fetch_one "$row" || return $?
    [ "$(printf '%s' "$MEASURED" | cut -f4)" = "$(field "$row" 8)" ] \
      || { echo "$1: sha256 مخالفة" >&2; return "$E_SEAL"; }
    echo "$1 مطابقٌ ثلاثيًّا ✓"
    return 0
  fi
  f="$STORE/$1.txt"
  [ -f "$f" ] || { echo "$1: لا نسخةَ حاضرةً في $f" >&2; return "$E_FETCH"; }
  blob="$(field "$row" 6)"; bytes="$(field "$row" 7)"; sha="$(field "$row" 8)"
  [ "$(git hash-object "$f")" = "$blob" ] || { echo "$1: بصمةُ كائنٍ مخالفة" >&2; bad=1; }
  [ "$(size "$f")" = "$bytes" ] || { echo "$1: طولٌ مخالف" >&2; bad=1; }
  [ "$(digest "$f")" = "$sha" ] || { echo "$1: sha256 مخالفة" >&2; bad=1; }
  [ "$bad" = "0" ] || return "$E_SEAL"
  echo "$1 مطابقٌ ثلاثيًّا ✓"
}

do_seal() { # do_seal <id> — بيد المالك وحدَه
  local row id path blob bytes sha tmp
  [ "${SOURCES_SEAL_OWNER:-}" = "1" ] \
    || die "الختمُ بيد المالك وحدَه: SOURCES_SEAL_OWNER=1 bash fetch_source.sh --seal $1"
  row="$(row_of "$1")" || die "لا معرِّفَ «$1» في البيان"
  excused_guard "$row" || return 0
  [ "$(field "$row" 9)" = "مختوم" ] && die "«$1» مختومٌ سلفًا — لا يُعاد ختمُه إلا بحذف ختمه بيدٍ معلَنة" "$E_SEAL"

  FETCHED=""; MEASURED=""
  fetch_one "$row" || return $?
  id="$1"
  path="$(printf '%s' "$MEASURED" | cut -f1)"
  blob="$(printf '%s' "$MEASURED" | cut -f2)"
  bytes="$(printf '%s' "$MEASURED" | cut -f3)"
  sha="$(printf '%s' "$MEASURED" | cut -f4)"

  tmp="$(mktemp)"
  awk -F'\t' -v OFS='\t' -v id="$id" -v p="$path" -v b="$blob" -v n="$bytes" -v s="$sha" '
    /^[[:space:]]*#/ || NF < 10 { print; next }
    $1 == id { $5 = p; $6 = b; $7 = n; $8 = s; $9 = "مختوم" }
    { print }
  ' "$MANIFEST" > "$tmp"
  mv "$tmp" "$MANIFEST"
  echo "$id مختومٌ في البيان ✓"
  echo "  $path · $blob · $bytes بايتًا · $sha"
}

usage() {
  awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "${BASH_SOURCE[0]}"
  exit "$E_USAGE"
}

# ــ المدخل ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ
main() {
  [ $# -ge 1 ] || usage
  validate

  local mode="$1"; shift
  case "$mode" in
    --list) do_list; return 0 ;;
    --resolve|--fetch|--check|--seal) ;;
    -h|--help) usage ;;
    *) die "طورٌ مجهول: $mode" ;;
  esac

  local targets=()
  if [ "${1:---all}" = "--all" ]; then
    [ "$mode" = "--seal" ] && die "الختمُ مصدرًا مصدرًا لا جملةً: --seal <id>"
    mapfile -t targets < <(ids)
  else
    targets=("$1")
  fi

  WORK="$(mktemp -d)"
  trap 'rm -rf "$WORK"' EXIT

  local id rc=0 one
  for id in "${targets[@]}"; do
    one=0
    case "$mode" in
      --resolve) do_resolve "$id" || one=$? ;;
      --fetch)   do_fetch   "$id" || one=$? ;;
      --check)   do_check   "$id" || one=$? ;;
      --seal)    do_seal    "$id" || one=$? ;;
    esac
    if [ "$one" -gt "$rc" ]; then rc="$one"; fi
  done
  return "$rc"
}

main "$@"
