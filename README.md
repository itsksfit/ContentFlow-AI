# ContentFlow AI 🚀 

**Live Demo:** [https://ks-contentflow-ai.netlify.app/](https://ks-contentflow-ai.netlify.app/)

**An intelligent 4-Agent AI Pipeline for creators to generate viral strategies, scripts, and hooks.**

---

## 📌 The Problem
Creating high-performing short-form content (Reels, Shorts, TikToks) is incredibly time-consuming. Creators have to manually research competitors, figure out what's trending, write scripts that sound authentic to them, and brainstorm engaging hooks. It's an exhausting, manual workflow.

## 💡 The Solution
**ContentFlow AI** automates the entire ideation and scripting process. By breaking the workflow down into **4 specialized AI agents**, it aggregates data, validates trends, and uses advanced Large Language Models (LLMs) to write highly targeted scripts and hooks in seconds.

---

## 🏗️ System Architecture (How it was built)

This project was built from scratch using a modern, decoupled architecture:

- **Frontend (UI/UX):** Built with pure HTML, CSS, and Vanilla JavaScript for maximum performance and a beautiful, dark-mode glassmorphism aesthetic. Hosted on **Netlify**.
- **Backend (API):** Built using **Python & FastAPI**. This serves as the brain of the operation, handling CORS, routing, and executing the agents asynchronously. Hosted on **Render**.
- **AI / LLM Integration:** Powered by the **Groq API** running the `Llama3-8b-8192` model. Groq was chosen for its blazing-fast inference speeds, allowing the multi-agent pipeline to resolve in mere seconds.

---

## 🧠 The 4-Agent Pipeline Explained

When a user clicks "Launch Pipeline," the backend triggers four sequential Python agents:

### 1. Agent 01: The Scraper (`content_scraper.py`) 🔍
- **Function:** Data Aggregation.
- **How it works:** It takes the user's niche and competitor handles and pulls top posts across Instagram, YouTube, and Twitter/X from the last 7 days.
- **Key Feature:** It automatically tags posts as **"VIRAL 🔥"** if they meet a specific threshold (e.g., Engagement Rate > 5% or >100K views).

### 2. Agent 02: The Validator (`content_validator.py`) ✅
- **Function:** Data Filtering & Scoring.
- **How it works:** It takes the raw scraped data and scores every post based on an algorithm (Views 40% + ER 35% + Comments 25%). 
- **Key Feature:** It filters out low-performing signals, clusters the data into specific topics (e.g., "AI Automation", "Tutorials"), and identifies "Repeat Viral Signals" so the creator knows exactly what format is currently dominating the algorithm.

### 3. Agent 03: The Voice Writer (`voice_writer.py`) ✍️
- **Function:** Tone Matching & Script Generation.
- **How it works:** This agent connects to the **Groq LLM**. It analyzes a provided sample of the creator's past scripts to extract their unique vocabulary, pacing, and Hinglish ratio.
- **Key Feature:** It forces the LLM to output a strict JSON format containing a 4-beat structural script (Intro → Context → Value → Call to Action) matching the creator's exact energy.

### 4. Agent 04: The Hook Generator (`hook_generator.py`) 🎣
- **Function:** Psychological Hook Engineering.
- **How it works:** Also powered by the Groq LLM, this agent takes the validated topic and generates exactly 5 distinct Hinglish hooks based on proven psychological frameworks (The Negative Warning, The Result Reveal, The Secret Hack, etc.).
- **Key Feature:** It assigns a "Confidence Score" out of 10 to each hook and recommends the absolute best one for the user.

---

## 🛠️ Step-by-Step: How it was developed from scratch

If you are presenting this, here is the exact development journey:

1. **Ideation & UI Design:** Started by designing a premium, interactive frontend using CSS grid, smooth transitions, and a futuristic aesthetic to ensure an incredible user experience. 
2. **Frontend Logic:** Built `app.js` to handle form validation, sequential progress bar animations (to show the user exactly what the agents are doing), and DOM manipulation to render the complex AI results into clean tables and cards.
3. **Backend Foundation:** Spun up a Python FastAPI server (`main.py`). Defined Pydantic models to strictly type the data passing between the frontend and the AI agents.
4. **Agent Engineering:** 
   - Wrote the Python logic for the Scraper and Validator to handle data manipulation and algorithmic scoring.
   - Integrated the `openai` Python SDK (pointed at Groq's API) to build the Writer and Hook agents. Engineered strict system prompts forcing the LLMs to return pure JSON for seamless frontend rendering.
5. **Connecting the Pieces:** Configured CORS middleware so the local frontend could speak to the backend, ensuring the pipeline flowed perfectly from Agent 1 to 4.
6. **Deployment:** 
   - Initialized Git and pushed the code to GitHub.
   - Deployed the frontend to **Netlify** for global CDN delivery.
   - Deployed the FastAPI backend to **Render**, mapping the environment variables (like the hidden `GROQ_API_KEY`) securely.
   - Linked the Netlify frontend directly to the live Render API URL.

---

*This application demonstrates the power of combining traditional algorithmic data processing (Agents 1 & 2) with advanced generative AI (Agents 3 & 4) to create a fully autonomous, production-ready product.*
