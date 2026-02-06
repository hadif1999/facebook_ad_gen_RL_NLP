from typing import Dict, Iterable, List

import numpy as np

from .generator import generate_variations
from .reward_model import RewardModel


def simulate_rlpf(
    texts: Iterable[str],
    reward_model: RewardModel,
    n_variations: int = 5,
    seed: int = 42,
) -> List[Dict]:
    results = []
    for idx, text in enumerate(texts):
        variations = generate_variations(text, n=n_variations, seed=seed + idx)
        candidates = [text] + variations
        scores = reward_model.score_texts(candidates)
        best_idx = int(np.argmax(scores))
        results.append(
            {
                "original_text": text,
                "original_score": scores[0],
                "best_text": candidates[best_idx],
                "best_score": scores[best_idx],
                "delta": scores[best_idx] - scores[0],
                "all_scores": scores,
                "all_texts": candidates,
            }
        )
    return results
