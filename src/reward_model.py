from dataclasses import dataclass
from typing import Iterable, List

import numpy as np

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import Ridge
    _SKLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover - fallback path
    TfidfVectorizer = None
    Ridge = None
    _SKLEARN_AVAILABLE = False


def _heuristic_score(text: str) -> float:
    score = 0.01
    if any(token in text for token in ["ثبت‌نام", "خرید", "شروع", "جزئیات"]):
        score += 0.008
    if 60 <= len(text) <= 120:
        score += 0.004
    if "؟" in text:
        score += 0.002
    return max(score, 0.001)


@dataclass
class RewardModel:
    min_df: int = 2
    ngram_range: tuple = (1, 2)
    alpha: float = 1.0

    def __post_init__(self) -> None:
        self._use_sklearn = _SKLEARN_AVAILABLE
        if self._use_sklearn:
            self.vectorizer = TfidfVectorizer(
                min_df=self.min_df,
                ngram_range=self.ngram_range,
                max_features=5000,
            )
            self.model = Ridge(alpha=self.alpha, random_state=42)
        else:
            self.vectorizer = None
            self.model = None

    def fit(self, texts: Iterable[str], scores: Iterable[float]) -> "RewardModel":
        if self._use_sklearn:
            X = self.vectorizer.fit_transform(texts)
            y = np.asarray(list(scores), dtype=float)
            self.model.fit(X, y)
        return self

    def predict(self, texts: Iterable[str]) -> np.ndarray:
        if self._use_sklearn:
            X = self.vectorizer.transform(texts)
            return self.model.predict(X)
        return np.asarray([_heuristic_score(t) for t in texts], dtype=float)

    def score_texts(self, texts: Iterable[str]) -> List[float]:
        return self.predict(texts).tolist()


def train_reward_model(texts: Iterable[str], scores: Iterable[float]) -> RewardModel:
    model = RewardModel()
    model.fit(texts, scores)
    return model
