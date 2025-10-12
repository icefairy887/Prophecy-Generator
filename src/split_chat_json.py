#!/usr/bin/env python3
import json, os, sys

def main():
    if len(sys.argv) < 3:
        print("Usage: split_chat_json.py <input_json> <output_dir>")
        sys.exit(1)

    src = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} conversations.")

    for i, convo in enumerate(data, start=1):
        # Try to make a clean title for the filename
        title = convo.get("title", f"conversation_{i}") or f"conversation_{i}"
        safe_title = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in title)[:60]
        out_path = os.path.join(out_dir, f"{i:04d}_{safe_title}.json")

        with open(out_path, "w", encoding="utf-8") as w:
            json.dump(convo, w, ensure_ascii=False, indent=2)

        if i % 100 == 0:
            print(f"→ {i} saved...")

    print(f"Done. Saved {len(data)} conversations to {out_dir}")

if __name__ == "__main__":
    main()
