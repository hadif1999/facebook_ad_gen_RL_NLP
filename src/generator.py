import random
from typing import List

CTA = [
    "همین امروز امتحان کنید",
    "اکنون ثبت‌نام کنید",
    "جزئیات بیشتر",
    "خرید کنید",
    "شروع کنید",
    "اطلاعات بیشتر",
]

PREFIXES = [
    "فرصت محدود:",
    "ویژه امروز:",
    "پیشنهاد تازه:",
]


def _to_question(text: str) -> str:
    if text.endswith("؟"):
        return text
    return f"{text.rstrip('.')}؟"


def _shorten(text: str) -> str:
    parts = text.split(".")
    if len(parts) <= 2:
        return text
    return ".".join(parts[:2]).strip() + "."


def _add_cta(text: str, rng: random.Random) -> str:
    cta = rng.choice(CTA)
    if cta in text:
        return text
    return f"{text.rstrip('.')} . {cta}."


def _add_prefix(text: str, rng: random.Random) -> str:
    prefix = rng.choice(PREFIXES)
    return f"{prefix} {text}"


def generate_variations(text: str, n: int = 5, seed: int = 42) -> List[str]:
    rng = random.Random(seed)
    strategies = [_to_question, _shorten, _add_cta, _add_prefix]
    variations = []
    for i in range(n):
        strategy = rng.choice(strategies)
        if strategy in (_add_cta, _add_prefix):
            new_text = strategy(text, rng)
        else:
            new_text = strategy(text)
        if new_text != text:
            variations.append(new_text)
        else:
            variations.append(f"{text} {rng.choice(CTA)}")
    return variations
