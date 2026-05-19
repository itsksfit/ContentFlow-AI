# ContentFlow AI 🚀

ContentFlow AI is a 4-agent AI pipeline designed to help creators generate viral content strategies, scripts, and hooks automatically. 

## 🤖 The 4 Agents

1. **Agent 01: content-scraper** 🔍
   - Scrapes viral reels and shorts from Instagram, YouTube, and Twitter/X based on your niche and competitors.
   - Flags "VIRAL 🔥" posts that have >5% Engagement Rate or >100K views.

2. **Agent 02: content-validator** ✅
   - Scores every post based on views, engagement rate, and comments.
   - Filters out low-performing signals and clusters trends by topic.

3. **Agent 03: my-voice-writer** ✍️
   - Analyzes your provided past scripts to extract your exact Hinglish tone, vocabulary, and pacing.
   - Writes a fresh 4-beat structure script completely in your unique voice.

4. **Agent 04: hook-generator** 🎣
   - Generates 5 distinct hook patterns designed to grab attention in under 3 seconds.
   - Assigns confidence scores to each hook and matches them with successful past trends.

## 🚀 How to Run Locally

### 1. Start the Backend API (FastAPI)
The backend requires Python and Uvicorn. Navigate to the `backend` folder and run:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
*(The backend runs on `http://localhost:8000`)*

### 2. Start the Frontend Dashboard
Open a new terminal at the root of the project and run a simple HTTP server:
```bash
python -m http.server 3000
```
Then, open your browser and navigate to: **`http://localhost:3000`**

---
*Built for creators. Powered by AI.*
