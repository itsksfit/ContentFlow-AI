from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from agents.content_scraper import fetch_real_posts, ScrapedPost
from agents.content_validator import validate, ValidationResult
from agents.voice_writer import write_script, ScriptResult
from agents.hook_generator import generate_hooks, HookResult

app = FastAPI(title="AI Agent Content System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request / Response Models ─────────────────────────────────────────────────
class PipelineRequest(BaseModel):
    niche: str
    topic: str
    platform: str = "all"
    tone: str = "casual"
    voice_sample: str = ""
    audience: str = "General"
    competitors: List[str] = []
    days: int = 7

class PipelineResponse(BaseModel):
    scraped_posts: List[ScrapedPost]
    validation: ValidationResult
    script: ScriptResult
    hooks: HookResult

class ScraperRequest(BaseModel):
    niche: str
    platform: str = "all"
    competitors: List[str] = []
    days: int = 7

class ValidatorRequest(BaseModel):
    niche: str
    platform: str = "all"
    competitors: List[str] = []
    days: int = 7

class ScriptRequest(BaseModel):
    topic: str
    niche: str
    voice_sample: str
    tone: str = "casual"
    validated_topic: str = ""

class HookRequest(BaseModel):
    topic: str
    niche: str
    top_views: List[int] = []

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "message": "ContentFlow AI API is live 🚀"}

@app.post("/api/agent/scraper", response_model=List[ScrapedPost])
def run_scraper(req: ScraperRequest):
    try:
        posts = fetch_real_posts(req.niche, req.platform, req.competitors, req.days)
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/validator", response_model=ValidationResult)
def run_validator(req: ValidatorRequest):
    try:
        posts = fetch_real_posts(req.niche, req.platform, req.competitors, req.days)
        result = validate(posts, req.competitors)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/script", response_model=ScriptResult)
def run_script_writer(req: ScriptRequest):
    try:
        result = write_script(req.topic, req.niche, req.voice_sample, req.tone, req.validated_topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/hooks", response_model=HookResult)
def run_hook_generator(req: HookRequest):
    try:
        result = generate_hooks(req.topic, req.niche, req.top_views)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
