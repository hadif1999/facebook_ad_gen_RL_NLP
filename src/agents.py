import random
from typing import Dict, List

from .generator import generate_variations
from .reward_model import RewardModel

COPYWRITER_PROMPT = (
    "Role: ad copywriter. Goal: rewrite the ad text to increase engagement. "
    "Constraint: short, clear, with a call-to-action."
)

CRITIC_PROMPT = (
    "Role: performance critic. Goal: score texts by predicted CTR. "
    "Output: numeric score and a short reason."
)

SELECTOR_PROMPT = (
    "Role: selector. Goal: pick the best text based on critic scores and clarity."
)


def run_multi_agent_sim(
    original_text: str,
    reward_model: RewardModel,
    seed: int = 42,
    n_variations: int = 4,
) -> Dict:
    rng = random.Random(seed)
    variations = generate_variations(original_text, n=n_variations, seed=seed)

    scores = reward_model.score_texts([original_text] + variations)
    critique = []
    for text, score in zip([original_text] + variations, scores):
        reason = "Strong CTA" if "Sign up" in text or "Shop" in text else "Clear message"
        critique.append({"text": text, "score": round(score, 4), "reason": reason})

    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    selected_text = ([original_text] + variations)[best_idx]

    return {
        "prompts": {
            "copywriter": COPYWRITER_PROMPT,
            "critic": CRITIC_PROMPT,
            "selector": SELECTOR_PROMPT,
        },
        "original_text": original_text,
        "variations": variations,
        "critic_scores": critique,
        "selected_text": selected_text,
        "selected_score": round(scores[best_idx], 4),
    }


def run_batch_sim(
    texts: List[str],
    reward_model: RewardModel,
    seed: int = 42,
) -> List[Dict]:
    runs = []
    for i, text in enumerate(texts):
        runs.append(run_multi_agent_sim(text, reward_model, seed=seed + i))
    return runs
