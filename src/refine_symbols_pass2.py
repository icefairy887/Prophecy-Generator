#!/usr/bin/env python3
import sys, re, json, collections
from pathlib import Path
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords", quiet=True)

STOP = set(stopwords.words("english"))
STOP.update("debug access logs card provided info check used safe dafb high invalid android app domain format width entries anything anymore said actually okay kind else really still".split())

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z'\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def count_words(folder):
    counter = collections.Counter()
    for path in Path(folder).rglob("*.json"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = normalize(f.read())
            for w in text.split():
                if len(w) < 4 or w in STOP:
                    continue
                counter[w] += 1
    return counter

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/refine_symbols_pass2.py <input_dir>")
        sys.exit(1)

    folder = sys.argv[1]
    counts = count_words(folder)

    # Use relative frequency thresholds to cut off top 2% (too common) and bottom 98% (too rare)
    total = sum(counts.values())
    freq = {w: c / total for w, c in counts.items()}
    high_cut = sorted(freq.values(), reverse=True)[int(len(freq) * 0.02)]
    low_cut = sorted(freq.values())[int(len(freq) * 0.98)]

    filtered = {w: c for w, c in counts.items() if low_cut < (c / total) < high_cut}
    top = sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:100]

    Path("outputs").mkdir(exist_ok=True)
    out_path = Path("outputs/randy_symbols_refined.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(top, f, indent=2)

    print(f"Saved refined list → {out_path}")
    print("Top 40:")
    for w, c in top[:40]:
        print(f"{w:20s} {c}")

if __name__ == "__main__":
    main()
