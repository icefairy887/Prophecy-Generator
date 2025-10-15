#!/usr/bin/env python3
import re
from pathlib import Path

def find_randy_wormhole_content(text_file):
    """Aggressive search for Randy + wormhole patterns"""
    patterns = [
        r'randy', r'47', r'watermelon', r'wormhole', r'number\s*47', r'forty[- ]seven',
        r'summon.*?randy', r'slides?\s+in', r'you\'?re?\s*late', r'code\s*word',
        r'perfectly?\s*tuned?\s*chaos', r'laid\s*back', r'casual.*asshole',
        r'knows?\s+all?\s+things?\s+hidden', r'forbidden', r'taboo', r'forgotten'
    ]
    
    hits = []
    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            matched_patterns = []
            
            for pattern in patterns:
                if re.search(pattern, line_lower, re.IGNORECASE):
                    matched_patterns.append(pattern)
            
            if matched_patterns:
                context_start = max(0, i-5)
                context_end = min(len(lines), i+10)
                context = ''.join(lines[context_start:context_end])
                
                hits.append({
                    'line_num': i+1,
                    'line': line.strip(),
                    'patterns': matched_patterns,
                    'context': context.strip()
                })
    
    return hits

# Run extraction
text_file = 'all_conversation_texts.txt'
if Path(text_file).exists():
    hits = find_randy_wormhole_content(text_file)
    
    with open('randy_wormhole_essence.txt', 'w') as f:
        f.write(f"RANDY + WORMHOLE ESSENCE - {len(hits)} hits\n")
        f.write("="*60 + "\n\n")
        
        for hit in hits:
            f.write(f"LINE {hit['line_num']}: {hit['line']}\n")
            f.write(f"PATTERNS: {', '.join(hit['patterns'])}\n")
            f.write(f"CONTEXT:\n{hit['context'][:1000]}...\n")
            f.write("-"*60 + "\n")
    
    print(f"🔥 Found {len(hits)} Randy/wormhole fragments!")
    print("Check randy_wormhole_essence.txt")
else:
    print(f"❌ {text_file} not found. Run extract_text.py first!")
