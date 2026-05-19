"""
Agent 03 — my-voice-writer
Analyses user's past scripts and writes a new reel script
in their exact tone: Hinglish, punchy, BEAT structure, comment CTA.
"""
import re
from collections import Counter
from typing import List
from pydantic import BaseModel

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
    # 1. Very basic fake voice analysis
    words = re.findall(r'\b\w+\b', voice_sample.lower())
    common = [w[0] for w in Counter(words).most_common(10) if len(w[0]) > 3][:3]
    if not common:
        common = ["bhai", "samjho", "literally"]

    # 2. Mock generation based on tone and niche
    b1 = f"Agar tum {niche} mein grow karna chahte ho, aur tumhara topic '{topic}' hai, toh yeh galti mat karna."
    b2 = f"Maine dekha hai log {topic} par bohot time waste karte hain. Reality mein tumhe sirf ek system chahiye."
    b3 = f"Jab se maine yeh implement kiya, mera output 3x fast ho gaya aur stress zero."
    
    if tone == "casual":
        cta = f"Mera exact framework chahiye? '{topic[:5].upper()}' comment karo, main DM kar dunga."
    elif tone == "educational":
        cta = f"Full guide ke liye mujhe follow karo aur link in bio check karo."
    else:
        cta = f"Save this reel aur mujhe DM karo 'GROW' for details."

    full = f"[BEAT 1]\n{b1}\n\n[BEAT 2]\n{b2}\n\n[BEAT 3]\n{b3}\n\n[CTA]\n{cta}"
    
    wc = len(full.split())
    dur = f"{max(25, wc * 60 // 130)}–{max(35, wc * 60 // 100)} sec"

    return ScriptResult(
        voice_analysis=VoiceAnalysis(
            vocabulary_words=common,
            avg_sentence_length="Short & Punchy",
            hinglish_ratio="65% Hindi / 35% English",
            energy=tone.capitalize(),
            cta_style="High-converting DM trigger",
            structure_pattern="BEAT 1 -> BEAT 2 -> BEAT 3 -> CTA"
        ),
        beat1=b1,
        beat2=b2,
        beat3=b3,
        cta=cta,
        full_script=full,
        word_count=wc,
        est_duration_sec=dur
    )
