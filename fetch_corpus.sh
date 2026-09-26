#!/usr/bin/env bash
# fetch_corpus.sh — جلب المجمَّد (نص Tanzil المشكول: quran-simple-enhanced.txt) إلى mujammad.txt.
# الملف لا يُودَع في المستودع؛ المودَع مِهرُه: البصمة + المصدر. البصمة تُقرأ من المحرّك نفسه،
# ويُتحقَّق منها قبل أيّ عدّ: من خالفها فليس المجمَّد — ولا يُقاس على بديلٍ صامت.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CORPUS_PATH:-$ROOT/mujammad.txt}"
ENGINE="$ROOT/algebra_engine.py"

SHA="$(sed -n 's/^MUJAMMAD_SHA256 = "\([0-9a-f]\{64\}\)".*/\1/p' "$ENGINE" | head -n 1)"
[ -n "$SHA" ] || { echo "صريخ: تعذّرت قراءة البصمة من $ENGINE" >&2; exit 3; }

digest() { sha256sum "$1" | cut -d' ' -f1; }

if [ -f "$DEST" ] && [ "$(digest "$DEST")" = "$SHA" ]; then
  echo "المجمَّد حاضرٌ مطابقُ البصمة: $DEST"
  exit 0
fi

# المرايا بالترتيب؛ CORPUS_URL يتقدّمها إن أُعلن (مرآةٌ محلّية أو داخليّة).
MIRRORS=(
  "https://tanzil.net/res/text/quran-simple-enhanced.txt"
  "http://www.globalquran.com/downloads/quran-simple-enhanced.txt"
)
[ -n "${CORPUS_URL:-}" ] && MIRRORS=("$CORPUS_URL" "${MIRRORS[@]}")

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

for url in "${MIRRORS[@]}"; do
  echo "جلبٌ من: $url"
  if curl -fsSL --max-time 120 -o "$TMP" "$url"; then
    got="$(digest "$TMP")"
    if [ "$got" = "$SHA" ]; then
      mv "$TMP" "$DEST"
      trap - EXIT
      echo "المجمَّد مُودَعٌ بالبصمة ✓: $DEST ($SHA)"
      exit 0
    fi
    echo "بصمةٌ مخالفة من $url: $got ≠ $SHA — يُرفض ولا يُقاس عليه" >&2
  else
    echo "تعذّر الجلب من $url" >&2
  fi
done

cat >&2 <<EOF
صريخ: لم يُجلَب المجمَّد المطابق للبصمة $SHA.
المصدر: نص Tanzil المشكول quran-simple-enhanced.txt (مرآة GlobalQuran) — 6,246 سطرًا، 1,306,770 بايتًا.
إن كانت الشبكة محجوبة، أعلن مرآةً بنفسك: CORPUS_URL=<رابط> bash fetch_corpus.sh
أو ضع الملف يدويًّا في $DEST — ثم تُفحَص بصمتُه في المحرّك قبل أيّ عدّ.
EOF
exit 1
