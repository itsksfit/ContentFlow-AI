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
    
    # Deterministic Templates (Flexible for any Niche/Vlog/Tips)
    beat1_templates = [
        "Let's talk about {topic}. Agar aap {niche} space mein ho, toh yeh aapke liye hai.",
        "Sabse badi galti jo log {topic} mein karte hain? Woh basics ko ignore kar dete hain. Dhyan se suno.",
        "Aaj main baat karne wala hoon about {topic}. Bina apna time waste kiye, sidhe point par aate hain."
    ]
    
    beat2_templates = [
        "Pehle mujhe bhi lagta tha it's too difficult. Then I realized the power of {validated_topic}, aur usne sab badal diya.",
        "Most people just copy-paste the same old stuff. Woh purane methods ab kaam nahi aate. But the real game-changer is {validated_topic}.",
        "If you look at the top creators, they all use {validated_topic} to their advantage. Yahi sach hai."
    ]
    
    beat3_templates = [
        "Step 1: Focus on the fundamentals. Step 2: Implement this consistently. Aur uske baad, you will see the difference.",
        "The secret is simple: stop focusing on vanity metrics. Apna unique style develop karo. Tabhi aap lambe time tak jeetoge.",
        "It only takes a little bit of consistency. Apne process ko set up karo, aur baaki sab apne aap flow hone lagega."
    ]
    
    # Adding an extra beat for more content
    beat4_templates = [
        "Ek aur pro-tip: Don't overcomplicate things. Process ko simple rakho aur execute karo. That's how you stand out.",
        "Yeh mind-set try karke dekho, I promise you won't regret it. Results aana shuru honge toh aap khud hairan rah jaoge.",
        "Remember, {niche} mein success overnight nahi aati. Par agar aap apna 100% dete ho, nobody can stop you."
    ]
    
    cta_templates = [
        "Save this video for later, share it with your friends, aur aisi daily {niche} content ke liye mujhe follow karna mat bhoolna!",
        "Kaisa laga yeh video? Comment karke batao. Aur haan, follow zaroor kar lena.",
        "Hit that follow button agar aapko iss type ka content pasand hai."
    ]
    
    # Build script (cleaned inputs)
    # Remove newlines and extra spaces
    import re as regex
    clean_topic = regex.sub(r'\s+', ' ', topic).strip().capitalize()
    clean_niche = regex.sub(r'\s+', ' ', niche).strip().capitalize()
    
    # Limit length so it doesn't sound awkward if they pasted a whole paragraph
    if len(clean_topic) > 40:
        clean_topic = clean_topic[:37] + "..."
        
    b1 = random.choice(beat1_templates).format(topic=clean_topic, niche=clean_niche)
    b2 = random.choice(beat2_templates).format(validated_topic=validated_topic if validated_topic else "this exact strategy")
    b3 = random.choice(beat3_templates)
    b4 = random.choice(beat4_templates).format(niche=clean_niche)
    cta = random.choice(cta_templates).format(niche=clean_niche)
    
    # Inject user's vocabulary naturally if possible
    if analysis.vocabulary_words:
        vocab_word = analysis.vocabulary_words[0].capitalize()
        b1 = b1 + f" Aur main hamesha yahi kehta hoon: '{vocab_word}' is everything."
        
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
