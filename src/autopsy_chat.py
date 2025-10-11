import json
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter

# === Load Data ===
with open('clean_conversations.json', 'r', encoding='utf-8') as f:
    conversations = json.load(f)

# === Init Analyzer ===
analyzer = SentimentIntensityAnalyzer()

# === Storage ===
user_msgs = []
gpt_msgs = []

# === Extract messages with compatibility handling ===
for convo in conversations:
    mapping = convo.get("mapping", {})
    for msg_id, msg in mapping.items():
        message = msg.get("message")
        if not message:
            continue

        role = message.get("author", {}).get("role", "")
        content_parts = message.get("content", {}).get("parts", [])
        content = ""

        if content_parts:
            part = content_parts[0]
            if isinstance(part, str):
                content = part.strip()
            elif isinstance(part, dict):
                content = part.get("text", "").strip()

        if role == "user" and content:
            user_msgs.append(content)
        elif role == "assistant" and content:
            gpt_msgs.append(content)

# === Sentiment Analysis ===
sentiments = [analyzer.polarity_scores(m)["compound"] for m in user_msgs]
average_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

# === Word Frequency ===
all_words = re.findall(r'\b\w+\b', ' '.join(user_msgs).lower())
word_counts = Counter(all_words)
top_words = word_counts.most_common(20)

# === Report ===
print("\n🩸 --- CHAT AUTOPSY REPORT --- 🩸\n")
print(f"🧠 Total User Messages: {len(user_msgs)}")
print(f"🤖 Total GPT Messages: {len(gpt_msgs)}")
print(f"📉 Average Sentiment Score: {average_sentiment:.3f}")

print("\n🔁 Top 20 Most Common Words in Your Messages:")
for word, count in top_words:
    print(f"  {word}: {count}")

# === Emotional Anchors ===
anchors = [w for w, c in word_counts.items() if c > 10 and len(w) > 3]
if anchors:
    print("\n🔂 Repetitive Emotional Anchors (used 10+ times):")
    for word in anchors:
        print(f"  {word}")
else:
    print("\n😐 No major repetition flags found.")

print("\n🧬 Done. File examined. Patterns exposed.")
