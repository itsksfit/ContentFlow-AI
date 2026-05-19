"""
Agent 01 — content-scraper
Simulates scraping Instagram Reels, YouTube Shorts, Twitter/X.
In production: swap generate_mock_posts() for real API calls
(Apify, RapidAPI social scrapers, YouTube Data API, etc.)
"""
import random
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel


class ScrapedPost(BaseModel):
    rank: int
    platform: str
    format: str
    hook_text: str
    full_caption: str
    views: int
    likes: int
    comments: int
    engagement_rate: float
    post_date: str
    content_url: str
    viral: bool
    transcript_snippet: str


KEYWORDS = [
    "Claude Code", "AI agents", "N8N automation", "AI coding",
    "vibe coding", "Claude skills", "AI automation", "OpenAI",
]

PLATFORMS = {
    "instagram": {"formats": ["Reel", "Carousel", "Story"]},
    "youtube":   {"formats": ["Short", "Tutorial", "Vlog"]},
    "twitter":   {"formats": ["Thread", "Video", "Poll"]},
}

HOOKS_POOL = [
    "Yeh dekh ke {kw} mein sab kuch badal gaya mera",
    "Maine {kw} try kiya aur result dekho 👀",
    "{kw} se 10x fast ho gaya mera workflow",
    "Yeh {kw} hack 99% log nahi jaante",
    "Agar tum {kw} use nahi kar rahe to paise waste kar rahe ho",
    "Real talk: {kw} ne meri life seriously change kar di",
    "{kw} ka yeh wala feature literally mind blowing hai",
    "Log {kw} ke baare mein galat soch rahe hain — sun",
    "Mujhe {kw} discover karne mein 6 mahine lag gaye — tumhe 60 sec",
    "Bhai {kw} without {kw2} is incomplete, aaj explain karta hoon",
]

CAPTIONS_POOL = [
    "Full breakdown in bio link. {kw} ka yeh feature aur koi nahi batata. Comment karo 'GUIDE' main bhej dunga.",
    "Yaar seriously {kw} ek baar try karo. 3 din mein hi results aane lagte hain. Follow karo aur notification on raho.",
    "{kw} automation setup ka full tutorial bana raha hoon. Save karo yeh post. Part 2 kal aayega.",
    "Mera entire {kw} stack yahan hai. DM karo 'STACK' main list bhej dunga.",
    "{kw} + N8N = 🔥 yeh combination try karo. Seriously next level productivity.",
]

TRANSCRIPTS = [
    "Okay toh aaj main tumhe {kw} ka ek aise feature ke baare mein bataunga jo literally...",
    "Bhai sun, {kw} ke saath mera experience kuch aisa raha hai...",
    "Yeh reel specifically {kw} users ke liye hai jo abhi start kar rahe hain...",
    "Agar tum AI tools use kar rahe ho aur {kw} miss kar rahe ho toh...",
]


def _rand_date(days_back_max: int = 7) -> str:
    d = datetime.now() - timedelta(days=random.randint(0, days_back_max))
    return d.strftime("%Y-%m-%d")


def generate_mock_posts(
    niche: str,
    platform: str,
    competitors: List[str],
    days: int = 7,
) -> List[ScrapedPost]:
    """Generate realistic mock posts. Replace with real API calls in production."""
    posts = []
    plat_keys = (
        list(PLATFORMS.keys()) if platform == "all" else [platform]
    )

    lower_niche = niche.lower()
    if any(k in lower_niche for k in ["ai", "claude", "code", "n8n"]):
        kw_pool = KEYWORDS + [niche] if niche not in KEYWORDS else KEYWORDS
    else:
        kw_pool = [
            niche,
            f"{niche} tips",
            f"best {niche} gear",
            f"how to start {niche}",
            f"{niche} hacks",
            f"{niche} secrets",
            f"{niche} mistakes",
        ]

    count = 0
    for _ in range(22):
        kw = random.choice(kw_pool)
        kw2 = random.choice([k for k in kw_pool if k != kw])
        plat = random.choice(plat_keys)
        fmt = random.choice(PLATFORMS[plat]["formats"])

        views = random.randint(8_000, 2_800_000)
        likes = int(views * random.uniform(0.03, 0.18))
        comments = int(views * random.uniform(0.005, 0.04))
        er = round((likes + comments) / views * 100, 2)
        viral = er >= 5.0 or views >= 100_000

        count += 1
        posts.append(ScrapedPost(
            rank=count,
            platform=plat.capitalize(),
            format=fmt,
            hook_text=random.choice(HOOKS_POOL).format(kw=kw, kw2=kw2),
            full_caption=random.choice(CAPTIONS_POOL).format(kw=kw),
            views=views,
            likes=likes,
            comments=comments,
            engagement_rate=er,
            post_date=_rand_date(days),
            content_url=f"https://example.com/{plat}/p/{random.randint(100000,999999)}",
            viral=viral,
            transcript_snippet=random.choice(TRANSCRIPTS).format(kw=kw),
        ))

    # Sort by views descending
    posts.sort(key=lambda p: p.views, reverse=True)
    for i, p in enumerate(posts):
        p.rank = i + 1

    return posts
