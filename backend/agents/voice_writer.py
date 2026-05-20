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

    # ── Clean inputs ─────────────────────────────────────────────────────────
    import re as regex
    clean_topic = regex.sub(r'\s+', ' ', topic).strip()
    # Capitalise first letter only
    clean_topic = clean_topic[0].upper() + clean_topic[1:] if clean_topic else "this topic"
    clean_niche = regex.sub(r'\s+', ' ', niche).strip()
    clean_niche = clean_niche[0].upper() + clean_niche[1:] if clean_niche else "your niche"

    # Shorten topic if too long so it fits naturally in a sentence
    if len(clean_topic) > 35:
        # Use just the first 4 words for in-sentence use
        short_topic = " ".join(clean_topic.split()[:4])
    else:
        short_topic = clean_topic

    # Use validated_topic as a friendly label (e.g. "Tutorials & How-to")
    # If empty or just the niche name, fall back to a safe phrase
    trend_label = (validated_topic or "").strip()
    if not trend_label or trend_label.lower() == clean_niche.lower():
        trend_label = "this content style"

    tone_key = (tone or "casual").lower()

    # ── Beat 1: HOOK ─────────────────────────────────────────────────────────
    # Rule: topic is introduced in ENGLISH — never jammed into a Hindi verb phrase
    beat1_map = {
        "educational":
            f"Aaj hum baat karenge — \"{short_topic}\". Yeh ek cheez hai jo most {clean_niche} creators completely ignore kar dete hain.",
        "inspirational":
            f"Ek cheez hai jo maine recently discover ki — \"{short_topic}\". Aur isse meri {clean_niche} journey totally change ho gayi.",
        "entertaining":
            f"Maine socha tha \"{short_topic}\" easy hoga. Spoiler alert — bilkul nahi tha. 😭 But jo maine seekha, woh sun lo.",
        "professional":
            f"Today's topic: \"{short_topic}\". Agar aap {clean_niche} mein seriously results chahte ho, yeh framework note kar lo.",
        "controversial":
            f"Hot take incoming — \"{short_topic}\" ke baare mein jo sab kehte hain, woh mostly galat hai. Main data ke saath baat karta hoon.",
        "casual":
            f"Yaar, aaj ek cheez share karni thi — \"{short_topic}\". Agar aap {clean_niche} mein ho, yeh 100% relatable lagega.",
    }

    # ── Beat 2: CONTEXT ───────────────────────────────────────────────────────
    # Rule: trend_label is an English phrase — safe to use as object, not subject of Hindi verb
    beat2_map = {
        "educational":
            f"Data dekha toh pata chala — \"{trend_label}\" is the format that's actually performing right now. Reason? Audience isko relate karta hai.",
        "inspirational":
            f"Main bhi struggle karta tha. Tab maine \"{trend_label}\" try kiya — aur honestly, that changed everything for me.",
        "entertaining":
            f"So I tried \"{trend_label}\" and bhai, main khud shocked tha. Mujhe expect nahi tha ki itna difference padega. 😂",
        "professional":
            f"Current data shows \"{trend_label}\" is dominating the algorithm right now. Aur iska ek clear, logical reason hai.",
        "controversial":
            f"Sach yeh hai — creators jo \"{trend_label}\" use kar rahe hain, woh baaki sabse consistently 3x better perform kar rahe hain.",
        "casual":
            f"Tab mujhe samajh aaya jab maine \"{trend_label}\" seriously lena shuru kiya. Yaar, game changer tha — no joke.",
    }

    # ── Beat 3: VALUE ─────────────────────────────────────────────────────────
    # Rule: no topic/niche injection — pure advice, fully self-contained sentences
    beat3_map = {
        "educational":
            "Theek hai, yeh 3 steps follow karo:\n"
            "Step 1 — Apna niche tight karo. Sab ko please karna band karo.\n"
            "Step 2 — Ek hi format choose karo aur usmein master bano.\n"
            "Step 3 — Consistency is your biggest weapon. Algorithm bhi wahi push karta hai jo regularly post karta hai.",
        "inspirational":
            "Bas ek commitment karo — roz ek piece of content. Perfect nahi, consistent. "
            "Quality apne aap improve hogi. Aur ek din aisa video aayega jo sab kuch badal dega. I genuinely believe that.",
        "entertaining":
            "Maine literally apna phone ek tripod pe rakh ke 10 videos ek din mein shoot ki. "
            "Cringe? Haan, thoda. Worth it? Absolutely. "
            "Kyunki wahi se mujhe pata chala ki mera audience actually kya chahta hai.",
        "professional":
            "Yeh framework use karo — har video ke liye:\n"
            "Hook: 0–3 seconds (attention grab)\n"
            "Problem: 3–15 seconds (why this matters)\n"
            "Solution: 15–45 seconds (the actual value)\n"
            "CTA: last 5 seconds (one clear ask). Simple. Proven. Repeat.",
        "controversial":
            "Log views ke peechhe bhagte hain. Smart creators followers ke peechhe bhagte hain. "
            "Aur actually successful creators community ke peechhe bhagte hain. "
            "Yeh ek line samajh lo — baaki sab apne aap clear ho jayega.",
        "casual":
            "Honestly yaar, koi magic shortcut nahi hai. "
            "Par ek chota sa shift hai jo sab kuch change kar deta hai — apni real life ko content banao. "
            "Log perfection pe nahi, authenticity pe react karte hain. Aur woh aapke paas already hai.",
    }

    # ── Beat 4: PRO-TIP ───────────────────────────────────────────────────────
    beat4_map = {
        "educational":
            f"Pro tip: Apne top 3 performing posts dekho. Jo format wahan repeat ho raha hai — wahi aapka hero format hai. "
            f"Usi ko dobara banao, thoda tweak karo, aur scale karo. Yahi formula works in {clean_niche}.",
        "inspirational":
            "Ek last baat — comparison sabse bada creativity killer hai. "
            "Doosron ko mat dekho. Apne aaj ko apne kal se compare karo. That's real progress.",
        "entertaining":
            "Aur haan — agar yeh video helpful laga, apne ek dost ko tag karo jisne abhi tak start nahi kiya. "
            "Unka time aa gaya hai. 😂",
        "professional":
            "Bonus metric: Har video ke baad sirf 3 numbers track karo — Watch Time %, Shares, aur Comments. "
            "Likes vanity metric hai. Baaki teen real signal hain jo algorithm ko bhi matter karte hain.",
        "controversial":
            "Agar aap agree nahi karte — perfect. Comment mein aao, debate karte hain. "
            "Mujhe echo chamber nahi chahiye, mujhe real conversation chahiye.",
        "casual":
            f"Last thought — {clean_niche} mein jo log jeet rahe hain woh perfect nahi hain, woh real hain. "
            "So bas show up karo. Roz. Wahi kaafi hai.",
    }

    # ── CTA ───────────────────────────────────────────────────────────────────
    cta_map = {
        "educational":
            f"Agar yeh helpful laga, video save kar lo — future mein kaam aayega. "
            f"Aur agar aap {clean_niche} content regularly chahte ho, toh follow zaroor karo.",
        "inspirational":
            "Comment mein 'START' likho agar aap aaj se seriously lena chahte ho. Main personally reply karoonga — promise.",
        "entertaining":
            f"Follow karo for more {clean_niche} chaos and real talk. Aur agar relate kiya toh share karo — "
            "shayad kisi aur ko bhi chahiye yeh. 😄",
        "professional":
            f"For more structured {clean_niche} breakdowns, follow karo. "
            "Aur comment mein batao — kaunsa step aapke liye sabse helpful tha?",
        "controversial":
            "Agree ho toh share karo. Disagree ho toh comment mein aao. Dono welcome hain.",
        "casual":
            f"Yaar, acha laga toh follow karo — main roz aise hi real {clean_niche} content dalta hoon. "
            "Aur apne dosto ko tag karo!",
    }

    b1  = beat1_map.get(tone_key, beat1_map["casual"])
    b2  = beat2_map.get(tone_key, beat2_map["casual"])
    b3  = beat3_map.get(tone_key, beat3_map["casual"])
    b4  = beat4_map.get(tone_key, beat4_map["casual"])
    cta = cta_map.get(tone_key,   cta_map["casual"])

    full_script = (
        f"[BEAT 1: HOOK]\n{b1}\n\n"
        f"[BEAT 2: CONTEXT]\n{b2}\n\n"
        f"[BEAT 3: VALUE]\n{b3}\n\n"
        f"[BEAT 4: PRO-TIP]\n{b4}\n\n"
        f"[CALL TO ACTION]\n{cta}"
    )
    word_count = len(full_script.split())
    duration   = max(15, round(word_count / 2.5))

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
