import random
from dataclasses import dataclass
from typing import List, Dict

import numpy as np

TOPICS = [
    "books and learning",
    "online shopping",
    "health and wellness",
    "travel deals",
    "personal finance app",
    "fitness coaching",
    "food and beverage",
    "local business",
]

CTA = [
    "Try it today",
    "Sign up now",
    "Learn more",
    "Shop now",
    "Get started",
    "See details",
]

STYLE = [
    "short and direct",
    "storytelling",
    "question",
    "advice",
]


def _build_text(topic: str, style: str, cta: str, seed: int) -> str:
    rnd = random.Random(seed)
    openers = {
        "short and direct": [
            f"Make {topic} easier today.",
            f"The fast way to handle {topic}.",
        ],
        "storytelling": [
            f"Last week I needed help with {topic}, and found a better way.",
            f"When you are short on time for {topic}, this helps.",
        ],
        "question": [
            f"Want to do better at {topic}?",
            f"How can you get faster results in {topic}?",
        ],
        "advice": [
            f"These tips work for {topic}.",
            f"A few simple steps to improve {topic}.",
        ],
    }
    benefits = [
        "Save time",
        "Cut costs",
        "See results faster",
        "Improve quality",
    ]
    opener = rnd.choice(openers.get(style, openers["short and direct"]))
    benefit = rnd.choice(benefits)
    return f"{opener} {benefit}. {cta}."


def _score_text(text: str) -> float:
    length = len(text)
    has_cta = any(phrase in text for phrase in CTA)
    score = 0.008
    if has_cta:
        score += 0.006
    if 60 <= length <= 110:
        score += 0.004
    if length < 40:
        score -= 0.002
    if "?" in text:
        score += 0.002
    return max(score, 0.001)


def generate_synthetic_ads(n: int = 500, seed: int = 42) -> List[Dict]:
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)

    ads = []
    for i in range(n):
        topic = rng.choice(TOPICS)
        style = rng.choice(STYLE)
        cta = rng.choice(CTA)
        text = _build_text(topic, style, cta, seed + i)
        base_ctr = _score_text(text)
        noise = np_rng.normal(0, 0.002)
        ctr = max(min(base_ctr + noise, 0.08), 0.002)
        impressions = int(np_rng.integers(800, 50000))
        clicks = int(np_rng.binomial(impressions, ctr))
        ads.append(
            {
                "ad_id": f"syn_{i:05d}",
                "page_name": f"{topic.title()} Page",
                "ad_creative_body": text,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": clicks / impressions if impressions else 0.0,
                "topic": topic,
                "style": style,
            }
        )
    return ads


def save_synthetic_csv(path: str, n: int = 500, seed: int = 42) -> None:
    import pandas as pd

    ads = generate_synthetic_ads(n=n, seed=seed)
    df = pd.DataFrame(ads)
    df.to_csv(path, index=False)
