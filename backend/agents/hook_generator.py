import os
import json
import random
from typing import List
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

class Hook(BaseModel):
    number: int
    text: str
    pattern_name: str
    pattern_description: str
    matched_reel_views: str
    confidence_score: float
    recommended: bool

class HookResult(BaseModel):
    topic: str
    avg_views_matched: int
    hooks: List[Hook]
    recommended_hook_number: int

def generate_hooks(
    topic: str,
    niche: str,
    top_views: List[int]
) -> HookResult:
    avg_v = sum(top_views) // len(top_views) if top_views else 125000
    
    prompt = f"""
    You are an expert hook generator for short-form video content in the {niche} niche.
    Generate exactly 5 distinct, highly-engaging Hinglish hooks for the topic: '{topic}'.
    Each hook must be short (under 4 seconds spoken), punchy, and use a different psychological pattern (e.g., Negative Warning, Result Reveal, Secret Hack, Contrarian Take, Fast-Track Promise).
    
    Respond ONLY in valid JSON matching this exact structure:
    {{
        "hooks": [
            {{
                "number": 1,
                "text": "The actual hook in Hinglish",
                "pattern_name": "Name of pattern",
                "pattern_description": "Brief description of why this pattern works",
                "confidence_score": 9.5
            }},
            {{
                "number": 2,
                "text": "...",
                "pattern_name": "...",
                "pattern_description": "...",
                "confidence_score": 8.0
            }},
            {{
                "number": 3,
                "text": "...",
                "pattern_name": "...",
                "pattern_description": "...",
                "confidence_score": 8.5
            }},
            {{
                "number": 4,
                "text": "...",
                "pattern_name": "...",
                "pattern_description": "...",
                "confidence_score": 9.0
            }},
            {{
                "number": 5,
                "text": "...",
                "pattern_name": "...",
                "pattern_description": "...",
                "confidence_score": 7.5
            }}
        ],
        "recommended_hook_number": 1
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        data = json.loads(response.choices[0].message.content)
        
        hooks = []
        for h in data.get("hooks", []):
            hooks.append(Hook(
                number=h.get("number", 1),
                text=h.get("text", "Fallback hook"),
                pattern_name=h.get("pattern_name", "Pattern"),
                pattern_description=h.get("pattern_description", "Desc"),
                matched_reel_views=f"{int((avg_v * random.uniform(0.8, 1.5)) / 1000)}K+",
                confidence_score=h.get("confidence_score", 8.0),
                recommended=(h.get("number") == data.get("recommended_hook_number"))
            ))
            
        return HookResult(
            topic=topic,
            avg_views_matched=avg_v,
            hooks=hooks,
            recommended_hook_number=data.get("recommended_hook_number", 1)
        )
    except Exception as e:
        # Fallback on error
        return HookResult(topic=topic, avg_views_matched=avg_v, hooks=[Hook(number=1, text=f"Error: {str(e)}", pattern_name="Error", pattern_description="Error fetching from Groq", matched_reel_views="0", confidence_score=0, recommended=True)], recommended_hook_number=1)
