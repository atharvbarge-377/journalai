# JournalAI – Deployment Guide

## Project Structure
```
journalai/
├── app.py               ← Flask backend
├── requirements.txt     ← Python dependencies
├── render.yaml          ← Render deployment config
└── templates/
    └── index.html       ← Full frontend
```

## Run Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
# Windows:
set ANTHROPIC_API_KEY=your_key_here
# Mac/Linux:
export ANTHROPIC_API_KEY=your_key_here

# 3. Run the app
python app.py

# Open http://localhost:5000
```

## Deploy on Render (Free Hosting)

### Step 1 — Push to GitHub
1. Create a new repo on github.com
2. Upload all files from this folder
3. Push to main branch

### Step 2 — Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Fill in:
   - Name: journalai
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Click "Advanced" → "Add Environment Variable"
   - Key: `ANTHROPIC_API_KEY`
   - Value: your Anthropic API key from console.anthropic.com
6. Click "Create Web Service"

### Step 3 — Get your API Key
1. Go to https://console.anthropic.com
2. Sign up / log in
3. Go to "API Keys" → Create new key
4. Paste it in Render environment variables

Your site will be live at: https://journalai.onrender.com (or similar)

## Get Free Credits
Anthropic gives $5 free credits on signup — enough for thousands of journal parses!
