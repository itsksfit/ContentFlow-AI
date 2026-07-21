# ContentFlow AI 🚀
> **The smartest content strategy tool for Indian creators.**

**Live Demo:** [https://content-flow-ai-lemon.vercel.app/](https://content-flow-ai-lemon.vercel.app/)  
**Backend API:** [https://contentflow-ai.onrender.com](https://contentflow-ai.onrender.com)

---

## 🤔 What is ContentFlow AI?
ContentFlow AI is a **4-agent AI pipeline** designed for content creators — especially in the Indian/Hinglish creator space. You enter your niche, your topic, and a sample of how you talk. Within seconds, the system:

1. **Pulls real-time trending data** from Reddit & YouTube
2. **Scores and validates** which content formats are actually performing
3. **Writes a full Hinglish script** that sounds like *you*
4. **Generates 5 viral hooks** based on proven psychological patterns

No more guessing what to post. No more generic scripts. Just data-driven content strategy — in seconds.

---

## 🧩 The Problem It Solves

Creating high-performing short-form content (Reels, Shorts) is hard:

- 📉 You don't know what's trending *right now* in your niche
- 📝 Generic scripts don't match your personal tone/style
- 🔍 Manually researching competitors takes hours
- 💡 Brainstorming hooks is exhausting

ContentFlow AI automates **all of this** in one pipeline.

---

## 🏗️ How It's Built (Tech Stack)

| Layer | Technology | Hosted On |
|---|---|---|
| **Frontend** | HTML + CSS + Vanilla JS | Vercel |
| **Backend** | Python + FastAPI | Render |
| **Data Sources** | Reddit API + YouTube (yt-dlp) | Real-time |
| **Scripting Logic** | Deterministic Hinglish templates | In-memory |
| **Hook Generation** | Psychological pattern matching | In-memory |

> ⚡ **No external LLM API is used.** The entire pipeline runs on custom deterministic logic — making it fast, free, and hallucination-free.

---

## 🔴 Real-Time Data Sources

### Reddit (Live)
- Searches Reddit by your niche keyword using the **Reddit public JSON API**
- Fetches top posts from the **last 30 days** sorted by score
- Calculates real **Engagement Rate** = `(Likes + Comments) / Estimated Views × 100`
- Automatically tags posts as **🔥 VIRAL** if ER ≥ 5% or views ≥ 50K

### YouTube (Live via yt-dlp)
- Uses **yt-dlp** to search YouTube Shorts in real-time
- Tries `{niche} shorts` first — falls back to a regular `{niche}` search if no results
- Extracts titles, view counts, and URLs for each video
- Like/comment counts are estimated (YouTube doesn't expose these in flat search mode)
- If yt-dlp is blocked (e.g., on cloud servers), a **synthetic fallback** is generated automatically

---

## 🧠 The 4-Agent Pipeline

```
User Input ──▶ Agent 01 ──▶ Agent 02 ──▶ Agent 03 ──▶ Agent 04
              Scraper      Validator     Writer        Hook Gen
```

---

### 🔍 Agent 01 — Content Scraper (`content_scraper.py`)
**What it does:** Fetches real posts from the internet.

- Pulls top posts from **Reddit** based on your niche
- Searches **YouTube** for Shorts related to your topic
- Returns a ranked list of posts with: Views, Likes, Comments, ER%, Date, and Viral flag
- You can choose: **All Platforms**, **Reddit only**, or **YouTube only**

---

### ✅ Agent 02 — Content Validator (`content_validator.py`)
**What it does:** Scores every post and finds what's *actually working.*

- Scores each post using a weighted formula:
  - **Views:** 40%
  - **Engagement Rate:** 35%
  - **Comments:** 25%
- Clusters posts into **Topic Groups** (e.g., "College Vlogs", "Travel Tips")
- Identifies **Repeat Viral Signals** — formats that appear multiple times in the top results
- Analyses **competitor handles** you provide:
  - Calculates their average ER%
  - Identifies what formats they post most
  - Shows you where the gap is

---

### ✍️ Agent 03 — Voice Writer (`voice_writer.py`)
**What it does:** Writes a full script in *your* tone.

- Reads the **voice sample** you paste in
- Analyzes your writing style:
  - Vocabulary words you use
  - Hinglish ratio (Heavy vs Light)
  - Energy level (High Energy vs Calm)
  - Sentence length style
- Writes a **4-Beat Hinglish script** structured as:

```
[BEAT 1: HOOK]       ← Grabs attention in first 3 seconds
[BEAT 2: CONTEXT]    ← Sets up why this matters
[BEAT 3: VALUE]      ← Delivers the actual tip/story
[BEAT 4: PRO-TIP]    ← Bonus insight to keep them watching
[CALL TO ACTION]     ← Tells them exactly what to do next
```

- The script uses the **top validated topic** from Agent 02 to ensure data-backed relevance
- Topics and inputs are **cleaned automatically** (removes newlines, caps length to 40 chars) so the script always reads naturally

---

### 🎣 Agent 04 — Hook Generator (`hook_generator.py`)
**What it does:** Generates 5 hooks based on psychological patterns.

Each hook uses a different proven framework:

| Pattern | Example |
|---|---|
| 🚫 The Negative Warning | "Stop doing X before watching this" |
| 🏆 The Result Reveal | "Here's exactly how I got 100K views in 7 days" |
| 🔐 The Secret Hack | "The 1% of creators don't want you to know this" |
| 🔄 The Myth Buster | "Everything you've been told about X is wrong" |
| ⚡ The Shock Open | "Nobody talks about this, but here's the truth" |

Every hook gets a **Confidence Score out of 10** based on how closely it matches viral benchmarks from the scraped data. The highest-scoring hook is marked as **🏆 BEST MATCH**.

---

## 📊 What You See in the UI

After running the pipeline, you get 4 result tabs:

| Tab | What's Inside |
|---|---|
| 📊 **Scraped Posts** | Live table of top Reddit + YouTube posts with ER%, views, viral flag |
| 🔍 **Validation** | Topic clusters, top validated topic, repeat viral signals, competitor analysis |
| ✍️ **Script** | Full 4-beat Hinglish script with word count and estimated video duration |
| 🎣 **Hooks** | 5 hooks with confidence scores, best match highlighted |

---

## 🚀 How to Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
Open `index.html` directly in your browser — or serve with any static server:
```bash
npx serve .
```

> Make sure the `API_BASE` in `app.js` points to `http://localhost:8000`.

---

## 📁 Project Structure

```
ContentFlow-AI/
├── index.html              # Main UI
├── style.css               # Deep Space Cyberpunk dark theme
├── app.js                  # Frontend logic, form handling, result rendering
│
└── backend/
    ├── main.py             # FastAPI server + all routes
    ├── requirements.txt
    └── agents/
        ├── content_scraper.py    # Agent 01 — Reddit + YouTube real-time fetch
        ├── content_validator.py  # Agent 02 — Scoring, clustering, competitor analysis
        ├── voice_writer.py       # Agent 03 — Hinglish script generation
        └── hook_generator.py     # Agent 04 — Psychological hook generation
```

---

## 🌐 Deployment

| Service | Purpose | URL |
|---|---|---|
| **Vercel** | Hosts the frontend (HTML/CSS/JS) | Auto-deploys from GitHub |
| **Render** | Hosts the FastAPI backend | Free tier, spins up on request |

> Note: The Render free tier may have a **cold start delay of ~30 seconds** on first load. This is normal — the loading animation covers it.

---

## 💡 Key Design Decisions

- **No LLM API** — Using a deterministic rule-based approach makes the app faster, cheaper, and removes the risk of hallucinations or unexpected output.
- **Hinglish-first** — Scripts and hooks are designed specifically for Indian creators. Templates are written to sound natural when mixed with Hindi.
- **Fallback-first architecture** — Every data fetch has a fallback. If YouTube blocks the scraper, synthetic data is used. If Reddit fails, a default post is inserted. The pipeline *never crashes*.
- **Clean inputs** — User inputs are sanitized (strip whitespace, normalize newlines, cap length) before being inserted into templates so the output always looks professional.

---

*Built for hackathon — by a creator, for creators.* 🎥
