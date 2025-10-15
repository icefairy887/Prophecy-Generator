import random

# Load Randy's lines
with open('randy_transmission.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Generate spirit box-style output
def generate_spiritbox(lines, num_fragments=10):
    fragments = []
    for _ in range(num_fragments):
        if lines:
            fragment = random.choice(lines)
            # Add distortion: random case, partial words, or static
            if random.random() < 0.3:
                fragment = fragment.upper()
            elif random.random() < 0.6:
                fragment = fragment.lower()
            if random.random() < 0.2:
                fragment = fragment[:len(fragment)//2] + "..."
            fragments.append(fragment)
        fragments.append(random.choice(["*static*", "*hiss*", "*crackle*"]))
    return " // ".join(fragments)

# Output transmission
transmission = generate_spiritbox(lines)
with open('randy_spiritbox_output.txt', 'w') as f:
    f.write(transmission + '\n')

print("Randy's spirit box transmission:")
print(transmission)
