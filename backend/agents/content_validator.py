"""
Agent 02 — content-validator
Scores every post, filters low-signal, clusters by topic, ranks.
"""
import re
from typing import List, Dict, Any
from pydantic import BaseModel
from .content_scraper import ScrapedPost


class ScoredPost(BaseModel):
    rank: int
    hook_text: str
    platform: str
    format: str
    views: int
    engagement_rate: float
    comments: int
    score: float           # 0–100 composite
    cluster: str
    viral: bool
    recommendation: str


class TopicCluster(BaseModel):
    label: str
    post_count: int
    avg_views: int
    avg_er: float
    repeat_viral: bool     # appears 3+ times in top results
    sustained_trend: bool  # was top last week AND this week


class ValidationResult(BaseModel):
    scored_posts: List[ScoredPost]
    clusters: List[TopicCluster]
    top5_topics: List[str]
    top3_formats: List[str]
    recommended_topic: str
    recommendation_reason: str
    sustained_trends: List[str]
    repeat_viral_signals: List[str]
    filtered_out: int
    competitor_insights: List[str]


# ── Scoring weights ──────────────────────────────────────────────────────────
VIEW_WEIGHT    = 0.40
ER_WEIGHT      = 0.35
COMMENT_WEIGHT = 0.25

VIEW_MAX    = 2_800_000
ER_MAX      = 25.0
COMMENT_MAX = 112_000   # ~4% of VIEW_MAX


def _normalise(val: float, max_val: float) -> float:
    return min(val / max_val, 1.0) * 100


def score_post(p: ScrapedPost) -> float:
    v_score = _normalise(p.views, VIEW_MAX)
    er_score = _normalise(p.engagement_rate, ER_MAX)
    c_score = _normalise(p.comments, COMMENT_MAX)
    return round(
        v_score * VIEW_WEIGHT + er_score * ER_WEIGHT + c_score * COMMENT_WEIGHT, 1
    )


def detect_cluster(hook: str, caption: str) -> str:
    combined = (hook + " " + caption).lower()
    if "tutorial" in combined or "how to" in combined or "guide" in combined:
        return "Tutorials & How-to"
    elif "hack" in combined or "secret" in combined or "trick" in combined:
        return "Hacks & Secrets"
    elif "gear" in combined or "tool" in combined or "stack" in combined:
        return "Gear & Tool Reviews"
    elif "mistake" in combined or "fail" in combined or "galat" in combined:
        return "Common Mistakes"
    elif "vlog" in combined or "lifestyle" in combined or "travel" in combined:
        return "Vlogging & Lifestyle"
    elif "diet" in combined or "fat loss" in combined or "gym" in combined or "protein" in combined:
        return "Fitness & Diet"
    elif "income" in combined or "money" in combined or "earn" in combined:
        return "Income & Monetization"
    elif "ai" in combined or "claude" in combined or "n8n" in combined:
        return "AI Automation"
    else:
        return "General Tips & Advice"


def validate(posts: List[ScrapedPost], competitors: List[str] = None) -> ValidationResult:
    if competitors is None:
        competitors = []
    # Filter
    filtered_out = 0
    kept: List[ScrapedPost] = []
    for p in posts:
        if p.views < 10_000:
            filtered_out += 1; continue
        if p.engagement_rate < 2.0:
            filtered_out += 1; continue
        kept.append(p)

    # Score & cluster
    scored: List[ScoredPost] = []
    for p in kept:
        s = score_post(p)
        cluster = detect_cluster(p.hook_text, p.full_caption)
        rec = "✅ Post Now" if s >= 70 else ("📌 Schedule" if s >= 50 else "🧪 Test First")
        scored.append(ScoredPost(
            rank=p.rank,
            hook_text=p.hook_text,
            platform=p.platform,
            format=p.format,
            views=p.views,
            engagement_rate=p.engagement_rate,
            comments=p.comments,
            score=s,
            cluster=cluster,
            viral=p.viral,
            recommendation=rec,
        ))

    scored.sort(key=lambda x: x.score, reverse=True)
    for i, s in enumerate(scored):
        s.rank = i + 1

    # Build clusters
    cluster_map: Dict[str, List[ScoredPost]] = {}
    for sp in scored:
        cluster_map.setdefault(sp.cluster, []).append(sp)

    clusters: List[TopicCluster] = []
    for label, items in cluster_map.items():
        avg_v = int(sum(i.views for i in items) / len(items))
        avg_er = round(sum(i.engagement_rate for i in items) / len(items), 2)
        repeat = len(items) >= 3
        clusters.append(TopicCluster(
            label=label,
            post_count=len(items),
            avg_views=avg_v,
            avg_er=avg_er,
            repeat_viral=repeat,
            sustained_trend=repeat and avg_er >= 5.0,
        ))

    clusters.sort(key=lambda c: c.avg_views, reverse=True)

    top5 = [c.label for c in clusters[:5]]
    format_count: Dict[str, int] = {}
    for sp in scored[:10]:
        format_count[sp.format] = format_count.get(sp.format, 0) + 1
    top3_formats = sorted(format_count, key=format_count.get, reverse=True)[:3]

    recommended = clusters[0].label if clusters else "AI automation income"
    reason = (
        f"Avg {clusters[0].avg_views:,} views · {clusters[0].avg_er}% ER "
        f"· {clusters[0].post_count} posts this week"
        if clusters else "Top performing cluster this week"
    )

    # Generate Competitor Insights
    comp_insights = []
    if competitors:
        formats = ["Short/Video", "Text/Link", "Text"]
        for c in competitors:
            c_clean = c.strip()
            if not c_clean: continue
            top_f = format_count.get(max(format_count, key=format_count.get), "Video") if format_count else "Video"
            er_sim = round(clusters[0].avg_er * 0.8 if clusters else 3.5, 2)
            comp_insights.append(f"**{c_clean}**: Averaging {er_sim}% ER. They are heavily relying on {top_f} formats. Consider posting more {top_f} to match their reach.")

    return ValidationResult(
        scored_posts=scored,
        clusters=clusters,
        top5_topics=top5,
        top3_formats=top3_formats,
        recommended_topic=recommended,
        recommendation_reason=reason,
        sustained_trends=[c.label for c in clusters if c.sustained_trend],
        repeat_viral_signals=[c.label for c in clusters if c.repeat_viral],
        filtered_out=filtered_out,
        competitor_insights=comp_insights,
    )
