#!/usr/bin/env python3
import re, json, sys, os

def main():
    if len(sys.argv) < 3:
        print("Usage: extract_chat_json.py <input_html> <output_json>")
        sys.exit(1)

    src = sys.argv[1]
    out = sys.argv[2]

    with open(src, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # Find the massive JSON assignment
    m = re.search(r'var\s+jsonData\s*=\s*(\[.*?\])\s*[,;]?\s*(?:var|function|window|document|</script|$)', text, re.S)
    if not m:
        print("Could not find jsonData array in file.")
        sys.exit(2)

    json_text = m.group(1)

    # Try to parse to validate
    try:
        data = json.loads(json_text)
    except Exception as e:
        print("Warning: JSON parse failed, writing raw text. Error:", e)
        data = None

    # Save a clean copy
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as w:
        if data is not None:
            json.dump(data, w, ensure_ascii=False, indent=2)
        else:
            w.write(json_text)

    print(f"Extracted JSON to {out}")
    if data is not None:
        print(f"Conversations: {len(data)}")

if __name__ == "__main__":
    main()
