import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from src.agents import run_batch_sim
from src.data_ad_library import load_ads_with_fallback
from src.eval import summarize_results
from src.reward_model import train_reward_model
from src.rlpf_sim import simulate_rlpf


def _proxy_score(text: str) -> float:
    length = len(text)
    score = 0.01
    if any(token in text for token in ["Sign up", "Shop", "Get started", "Learn more", "See details"]):
        score += 0.008
    if 60 <= length <= 120:
        score += 0.004
    if "?" in text:
        score += 0.002
    return max(score, 0.001)


def build_scores(df: pd.DataFrame) -> pd.Series:
    if "ctr" in df.columns:
        return df["ctr"].fillna(0.0)
    if "clicks" in df.columns and "impressions" in df.columns:
        with np.errstate(divide="ignore", invalid="ignore"):
            ctr = df["clicks"].fillna(0) / df["impressions"].replace(0, np.nan)
        return ctr.fillna(0.0)
    return df["text"].fillna("").map(_proxy_score)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-terms", default="education")
    parser.add_argument("--countries", default="US")
    parser.add_argument("--max-records", type=int, default=300)
    parser.add_argument("--token", default=None)
    parser.add_argument("--n-variations", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default="logs")
    args = parser.parse_args()

    data = load_ads_with_fallback(
        search_terms=args.search_terms,
        ad_reached_countries=[c.strip() for c in args.countries.split(",")],
        max_records=args.max_records,
        token=args.token,
    )

    df = pd.DataFrame(data)
    if "text" not in df.columns:
        df["text"] = df["ad_creative_body"].fillna("")
    df["text"] = df["text"].fillna("")
    df = df[df["text"].str.strip().astype(bool)]

    if df.empty:
        raise SystemExit("No text records available after filtering.")

    df["score"] = build_scores(df)

    reward_model = train_reward_model(df["text"], df["score"])
    results = simulate_rlpf(
        df["text"].tolist(),
        reward_model=reward_model,
        n_variations=args.n_variations,
        seed=args.seed,
    )
    summary = summarize_results(results)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    summary_path = out_dir / f"summary_{stamp}.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    sample_runs = run_batch_sim(df["text"].head(2).tolist(), reward_model)
    sample_path = out_dir / f"agent_runs_{stamp}.json"
    with sample_path.open("w", encoding="utf-8") as f:
        json.dump(sample_runs, f, ensure_ascii=False, indent=2)

    df.to_csv(out_dir / f"ads_{stamp}.csv", index=False)

    print("Saved:")
    print(summary_path)
    print(sample_path)


if __name__ == "__main__":
    main()
