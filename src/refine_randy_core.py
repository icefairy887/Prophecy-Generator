#!/usr/bin/env python3
import sys, re, json, collections
from pathlib import Path
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords", quiet=True)

# Use NLTK's English stopwords as an extra safety net
STOP = set(stopwords.words("english"))
# Add your own high-frequency filler seen in the last run
STOP.update("time turn your like stop what just this with want real from they something when about because know feel still next right there more through back where someone yeah make need been keep them then".split())

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z'\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def count_terms(folder):
    counts = collections.Counter()
    for path in Path(folder).rglob("*.json"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = normalize(f.read())
            for word in text.split():
                if len(word) < 4 or word in STOP:
                    continue
                counts[word] += 1
    return counts

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/refine_randy_core.py <input_dir>")
        sys.exit(1)

    folder = sys.argv[1]
    counts = count_terms(folder)
    # Keep only mid-frequency terms (not singletons, not global spam)
    refined = [(w, c) for w, c in counts.items() if 5 < c < 10000]
    refined = sorted(refined, key=lambda x: x[1], reverse=True)
    with open("outputs/randy_core_lexicon.json", "w", encoding="utf-8") as out:
        json.dump(refined[:300], out, indent=2)
    print("Saved refined lexicon to outputs/randy_core_lexicon.json")
    print("Sample:")
    for w, c in refined[:40]:
        print(f"{w:20s} {c}")

if __name__ == "__main__":
    main()
