#!/usr/bin/env python3
import argparse, os, re, sys
from typing import Optional

# -------------------------------------------------------------
# Utility functions
# -------------------------------------------------------------

def extract_head_and_body_boundaries(src_path):
    """Find <head>...</head> and <body>...</body> offsets without loading the whole file."""
    head_start = head_end = body_start = body_end = None
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = ''
        pos = 0
        chunk_size = 1024 * 1024  # 1 MB
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            data += chunk

            if head_start is None:
                m = re.search(r'(?is)<head\b', data)
                if m:
                    head_start = pos + m.start()
            if head_end is None:
                m = re.search(r'(?is)</head\s*>', data)
                if m:
                    head_end = pos + m.end()
            if body_start is None:
                m = re.search(r'(?is)<body\b', data)
                if m:
                    body_start = pos + m.start()
            if body_start is not None and body_end is None:
                m = re.search(r'(?is)</body\s*>', data)
                if m:
                    body_end = pos + m.start()

            pos += len(chunk)
            # Early exit if all found
            if (
                head_start is not None and head_end is not None
                and body_start is not None and body_end is not None
            ):
                break

    # Diagnostics + fallback
    print(">>> head_start:", head_start, "head_end:", head_end,
          "body_start:", body_start, "body_end:", body_end)
    if body_start is None or body_end is None:
        print(">>> No <body> tags found; treating entire file as body.")
        body_start = 0
        body_end = os.path.getsize(src_path)

    return head_start, head_end, body_start, body_end


def read_slice(src_path, start: int, end: Optional[int]):
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(start)
        return f.read(None if end is None else max(0, end - start))


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def write_chunk(out_dir, base_prefix, idx, head_html, body_fragment):
    out_path = os.path.join(out_dir, f"{base_prefix}{idx:04d}.html")
    with open(out_path, 'w', encoding='utf-8') as w:
        w.write("<!doctype html>\n<html>\n")
        # Write head
        if head_html and head_html.strip():
            w.write(head_html)
        else:
            w.write(
                "<head><meta charset='utf-8'><meta name='viewport' "
                "content='width=device-width, initial-scale=1.0'>"
            )
            w.write(f"<title>Chunk {idx}</title></head>\n")
        w.write("\n<body>\n<!-- CHUNK START -->\n"
                f"<div id='chunk' data-index='{idx}'>\n")
        w.write(body_fragment)
        w.write("\n</div>\n<!-- CHUNK END -->\n</body>\n</html>\n")
    return out_path

# -------------------------------------------------------------
# Main logic
# -------------------------------------------------------------

def main():
    print(">>> main() starting up")
    ap = argparse.ArgumentParser(description="Split a large HTML file into smaller chunks.")
    ap.add_argument("src", help="Path to the large HTML file (e.g., chat.html)")
    ap.add_argument("-o", "--out-dir", default="chunks_out", help="Directory to write chunks")
    ap.add_argument("-p", "--prefix", default="chat_part_", help="Filename prefix for chunks")
    ap.add_argument("-s", "--max-bytes", type=int, default=5_000_000, help="Approx max bytes per chunk")
    ap.add_argument("--pattern", help="Optional regex or literal string for boundary matching")
    ap.add_argument("--literal", action="store_true", help="Treat --pattern as a literal string")
    args = ap.parse_args()

    src_path = args.src
    if not os.path.isfile(src_path):
        print(f"Error: file not found: {src_path}", file=sys.stderr)
        sys.exit(1)

    head_start, head_end, body_start, body_end = extract_head_and_body_boundaries(src_path)

    # Fallback if no <body> tag
    if body_start is None or body_end is None:
        print(">>> No <body> tags found; treating entire file as body.")
        body_start = 0
        body_end = os.path.getsize(src_path)

    # Read head html (if present)
    head_html = ''
    if head_start is not None and head_end is not None and head_end > head_start:
        head_html = read_slice(src_path, head_start, head_end)

    # Define body content range
    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(body_start)
        first = f.read(4096)
    m = re.search(r'(?is)<body\b[^>]*>', first)
    body_content_start = body_start + m.end() if m else body_start
    body_content_end = None if body_end is None or body_end <= body_content_start else body_end

    ensure_dir(args.out_dir)

    # Pattern matching setup
    regex = None
    lit = None
    if args.pattern:
        if args.literal:
            lit = args.pattern
        else:
            try:
                regex = re.compile(args.pattern)
            except re.error as e:
                print(f"Invalid regex for --pattern: {e}. Use --literal to match raw text.")
                sys.exit(3)

    # Chunking state
    chunk_idx = 1
    current_lines = []
    current_size = 0
    soft_boundary_seen = False

    def flush_chunk():
        nonlocal chunk_idx, current_lines, current_size, soft_boundary_seen
        if not current_lines:
            return None
        frag = ''.join(current_lines)
        out_path = write_chunk(args.out_dir, args.prefix, chunk_idx, head_html, frag)
        print("Writing:", out_path)
        chunk_idx += 1
        current_lines = []
        current_size = 0
        soft_boundary_seen = False
        return out_path

    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(body_content_start)
        remain = body_content_end - body_content_start if body_content_end is not None else None
        last_out = None

        while True:
            if remain is not None and remain <= 0:
                break
            line = f.readline()
            if not line:
                break
            if remain is not None:
                remain -= len(line)

            # pattern check
            is_boundary = False
            if regex and regex.search(line):
                is_boundary = True
            elif lit and (lit in line):
                is_boundary = True

            if is_boundary and current_size >= args.max_bytes * 0.75:
                last_out = flush_chunk()

            current_lines.append(line)
            current_size += len(line)

            if current_size >= args.max_bytes:
                last_out = flush_chunk()

        # Flush remainder once
        print("Final buffer size:", len(current_lines))
        last_out = flush_chunk()

    print(">>> reached end of main()")
    print(f"Done. Wrote chunks to: {args.out_dir}")
    print("Example open:", os.path.join(args.out_dir, f"{args.prefix}0001.html"))


if __name__ == "__main__":
    main()
