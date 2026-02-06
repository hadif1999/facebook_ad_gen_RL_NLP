# Experiments Log

## Run 1 (synthetic fallback)
- Date: 2026-02-06
- Command: `python3 run_demo.py --max-records 120 --search-terms education --countries US --n-variations 4 --seed 7 --out-dir logs`
- Data source: Ad Library API fallback to synthetic data (no API token provided).
- Reward model: TF-IDF + Ridge if scikit-learn is available, otherwise heuristic scoring.
- Metrics: mean original score, mean best score, mean delta, median delta, improvement rate.
- Results (from `logs/summary_20260206_133025.json`):
  - count: 120
  - mean_original: 0.01952
  - mean_best: 0.02228
  - mean_delta: 0.00277
  - median_delta: 0.00200
  - improvement_rate: 0.65

## Planned Runs
- Real Ad Library API data with a valid token.
- Compare results across multiple search terms (e.g., education, health, finance).
- Sensitivity analysis: vary `n_variations` and seed.
