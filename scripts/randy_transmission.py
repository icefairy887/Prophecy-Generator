import re

# Randy-specific keywords
keywords = r'\b(randy|fucker|vault|coalcunt|gritfuck|shitsnarl|minesuck|hellsneer)\b'
keyword_re = re.compile(keywords, re.I)

# Input and output files
input_file = 'data/spiritbox_transmissions.txt'
output_file = 'randy_transmission.txt'

randy_lines = []
with open(input_file, 'r') as f:
    for line in f:
        if keyword_re.search(line):
            randy_lines.append(line.strip())

# Write Randy-only lines
with open(output_file, 'w') as f:
    for line in randy_lines:
        f.write(line + '\n')

print(f"Extracted {len(randy_lines)} Randy-related transmissions to {output_file}")
