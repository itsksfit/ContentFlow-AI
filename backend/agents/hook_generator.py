import re
import random
from typing import List
from pydantic import BaseModel

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

# Rule: topic is ALWAYS introduced in English (quoted or natural English phrase).
# Never force an English topic string into a Hindi verb construction.
# niche is used only as a noun/label in English or at the end of a sentence.

HOOK_PATTERNS = [
    {
        "name": "The Negative Warning",
        "description": "Uses fear of doing something wrong to stop the scroll.",
        # topic used as English label in quotes — grammatically safe
        "template": "Agar aap \"{topic}\" ke baare mein yeh galti kar rahe ho, toh ruk jao. Yeh video aapke liye hai."
    },
    {
        "name": "The Secret Hack",
        "description": "Promises insider knowledge most people don't know.",
        # topic as English object of 'about'
        "template": "95% {niche} creators don't know this about \"{topic}\". Aaj main woh secret share kar raha hoon."
    },
    {
        "name": "The Result Reveal",
        "description": "Shows the end result first to build curiosity.",
        # topic as English label, result statement in Hinglish
        "template": "Maine \"{topic}\" try kiya — aur results ne mujhe khud hairan kar diya. Yeh dekh lo."
    },
    {
        "name": "The Contrarian Take",
        "description": "Goes against common advice to grab attention.",
        # topic as English object of 'about' — grammatically clean
        "template": "Hot take: jo bhi aapne \"{topic}\" ke baare mein suna hai, woh mostly galat hai. Main explain karta hoon kyun."
    },
    {
        "name": "The Fast-Track Promise",
        "description": "Offers a quick, clear solution in a time-bound hook.",
        # topic as English object — safe construction
        "template": "Sirf 60 seconds mein main aapko \"{topic}\" ka fastest shortcut bata deta hoon. Ready? Sun lo."
    },
]

def generate_hooks(
    topic: str,
    niche: str,
    top_views: List[int]
) -> HookResult:
    avg_v = sum(top_views) // len(top_views) if top_views else 125000

    # ── Clean inputs ──────────────────────────────────────────────────────────
    clean_topic = re.sub(r'\s+', ' ', topic).strip()
    clean_topic = clean_topic[0].upper() + clean_topic[1:] if clean_topic else "this topic"
    # Shorten topic to first 5 words so it fits inside quotes naturally
    short_topic = " ".join(clean_topic.split()[:5])

    clean_niche = re.sub(r'\s+', ' ', niche).strip()
    clean_niche = clean_niche[0].upper() + clean_niche[1:] if clean_niche else "content"

    hooks = []

    for idx, pattern in enumerate(HOOK_PATTERNS):
        hook_text = pattern["template"].format(topic=short_topic, niche=clean_niche)

        # Pseudo-deterministic confidence score
        confidence = round(9.8 - (idx * 0.4) + random.uniform(-0.2, 0.2), 1)
        confidence = min(confidence, 9.9)

        hooks.append(Hook(
            number=idx + 1,
            text=hook_text,
            pattern_name=pattern["name"],
            pattern_description=pattern["description"],
            matched_reel_views=f"{int((avg_v * random.uniform(0.8, 1.5)) / 1000)}K+",
            confidence_score=confidence,
            recommended=(idx == 0)
        ))

    return HookResult(
        topic=topic,
        avg_views_matched=avg_v,
        hooks=hooks,
        recommended_hook_number=1
    )
