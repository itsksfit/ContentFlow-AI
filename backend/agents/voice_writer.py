import os
import json
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

class VoiceAnalysis(BaseModel):
    vocabulary_words: List[str]
    avg_sentence_length: str
    hinglish_ratio: str
    energy: str
    cta_style: str
    structure_pattern: str

class ScriptResult(BaseModel):
    voice_analysis: VoiceAnalysis
    beat1: str
    beat2: str
    beat3: str
    cta: str
    full_script: str
    word_count: int
    est_duration_sec: str

def write_script(
    topic: str,
    niche: str,
    voice_sample: str,
    tone: str,
    validated_topic: str,
) -> ScriptResult:
    prompt = f"""
    You are an expert content script writer. Analyze the following voice sample to extract the user's tone, vocabulary, and Hinglish ratio.
    Then, write a new 4-part short-form video script about '{topic}' (Niche: {niche}, Tone: {tone}).
    The script must strictly have 4 parts: BEAT 1 (Intro/Problem), BEAT 2 (Context/Build-up), BEAT 3 (Solution/Value), and CTA.
    
    Voice Sample:
    "{voice_sample}"
    
    Respond ONLY in valid JSON matching this exact structure:
    {{
        "voice_analysis": {{
            "vocabulary_words": ["word1", "word2", "word3"],
            "avg_sentence_length": "Short/Medium/Long",
            "hinglish_ratio": "Percentage of Hindi vs English",
            "energy": "Description of energy",
            "cta_style": "Description of CTA style",
            "structure_pattern": "BEAT 1 -> BEAT 2 -> BEAT 3 -> CTA"
        }},
        "beat1": "...",
        "beat2": "...",
        "beat3": "...",
        "cta": "...",
        "full_script": "Full combined script text",
        "word_count": 0,
        "est_duration_sec": "time in seconds"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        data = json.loads(response.choices[0].message.content)
        return ScriptResult(**data)
    except Exception as e:
        # Fallback in case of Groq error
        return ScriptResult(
            voice_analysis=VoiceAnalysis(vocabulary_words=["error"], avg_sentence_length="error", hinglish_ratio="error", energy="error", cta_style="error", structure_pattern="error"),
            beat1="Error fetching from Groq API", beat2=str(e), beat3="", cta="", full_script=f"Error: {str(e)}", word_count=0, est_duration_sec="0s"
        )
