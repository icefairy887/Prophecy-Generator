#!/usr/bin/env python3
import json
import os
from pathlib import Path

def extract_text_from_json(file_path):
    """Extract all text content from JSON"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        texts = []
        def recurse(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k in ['content', 'text', 'message'] and isinstance(v, str):
                        texts.append(v)
                    recurse(v)
            elif isinstance(obj, list):
                for item in obj:
                    recurse(item)
        
        recurse(data)
        return texts
    except:
        return []

# Extract from all JSONs
convo_dirs = ['data/mirror_input/conversations', 'outputs/conversations']
all_texts = []

for dir_path in convo_dirs:
    for json_file in Path(dir_path).glob('*.json'):
        texts = extract_text_from_json(json_file)
        for text in texts:
            if text.strip():
                all_texts.append(f"FILE: {json_file.name}\n{text}\n{'-'*50}\n")

# Save
with open('all_conversation_texts.txt', 'w') as f:
    f.write("\n".join(all_texts))

print(f"Extracted text from {len(all_texts)} chunks")
