#!/bin/bash
echo "🚀 Setting up Randy Prophecy Pipeline..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo "✅ Setup complete! Run: source venv/bin/activate"
