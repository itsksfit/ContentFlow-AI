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
        "If you are still struggling with {topic} in {niche}, you need to stop and watch this.",
        "Here is the brutal truth about {topic} that nobody in {niche} is telling you.",
        "Everyone says {topic} is hard. But using this {niche} trick, I completely changed the game."
    ]
    
    beat2_templates = [
        "For months, I was doing it the old way. Then I discovered {validated_topic}, and it literally shifted my perspective.",
        "Most people just copy-paste the same generic advice. But the real magic happens when you apply {validated_topic}.",
        "I analyzed the top creators, and they all have one thing in common: {validated_topic}."
    ]
    
    beat3_templates = [
        "Step 1: Change your mindset. Step 2: Implement this framework. And boom, your {niche} workflow is instantly better.",
        "The secret is simple: stop focusing on vanity metrics and start building a real foundation. That is how you win.",
        "It only takes 10 minutes a day. Just set up your systems, let the data flow, and watch the results multiply."
    ]
    
    cta_templates = [
        "Save this video for later and follow me for more daily {niche} tips!",
        "Want my full blueprint? Comment 'GUIDE' below and I will DM it to you right now.",
        "Hit that follow button if you want to master {niche} this year."
    ]
    
    # Build script
    b1 = random.choice(beat1_templates).format(topic=topic, niche=niche)
    b2 = random.choice(beat2_templates).format(validated_topic=validated_topic if validated_topic else "this secret strategy")
    b3 = random.choice(beat3_templates).format(niche=niche)
    cta = random.choice(cta_templates).format(niche=niche)
    
    # Inject user's vocabulary if possible
    if analysis.vocabulary_words:
        b1 = b1 + f" It's {analysis.vocabulary_words[0]}."
        
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
