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
    
    # Clean inputs
    import re as regex
    clean_topic = regex.sub(r'\s+', ' ', topic).strip().capitalize()
    clean_niche = regex.sub(r'\s+', ' ', niche).strip().capitalize()
    if len(clean_topic) > 40:
        clean_topic = clean_topic[:37] + "..."

    # Tone-aware templates
    tone_key = (tone or "casual").lower()

    beat1_map = {
        "educational":   "Ek cheez hai jo most {niche} creators completely miss kar dete hain about {topic}. Aaj main woh bata raha hoon.",
        "inspirational": "Yaar, {topic} ne meri life badal di. Aur agar aap bhi {niche} mein seriously aana chahte ho, toh yeh sun lo.",
        "entertaining":  "Okay so maine socha tha {topic} easy hoga. Spoiler alert — nahi tha. Par jo maine seekha, woh 🔥",
        "professional":  "Let's break down {topic} properly. Agar aap {niche} mein results chahte ho, yeh framework follow karo.",
        "controversial": "Hot take: {topic} ke baare mein jo sab bol rahe hain woh galat hai. Main proof ke saath baat karta hoon.",
        "casual":        "Bhai sun, {topic} ke baare mein kuch baat karni thi. Agar aap {niche} mein ho, yeh relatable lagega.",
    }
    beat2_map = {
        "educational":   "Data yeh kehta hai: {validated_topic} woh format hai jo is waqt sabse zyada perform kar raha hai. Reason simple hai.",
        "inspirational": "Maine bhi ek time pe struggle kiya. Phir {validated_topic} ne sab kuch badal diya — seriously.",
        "entertaining":  "Toh maine try kiya {validated_topic}. Results? Bhai, main khud hairan tha. 😭",
        "professional":  "Research shows {validated_topic} is dominating right now. Aur iska ek clear reason hai.",
        "controversial": "Sach yeh hai: {validated_topic} use karne wale creators baaki sabse 3x aage hain. Kyun? Sun.",
        "casual":        "Mujhe khud tab pata chala jab maine {validated_topic} seriously lena shuru kiya. Game changer tha yaar.",
    }
    beat3_map = {
        "educational":   "Step 1 — Apna niche tight karo, sab ko please karna band karo. Step 2 — Ek format choose karo aur usmein master bano. Step 3 — Consistency hi aapki moat hai.",
        "inspirational": "Bas ek kaam karo — roz ek video. Quality improve hoti rahegi. Aur ek din woh video aayegi jo sab kuch badal degi. I promise.",
        "entertaining":  "Maine kya kiya? Maine literally apne phone ko tripod pe rakh ke 10 videos ek din mein shoot ki. Cringe? Haan. Worth it? Bilkul.",
        "professional":  "Framework simple hai: Hook (3 sec) → Problem (10 sec) → Solution (30 sec) → CTA (5 sec). Yahi formula top creators use karte hain.",
        "controversial": "Log views ke peechhe bhagte hain. Smart creators followers ke peechhe bhagte hain. Aur legendary creators community ke peechhe bhagte hain. Farak samajh lo.",
        "casual":        "Honestly yaar, koi shortcut nahi hai. Par ek trick hai — apni life ko content banao. Log authenticity pe react karte hain, perfection pe nahi.",
    }
    beat4_map = {
        "educational":   "Pro tip: Apne top 3 posts ko dekho — woh format jo wahan hai, wahi aapka hero format hai. Wahi dobara banao, tweak karo, scale karo.",
        "inspirational": "Ek baat yaad rakho — comparison sabse bada killer hai. Apna journey track karo, doosron ka nahi.",
        "entertaining":  "Aur haan, agar yeh video aapko useful laga toh share karna mat bhoolna. Apne dost ko tag karo jisne abhi tak start nahi kiya. 😂",
        "professional":  "Bonus: Har video ke baad 3 metrics track karo — Watch Time, Shares, aur Comments. Likes vanity metric hai. Baaki teen real signal hain.",
        "controversial": "Agar aap agree nahi karte, comment mein batao. Mujhe genuine debate se koi darr nahi hai.",
        "casual":        "Ek last cheez — {niche} mein woh log jeet rahe hain jo real hain, perfect nahi. So just show up, yaar.",
    }
    cta_map = {
        "educational":   "Agar yeh helpful laga, save kar lo — aapko baar baar chahiye hoga. Aur follow karo for more {niche} tips.",
        "inspirational": "Comment mein 'START' likho agar aap aaj se seriously lena chahte ho. Main personally reply karoonga.",
        "entertaining":  "Follow karo for more {niche} chaos. Aur agar relate kiya, share zaroor karo! 😄",
        "professional":  "For more structured {niche} content, follow karo. Aur comment mein batao — kaunsa step sabse helpful laga?",
        "controversial": "Disagree ho toh comment mein batao. Agree ho toh share karo taaki yeh baat aur logo tak pahunche.",
        "casual":        "Yaar acha laga toh follow karo — main roz aisa content dalta rehta hoon. Aur apne dosto ko tag karo!",
    }

    b1 = beat1_map.get(tone_key, beat1_map["casual"]).format(topic=clean_topic, niche=clean_niche)
    b2 = beat2_map.get(tone_key, beat2_map["casual"]).format(validated_topic=validated_topic if validated_topic else "this approach")
    b3 = beat3_map.get(tone_key, beat3_map["casual"])
    b4 = beat4_map.get(tone_key, beat4_map["casual"]).format(niche=clean_niche)
    cta = cta_map.get(tone_key, cta_map["casual"]).format(niche=clean_niche)

    
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
