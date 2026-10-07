#!/usr/bin/env bash
# fetch_maqayis.sh — جلب جدول جذور «مقاييس اللغة» إلى maqayis_by_root_csv_999.csv.
# الملف لا يُودَع في المستودع؛ المودَع مِهرُه: البصمة + الطول + المصدر. البصمة والطول
# يُقرآن من المحرّك نفسه (maqayis_layer.py) — مصدرُ حقيقةٍ واحد، لا نسخةٌ ثانيةٌ تتخلّف.
# من خالفهما فليس الجدول — ولا إثراءَ على بديلٍ صامت.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${MAQAYIS_PATH:-$ROOT/maqayis_by_root_csv_999.csv}"
ENGINE="$ROOT/maqayis_layer.py"

SHA="$(sed -n 's/^SEAL = "\([0-9a-f]\{64\}\)".*/\1/p' "$ENGINE" | head -n 1)"
LEN="$(sed -n 's/^SEAL_BYTES = \([0-9]\{1,\}\).*/\1/p' "$ENGINE" | head -n 1)"
[ -n "$SHA" ] && [ -n "$LEN" ] || { echo "صريخ: تعذّرت قراءة البصمة/الطول من $ENGINE" >&2; exit 3; }

digest() { sha256sum "$1" | cut -d' ' -f1; }
size() { wc -c < "$1" | tr -d ' '; }

if [ -f "$DEST" ] && [ "$(digest "$DEST")" = "$SHA" ]; then
  echo "جدول المقاييس حاضرٌ مطابقُ البصمة: $DEST"
  exit 0
fi

# المرايا بالترتيب؛ MAQAYIS_URL يتقدّمها إن أُعلن (مرآةٌ محلّية أو داخليّة).
MIRRORS=(
  "https://raw.githubusercontent.com/Saleh1967/Alghanem/main/maqayis_by_root_csv_999.csv"
  "https://raw.githubusercontent.com/Saleh1967/Alghanem/master/maqayis_by_root_csv_999.csv"
)
[ -n "${MAQAYIS_URL:-}" ] && MIRRORS=("$MAQAYIS_URL" "${MIRRORS[@]}")

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

for url in "${MIRRORS[@]}"; do
  echo "جلبٌ من: $url"
  if curl -fsSL --max-time 180 --retry 3 --retry-delay 5 -o "$TMP" "$url"; then
    got_len="$(size "$TMP")"
    if [ "$got_len" != "$LEN" ]; then
      echo "طولٌ مخالف من $url: $got_len ≠ $LEN — يُرفض" >&2
      continue
    fi
    got="$(digest "$TMP")"
    if [ "$got" = "$SHA" ]; then
      mv "$TMP" "$DEST"
      trap - EXIT
      echo "جدول المقاييس مُودَعٌ بالبصمة ✓: $DEST ($SHA)"
      exit 0
    fi
    echo "بصمةٌ مخالفة من $url: $got ≠ $SHA — يُرفض ولا يُقاس عليه" >&2
  else
    echo "تعذّر الجلب من $url" >&2
  fi
done

cat >&2 <<EOF
صريخ: لم يُجلَب جدول المقاييس المطابق للبصمة $SHA.
المصدر: Saleh1967/Alghanem@main:maqayis_by_root_csv_999.csv — $LEN بايتًا (انظر MAQAYIS.md).
إن كانت الشبكة محجوبة، أعلن مرآةً بنفسك: MAQAYIS_URL=<رابط> bash fetch_maqayis.sh
أو ضع الملف يدويًّا في $DEST — ثم تُفحَص بصمتُه في المحرّك قبل أيّ عدّ.
EOF
exit 1
