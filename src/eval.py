from typing import Dict, List

import numpy as np


def summarize_results(results: List[Dict]) -> Dict:
    deltas = np.array([r["delta"] for r in results], dtype=float)
    orig_scores = np.array([r["original_score"] for r in results], dtype=float)
    best_scores = np.array([r["best_score"] for r in results], dtype=float)

    improvement_rate = float(np.mean(deltas > 0)) if deltas.size else 0.0
    return {
        "count": int(len(results)),
        "mean_original": float(orig_scores.mean()) if orig_scores.size else 0.0,
        "mean_best": float(best_scores.mean()) if best_scores.size else 0.0,
        "mean_delta": float(deltas.mean()) if deltas.size else 0.0,
        "median_delta": float(np.median(deltas)) if deltas.size else 0.0,
        "improvement_rate": improvement_rate,
    }
