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
    beat4: str
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
    
    # Deterministic Templates (Longer & Mixed Hinglish)
    beat1_templates = [
        "Let's talk about {topic}. Agar aap {niche} space mein grow karna chahte ho, toh you need to hear this right now.",
        "The biggest mistake I see with {topic}? Log basics ko completely ignore kar dete hain. Aur wahi unki growth rokta hai.",
        "I'm going to show you exactly how to handle {topic}. Bina apna time waste kiye, yahan dhyan do."
    ]
    
    beat2_templates = [
        "For a long time, I struggled with this too. Mujhe lagta tha it's too difficult. Then I realized the power of {validated_topic}, aur usne sab badal diya.",
        "Most people just copy-paste the same generic advice. Woh purane methods ab kaam nahi aate. But the real game-changer is {validated_topic}.",
        "If you look at the top creators, they all use {validated_topic} to their advantage. Woh yeh secret aapko nahi batate, par yahi sach hai."
    ]
    
    beat3_templates = [
        "Step 1: Focus on the fundamentals. Apni foundation strong karo. Step 2: Implement this system consistently. Aur uske baad, watch your results multiply overnight.",
        "The secret is simple: stop focusing on vanity metrics. Views aur likes ke peechhe mat bhago. Start building a real foundation. Tabhi aap lambe time tak jeetoge.",
        "It only takes 10 minutes a day. Apne systems ko properly set up karo, aur baaki sab apne aap flow hone lagega. Consistency is everything."
    ]
    
    # Adding an extra beat for more content
    beat4_templates = [
        "Ek aur pro-tip: Don't overcomplicate things. Process ko simple rakho aur execute karo. That's the only way to beat the algorithm.",
        "Yeh method try karke dekho, I promise you won't regret it. Results aana shuru honge toh aap khud hairan rah jaoge.",
        "Remember, {niche} mein success overnight nahi aati. Par agar aap yeh framework use karte ho, aap apne competitors se 10x aage nikal jaoge."
    ]
    
    cta_templates = [
        "Save this video for later, share it with your friends, aur aisi daily {niche} tips ke liye mujhe follow karna mat bhoolna!",
        "Want the full blueprint? Comment 'GUIDE' niche, and I will DM it to you right now. Aur haan, follow zaroor kar lena.",
        "Hit that follow button agar aap iss saal sach mein grow karna chahte ho."
    ]
    
    # Build script (cleaned inputs)
    clean_topic = topic.strip().capitalize()
    clean_niche = niche.strip().capitalize()
    
    b1 = random.choice(beat1_templates).format(topic=clean_topic, niche=clean_niche)
    b2 = random.choice(beat2_templates).format(validated_topic=validated_topic if validated_topic else "this exact strategy")
    b3 = random.choice(beat3_templates)
    b4 = random.choice(beat4_templates).format(niche=clean_niche)
    cta = random.choice(cta_templates).format(niche=clean_niche)
    
    # Inject user's vocabulary naturally if possible
    if analysis.vocabulary_words:
        b1 = b1 + f" And honestly, yeh strictly {analysis.vocabulary_words[0]} hai."
        
    full_script = f"[BEAT 1: HOOK]\n{b1}\n\n[BEAT 2: CONTEXT]\n{b2}\n\n[BEAT 3: VALUE]\n{b3}\n\n[BEAT 4: EXTRA PRO-TIP]\n{b4}\n\n[CALL TO ACTION]\n{cta}"
    word_count = len(full_script.split())
    duration = max(15, round(word_count / 2.5)) # roughly 2.5 words per second
    
    return ScriptResult(
        voice_analysis=analysis,
        beat1=b1,
        beat2=b2,
        beat3=b3,
        beat4=b4,
        cta=cta,
        full_script=full_script,
        word_count=word_count,
        est_duration_sec=f"{duration}s"
    )
