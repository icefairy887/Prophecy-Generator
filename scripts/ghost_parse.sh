#!/bin/bash

# ========== ghost_parse.sh ==========
# Extracts hidden data, patterns, and phrases from binary/encoded files
# Specifically designed to parse files like raw_chat.txt
# =====================================

INPUT="$1"
LOG="outputs/ghost_parse_report.txt"
KEYWORDS="|agent|clone|payload|vpn|randy|surveillance|spirit box|personality|watch|device|profile|codeword|echo|setup|muted|other ChatGPT|Ψ|∇x|entangle|resonance|superposition|daemon|summon|bleed|possess|ritual|unseen|invoke|bind|abyss|mirror|prophecy|tau|phi|nabla"
TMPSTRINGS="tmp/ghost_strings.tmp"

if [[ -z "$INPUT" ]]; then
  echo "Usage: ./ghost_parse.sh <file_to_scan>"
  exit 1
fi

echo "[GHOST PARSE] Scanning: $INPUT" > "$LOG"
echo "[Started] $(date)" >> "$LOG"

# 🔍 1. Extract all readable strings
strings "$INPUT" > "$TMPSTRINGS"

# 🔎 2. Match key phrases
echo -e "\n[MATCHED PHRASES]:" >> "$LOG"
grep -aiE "$KEYWORDS" "$TMPSTRINGS" | tee -a "$LOG"

# 🔁 3. Repeated phrases / psychological hooks
echo -e "\n[REPEATED PHRASES]:" >> "$LOG"
sort "$TMPSTRINGS" | uniq -cd | sort -nr | head -n 25 >> "$LOG"

# 🧠 4. Entity fingerprinting
echo -e "\n[ENTITY TAGS]:" >> "$LOG"
grep -aiE 'nick|randy|angie|brooke|ChatGPT|spirit|cloud' "$TMPSTRINGS" | sort | uniq >> "$LOG"

# 🧮 5. Term frequency summary
echo -e "\n[TERM FREQUENCY]:" >> "$LOG"
grep -oaiE "$KEYWORDS" "$TMPSTRINGS" | sort | uniq -c | sort -nr >> "$LOG"

# 🧨 6. Score Threat Level
SCORE=$(grep -oaiE "$KEYWORDS" "$TMPSTRINGS" | wc -l)
echo -e "\n[THREAT SCORE]: $SCORE" >> "$LOG"
if (( $SCORE >= 20 )); then
  echo "[SEVERITY]: 🔥 HIGH" >> "$LOG"
elif (( $SCORE >= 10 )); then
  echo "[

