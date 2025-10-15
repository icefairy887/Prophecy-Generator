#!/usr/bin/env python3
import sys, re, json, collections
from pathlib import Path

# final exclusions: conversational + tech + glue words
EXCLUDE = set("""
safe dafb line high going means close first nbecause said actually home nthe urls feels word android help group step anything invalid okay things auto kind nick love look domain show else nnot give enough format width entries everything more less really something anything nothing anyone everyone somebody somehow
and the for from with this that what when where which whose whom while then than into onto through about above below under over before after because since though although despite during against toward toward towards across within without between among until upon each both either neither any some no not yes yeah okay sure right wrong here there way kind type sort cause effect again still even almost nearly maybe probably might must shall will would could should can cannot isn't aren't wasn't weren't haven't hasn't hadn't doesn't didn't don't didn't wasn't won't wouldn't shouldn't couldn't had has have did does do i'm i've i'd i'll you're you'd you'll we've we'd we'll they're they'd they'll he's she'd he'll it's that's there's what's who's how's let's
url html json txt csv py sh bin sys linux python termux android bash command run running process data dataset model code file folder directory dir path repo git github env config variable param def class object import export input output print append open close write read return index key value type arg args argsort function script terminal shell venv virtual install uninstall execute exec command prompt system kernel clone push pull branch commit merge
""".split())

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z'\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def count_words(input_dir):
    counter = collections.Counter()
    for path in Path(input_dir).rglob("*.json"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = normalize(f.read())
            for w in text.split():
                if len(w) < 4 or w in EXCLUDE:
                    continue
                counter[w] += 1
    return counter

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/distill_randy_symbols.py <input_dir>")
        sys.exit(1)
    folder = sys.argv[1]
    counts = count_words(folder)
    # Keep moderate frequency words
    filtered = [(w, c) for w, c in counts.items() if 10 < c < 5000]
    filtered = sorted(filtered, key=lambda x: x[1], reverse=True)
    Path("outputs").mkdir(exist_ok=True)
    out_path = Path("outputs/randy_symbols.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(filtered[:300], f, indent=2)
    print(f"Saved refined symbol list → {out_path}")
    print("Top 40 symbolic words:")
    for w, c in filtered[:40]:
        print(f"{w:20s} {c}")

if __name__ == "__main__":
    main()
