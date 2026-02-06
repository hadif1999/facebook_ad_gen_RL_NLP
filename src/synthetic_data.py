import random
from dataclasses import dataclass
from typing import List, Dict

import numpy as np

TOPICS = [
    "کتاب و آموزش",
    "فروشگاه آنلاین",
    "سلامت و تندرستی",
    "گردشگری",
    "اپلیکیشن مالی",
    "ورزش و فیتنس",
    "غذا و نوشیدنی",
    "کسب‌وکار محلی",
]

CTA = [
    "همین امروز امتحان کنید",
    "اکنون ثبت‌نام کنید",
    "جزئیات بیشتر",
    "خرید کنید",
    "شروع کنید",
    "اطلاعات بیشتر",
]

STYLE = [
    "کوتاه و مستقیم",
    "داستانی",
    "پرسشی",
    "توصیه‌محور",
]


def _build_text(topic: str, style: str, cta: str, seed: int) -> str:
    rnd = random.Random(seed)
    openers = {
        "کوتاه و مستقیم": [
            f"{topic} را همین حالا ساده‌تر کنید.",
            f"راه سریع برای {topic}.",
        ],
        "داستانی": [
            f"هفته پیش به دنبال {topic} بودم و یک راه بهتر پیدا کردم.",
            f"وقتی برای {topic} زمان ندارید، این راه کمک می‌کند.",
        ],
        "پرسشی": [
            f"آیا می‌خواهید {topic} را بهتر انجام دهید؟",
            f"چطور می‌شود در {topic} سریع‌تر پیش رفت؟",
        ],
        "توصیه‌محور": [
            f"این توصیه‌ها برای {topic} واقعاً جواب می‌دهند.",
            f"چند قدم ساده برای بهبود {topic}.",
        ],
    }
    benefits = [
        "زمان را ذخیره کنید",
        "هزینه‌ها را کاهش دهید",
        "نتیجه را سریع‌تر ببینید",
        "کیفیت را بالا ببرید",
    ]
    opener = rnd.choice(openers.get(style, openers["کوتاه و مستقیم"]))
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
    if "؟" in text:
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
                "page_name": f"صفحه {topic}",
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
