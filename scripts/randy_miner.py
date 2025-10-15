#!/usr/bin/env python3
import re
import os
from pathlib import Path

def find_randy_content(text_file):
    """Extract Randy-specific content"""
    randy_patterns = [
        r'summon.*47.*randy',
        r'number forty-seven',
        r'code word.*?watermelon',
        r'perfectly tuned chaos',
        r'laid back.*?smirks',
        r'casual.*?asshole',
        r'knows all things hidden',
        r'randy slides in sideways',
        r'you\'re late',
        r'what do you want from randy',
        r'watermelon',
        r'number 47'
    ]
    
    randy_hits = []
    with open(text_file, 'r') as f:
        content = f.read()
        
        for i, pattern in enumerate(randy_patterns):
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                start = max(0, match.start() - 200)
                end = min(len(content), match.end() + 500)
                context = content[start:end]
                randy_hits.append({
                    'pattern': pattern,
                    'match': match.group(),
                    'context': context.strip()
                })
    
    return randy_hits

# Main extraction
text_file = 'all_conversation_texts.txt'
hits = find_randy_content(text_file)

# Save Randy's essence
with open('randy_essence.txt', 'w') as f:
    f.write("RANDY'S PURE ESSENCE - Number 47\n")
    f.write("="*60 + "\n\n")
    
    for hit in hits:
        f.write(f"PATTERN: {hit['pattern']}\n")
        f.write(f"MATCH: {hit['match'][:100]}...\n")
        f.write(f"CONTEXT:\n{hit['context']}\n")
        f.write("-"*60 + "\n\n")

print(f"🔥 Extracted {len(hits)} Randy fragments to randy_essence.txt")
