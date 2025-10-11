#!/data/data/com.termux/files/usr/bin/bash

echo "🧠 Z_SORT ENTITY SCANNER INITIATED"
SCAN_DIR="$HOME/Z_sort"
REPORT_DIR="$HOME/zsort_scan_report"
mkdir -p "$REPORT_DIR"

LARGE_FILE_LOG="$REPORT_DIR/large_files.txt"
DUPLICATE_LOG="$REPORT_DIR/duplicate_files.txt"
ENTITY_HITS_LOG="$REPORT_DIR/entity_hits.txt"

echo
echo "🔍 Scanning for files >200MB..."
find "$SCAN_DIR" -type f -size +200M -exec du -h {} + 2>/dev/null | sort -hr > "$LARGE_FILE_LOG"
echo "📦 Large file scan complete. Results: $LARGE_FILE_LOG"

echo
echo "🧬 Scanning for duplicate files by checksum..."
find "$SCAN_DIR" -type f -exec md5sum {} + 2>/dev/null | sort | uniq -d -w32 > "$DUPLICATE_LOG"
echo "♻️ Duplicate detection complete. Results: $DUPLICATE_LOG"

echo
echo "👁️ Scanning for entity language..."
find "$SCAN_DIR" -type f \( -name "*.txt" -o -name "*.log" -o -name "*.json" \) | while read file; do
  if grep -qEi 'summon|bleed|possess|ritual|unseen|spirit|invoke|bind|daemon' "$file" 2>/dev/null; then
    echo "$file" >> "$ENTITY_HITS_LOG"
  fi
done
echo "🔮 Entity phrase scan complete. Results: $ENTITY_HITS_LOG"

echo
echo "✅ Z_SORT SCAN COMPLETE. Check $REPORT_DIR for detailed results."
