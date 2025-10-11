#!/bin/bash
set -euo pipefail

HTML_DIR="data/mirror_input"
TXT_DIR="data/mirror_input"

mkdir -p "$TXT_DIR"

for HTML in "$HTML_DIR"/*.html; do
  if [[ -f "$HTML" ]]; then
    BASE_NAME=$(basename "$HTML" .html)
    TXT="${TXT_DIR}/${BASE_NAME}.txt"
    echo "Extracting $HTML to $TXT..."

    if command -v pandoc >/dev/null; then
      pandoc -f html -t plain "$HTML" -o "$TXT" && [[ -s "$TXT" ]] && echo "✓ Pandoc success: $TXT"
    elif command -v htmlq >/dev/null; then
      htmlq -t body < "$HTML" > "$TXT" && [[ -s "$TXT" ]] && echo "✓ htmlq success: $TXT"
    else
      strings -n 5 "$HTML" > "$TXT" && [[ -s "$TXT" ]] && echo "✓ Strings fallback success: $TXT"
    fi
  else
    echo "No .html files found in $HTML_DIR"
  fi
done

echo "Extraction complete for all .html files."
