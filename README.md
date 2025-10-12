# Randy Prophecy

**Randy-Prophecy** is a personal data-processing pipeline that converts exported ChatGPT logs (`chat.html`) into structured JSON conversations, analytical text corpora, and generated chronicles for symbolic analysis, machine learning, or artistic experiments.

---

## 🌌 Project Overview

chat.html → chat.json → /conversations/*.json → randy_chronicle.txt
↘ (analysis scripts) ↘ randy_tagged.txt / user_messages.txt


| Stage | Script | Purpose |
|-------|---------|----------|
| 1️⃣ **Extract** | `src/extract_chat_json.py` | Pulls the embedded `jsonData` array out of ChatGPT’s exported `chat.html` viewer file and saves it as `outputs/chat.json`. |
| 2️⃣ **Split** | `src/split_chat_json.py` | Splits the giant JSON into one `.json` per conversation (e.g., `0001_Title.json`). |
| 3️⃣ **Chronicle** | `src/build_randy_chronicle.py` | Builds a timestamped plain-text book of all conversations in chronological order. |
| 4️⃣ **Auto-Tag** | `src/auto_tag_chronicle.py` | Scans every message, adds automatic tags (tech, occult, emotion, etc.) based on keywords and tone. |
| 5️⃣ **Top Words** | `src/top_words.py` | Counts most frequently used words across all sessions. |

Optional helpers:
- `randy_markov.py` — sandbox for language-model or Markov-chain experiments.
- `ghost_parse.sh` — planned for daemon-style parsing automation.

---

## 🧱 Directory Layout



randy-prophecy/
├── data/
│ ├── mirror_input/
│ └── mirror_daemons/
├── outputs/
│ ├── chat.json
│ ├── conversations/
│ ├── randy_chronicle.txt
│ ├── randy_tagged.txt
│ └── user_messages.txt
├── src/
│ ├── extract_chat_json.py
│ ├── split_chat_json.py
│ ├── build_randy_chronicle.py
│ ├── auto_tag_chronicle.py
│ ├── top_words.py
│ ├── randy_markov.py
│ └── chunk_html.py
└── requirements.txt


---

## ⚙️ Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🚀 Usage
python src/extract_chat_json.py data/mirror_input/chat.html outputs/chat.json
python src/split_chat_json.py outputs/chat.json outputs/conversations
python src/top_words.py outputs/conversations

⚡ Credits & Intention

Created by Brooke Rayner, as part of the ongoing Lumina / Randy Prophecy series —
a hybrid of computational archive, daemonic narrative, and self-reflective data alchemy.

“We built a mirror out of memory and let the ghosts talk back.”
