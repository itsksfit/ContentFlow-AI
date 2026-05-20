import random
import re
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

def analyze_voice(sample: str) -> VoiceAnalysis:
    """Deterministically analyze the voice sample."""
    words = re.findall(r'\b\w+\b', sample.lower())
    
    # Simple stop words to filter out common words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "is", "are", "was", "were", "it", "this", "that", "i", "you", "he", "she", "we", "they", "mera", "yeh", "hai", "ka", "ki", "ke", "ho"}
    
    vocab = [w for w in set(words) if w not in stop_words and len(w) > 3]
    
    # Pick top 3 words to highlight
    top_vocab = vocab[:3] if len(vocab) >= 3 else (vocab + ["actually", "literally", "seriously"])[:3]
    
    # Determine sentence length
    sentences = [s.strip() for s in re.split(r'[.!?]', sample) if s.strip()]
    avg_len = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    
    if avg_len < 8:
        length_desc = "Short & Punchy"
    elif avg_len < 15:
        length_desc = "Medium & Flowing"
    else:
        length_desc = "Long & Detailed"
        
    # Check for Hindi/Hinglish indicators (very rudimentary check)
    hinglish_markers = ["bhai", "yaar", "toh", "hai", "kya", "mera", "dekho"]
    hinglish_score = sum(1 for w in words if w in hinglish_markers)
    ratio = "Heavy Hinglish (60/40)" if hinglish_score > 2 else "Mostly English (90/10)"
    
    return VoiceAnalysis(
        vocabulary_words=top_vocab,
        avg_sentence_length=length_desc,
        hinglish_ratio=ratio,
        energy="High Energy & Urgent" if "!" in sample else "Calm & Educational",
        cta_style="Direct Ask",
        structure_pattern="Hook -> Context -> Value -> CTA"
    )

def write_script(
    topic: str,
    niche: str,
    voice_sample: str,
    tone: str,
    validated_topic: str,
) -> ScriptResult:
    analysis = analyze_voice(voice_sample)
    
    # Deterministic Templates
    beat1_templates = [
        "Let's talk about {topic}. If you're in the {niche} space, you need to hear this.",
        "The biggest mistake I see with {topic}? People completely ignore the basics.",
        "I'm going to show you exactly how to handle {topic} without wasting your time."
    ]
    
    beat2_templates = [
        "For a long time, I struggled with this. Then I realized the power of {validated_topic}.",
        "Most people just copy-paste the same generic advice. But the real game-changer is {validated_topic}.",
        "If you look at the top performers, they all use {validated_topic} to their advantage."
    ]
    
    beat3_templates = [
        "Step 1: Focus on the fundamentals. Step 2: Implement this system. Watch your results multiply.",
        "The secret is simple: stop focusing on vanity metrics and start building a real foundation.",
        "It only takes 10 minutes a day. Set up your systems properly and the rest takes care of itself."
    ]
    
    cta_templates = [
        "Save this video for later and follow me for more {niche} tips!",
        "Want the full blueprint? Comment 'GUIDE' below and I will DM it to you right now.",
        "Hit that follow button if you want to master this."
    ]
    
    # Build script (cleaned inputs)
    clean_topic = topic.strip().capitalize()
    clean_niche = niche.strip().capitalize()
    
    b1 = random.choice(beat1_templates).format(topic=clean_topic, niche=clean_niche)
    b2 = random.choice(beat2_templates).format(validated_topic=validated_topic if validated_topic else "this exact strategy")
    b3 = random.choice(beat3_templates)
    cta = random.choice(cta_templates).format(niche=clean_niche)
    
    # Inject user's vocabulary naturally if possible
    if analysis.vocabulary_words:
        b1 = b1 + f" And honestly, it's {analysis.vocabulary_words[0]}."
        
    full_script = f"[BEAT 1: HOOK]\n{b1}\n\n[BEAT 2: CONTEXT]\n{b2}\n\n[BEAT 3: VALUE]\n{b3}\n\n[CALL TO ACTION]\n{cta}"
    word_count = len(full_script.split())
    duration = max(15, round(word_count / 2.5)) # roughly 2.5 words per second
    
    return ScriptResult(
        voice_analysis=analysis,
        beat1=b1,
        beat2=b2,
        beat3=b3,
        cta=cta,
        full_script=full_script,
        word_count=word_count,
        est_duration_sec=f"{duration}s"
    )
