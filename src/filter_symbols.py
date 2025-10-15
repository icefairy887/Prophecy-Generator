#!/usr/bin/env python3
import sys, re, collections
from pathlib import Path

TECH_NOISE = set("""
android app domain format width height bytes datetime tool org auto entries invalid profile usd mdl udd
code codes coding function script scripts run running execute executed command commands bash termux system sys kernel text txt file files data dataset datasets json csv html com name path paths dir directory directories output input variable variables param parameter params config terminal shell linux python version install clone repo github git env venv virtual import print type class object value values key keys line lines start step end return def while for if else elif true false null none read write open close append log error debug warn warning result results output process processes model models metadata content token tokens url urls https http index indices source sources ref refs reference references citation citations default async complete completion parts search channel request response role author recipient message messages absolute finished success successfully update create parent children weight slug timestamp voice audio image gizmo mode user assistant attribution
""".split())

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z'\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def count_words(input_dir):
    counts = collections.Counter()
    for path in Path(input_dir).rglob("*.json"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = normalize(f.read())
            for word in text.split():
                if len(word) <= 2:
                    continue
                if word in TECH_NOISE:
                    continue
                counts[word] += 1
    return counts

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/filter_symbols.py <input_dir>")
        sys.exit(1)
    counts = count_words(sys.argv[1])
    filtered = [(w, c) for w, c in counts.most_common(100) if not re.match(r"^[a-z]{1,3}$", w)]
    print("Top symbolic vocabulary:")
    for w, c in filtered:
        print(f"{w:20s} {c}")

if __name__ == "__main__":
    main()
