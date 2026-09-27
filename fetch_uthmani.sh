#!/usr/bin/env bash
# fetch_uthmani.sh — جلب النسخة العثمانية (quran-uthmani.txt) إلى uthmani.txt.
# البايتات مودَعةٌ في الشجرة كالمجمَّد؛ وهذا المسارُ الاحتياطيُّ لمن استنسخ ناقصًا.
# البصمةُ تُقرأ من المحرّك نفسه — مصدرُ حقيقةٍ واحد — ويُتحقَّق منها قبل أيّ عدّ.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${UTHMANI_PATH:-$ROOT/uthmani.txt}"
ENGINE="$ROOT/waqf_layer.py"

SHA="$(sed -n 's/^UTHMANI_SHA256 = "\([0-9a-f]\{64\}\)".*/\1/p' "$ENGINE" | head -n 1)"
[ -n "$SHA" ] || { echo "صريخ: تعذّرت قراءة البصمة من $ENGINE" >&2; exit 3; }

digest() { sha256sum "$1" | cut -d' ' -f1; }

if [ -f "$DEST" ] && [ "$(digest "$DEST")" = "$SHA" ]; then
  echo "العثماني حاضرٌ مطابقُ البصمة: $DEST"
  exit 0
fi

MIRRORS=(
  "https://raw.githubusercontent.com/globalquran/data/master/Quran/quran-uthmani.txt"
  "https://tanzil.net/res/text/quran-uthmani.txt"
)
[ -n "${UTHMANI_URL:-}" ] && MIRRORS=("$UTHMANI_URL" "${MIRRORS[@]}")

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

for url in "${MIRRORS[@]}"; do
  echo "جلبٌ من: $url"
  if curl -fsSL --max-time 120 -o "$TMP" "$url"; then
    got="$(digest "$TMP")"
    if [ "$got" = "$SHA" ]; then
      mv "$TMP" "$DEST"
      trap - EXIT
      echo "العثماني مُودَعٌ بالبصمة ✓: $DEST ($SHA)"
      exit 0
    fi
    echo "بصمةٌ مخالفة من $url: $got ≠ $SHA — يُرفض ولا يُقاس عليه" >&2
  else
    echo "تعذّر الجلب من $url" >&2
  fi
done

cat >&2 <<EOF
صريخ: لم تُجلَب النسخة العثمانية المطابقة للبصمة $SHA.
المصدر: globalquran/data@Quran/quran-uthmani.txt (أصلُه Tanzil) — 6,236 سطرًا، 1,352,197 بايتًا.
إن كانت الشبكة محجوبة، أعلن مرآةً بنفسك: UTHMANI_URL=<رابط> bash fetch_uthmani.sh
EOF
exit 1
