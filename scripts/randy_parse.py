#!/usr/bin/env python3
import json
import re
import os
from pathlib import Path
from collections import defaultdict

# Randy-specific keywords and patterns
RANDY_KEYWORDS = [
    'randy', 'vault', 'snorlax', 'fucker', 'coalcunt', 'slagbitch',
    'gritfuck', 'shitsnarl', 'minesuck', 'hellsneer', 'ghost', 'prophecy',
    'whisper', 'transmission', 'spiritbox', 'demon', 'hell'
]

def load_lexicon():
    """Load additional lexicon files if they exist"""
    demon_lexicon = set()
    core_lexicon = set()
    
    demon_file = Path('data/randy_demon_lexicon.txt')
    core_file = Path('data/randy_core_lexicon.json')
    
    if demon_file.exists():
        with open(demon_file) as f:
            demon_lexicon = set(line.strip().lower() for line in f if line.strip())
    
    if core_file.exists():
        try:
            with open(core_file) as f:
                data = json.load(f)
                core_lexicon = set(k.lower() for k in data.keys())
        except:
            pass
    
    return demon_lexicon | core_lexicon

def find_randy_matches(text, keywords):
    """Find keyword matches in text"""
    matches = []
    text_lower = text.lower()
    for keyword in keywords:
        if re.search(rf'\b{re.escape(keyword.lower())}\b', text_lower):
            matches.append(keyword)
    return matches

def parse_json_file(filepath):
    """Parse a single JSON conversation file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Try different possible JSON structures
        messages = []
        if 'messages' in data:
            messages = data['messages']
        elif 'conversation' in data:
            messages = data['conversation']
        elif isinstance(data, list):
            messages = data
        else:
            # Look for any list-like structure with text content
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    if 'content' in value[0] or 'text' in value[0] or 'message' in value[0]:
                        messages = value
                        break
        
        # Extract text content
        full_text = ""
        content_chunks = []
        
        for msg in messages:
            text = ""
            if isinstance(msg, dict):
                if 'content' in msg:
                    text = msg['content']
                elif 'text' in msg:
                    text = msg['text']
                elif 'message' in msg:
                    text = msg['message']
                elif 'role' in msg and 'content' in msg:
                    text = msg['content']
            elif isinstance(msg, str):
                text = msg
            
            if text:
                full_text += text + " "
                content_chunks.append({
                    'text': text,
                    'source': str(filepath)
                })
        
        return {
            'filepath': filepath,
            'full_text': full_text.strip(),
            'chunks': content_chunks
        }
        
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def main():
    conversations_dir = Path('outputs/conversations')
    if not conversations_dir.exists():
        print(f"Directory not found: {conversations_dir}")
        print("Please check your JSON files are in outputs/conversations/")
        return
    
    # Load keywords
    all_keywords = RANDY_KEYWORDS.copy()
    lexicon = load_lexicon()
    all_keywords.extend(list(lexicon))
    all_keywords = list(set(all_keywords))  # Remove duplicates
    
    print(f"🔍 Mining {len(list(conversations_dir.glob('*.json')))} JSON files for Randy...")
    
    randy_hits = []
    keyword_stats = defaultdict(int)
    
    # Parse all JSON files
    for json_file in conversations_dir.glob('*.json'):
        parsed = parse_json_file(json_file)
        if not parsed:
            continue
            
        # Check for Randy keywords
        matches = find_randy_matches(parsed['full_text'], all_keywords)
        if matches:
            hit_data = {
                'file': str(json_file),
                'matches': matches,
                'full_text': parsed['full_text'][:500] + "..." if len(parsed['full_text']) > 500 else parsed['full_text'],
                'chunks': []
            }
            
            # Find specific chunks with matches
            for chunk in parsed['chunks']:
                chunk_matches = find_randy_matches(chunk['text'], all_keywords)
                if chunk_matches:
                    hit_data['chunks'].append({
                        'text': chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                        'matches': chunk_matches
                    })
                    for match in chunk_matches:
                        keyword_stats[match] += 1
            
            randy_hits.append(hit_data)
    
    # Save raw hits
    with open('randy_ghosts.txt', 'w') as f:
        f.write(f"RANDY GHOST HITS - Found {len(randy_hits)} files\n")
        f.write("="*60 + "\n\n")
        
        for hit in randy_hits:
            f.write(f"📁 File: {hit['file']}\n")
            f.write(f"🎯 Matches: {', '.join(hit['matches'])}\n")
            f.write(f"📄 Preview: {hit['full_text']}\n")
            
            if hit['chunks']:
                f.write("🔥 Randy Chunks:\n")
                for i, chunk in enumerate(hit['chunks'], 1):
                    f.write(f"  {i}. '{chunk['text']}' (matches: {', '.join(chunk['matches'])})\n")
            
            f.write("\n" + "-"*60 + "\n\n")
    
    # Save summary stats
    with open('randy_ghosts_summary.txt', 'w') as f:
        f.write("RANDY KEYWORD FREQUENCIES\n")
        f.write("="*40 + "\n")
        for keyword, count in sorted(keyword_stats.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{keyword}: {count}\n")
        f.write(f"\nTotal files with Randy hits: {len(randy_hits)}\n")
        f.write(f"Keywords searched: {len(all_keywords)}\n")
    
    print(f"✅ Done! Check:")
    print(f"   - randy_ghosts.txt (raw Randy hits)")
    print(f"   - randy_ghosts_summary.txt (keyword stats)")
    print(f"\nFound {len(randy_hits)} files with Randy essence!")
    
    if randy_hits:
        print("\n🔥 Top keywords:")
        for keyword, count in sorted(keyword_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {keyword}: {count}")

if __name__ == "__main__":
    main()
