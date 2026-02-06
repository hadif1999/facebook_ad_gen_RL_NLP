# RLPF Ad Text Project (Course Prototype)

This repo implements a **prototype** inspired by the paper *Improving Generative Ad Text on Facebook using Reinforcement Learning*. The paper uses RL with performance feedback (RLPF) and a large-scale A/B test. Since the paper has **no public code or dataset**, this repo provides:

- A **data pipeline** that can pull from the Meta Ad Library API (political/issue ads).
- A **synthetic fallback dataset** when API access is unavailable.
- A **reward model baseline** (TF-IDF + Ridge) with a heuristic fallback.
- A **simulation** of RLPF-style selection over generated text variations.
- A **demo notebook** and experiment logs.

## Project Structure
- `src/` core logic (data loader, reward model, generator, simulation)
- `run_demo.py` command-line demo runner
- `demo/` Jupyter notebook + notes
- `data/` synthetic data (no real data stored)
- `logs/` output artifacts from runs
- `reports/` paper summary (MD + PDF)
- `experiments.md` short experiment log

## Requirements
- Python 3.10 or 3.11
- Install dependencies:

```bash
pip install -r requirements.txt
```

Note: If `scikit-learn` is not installed, the reward model falls back to a heuristic scoring function.

## Running the Demo (Synthetic Fallback)
```bash
python3 run_demo.py --max-records 120 --search-terms education --countries US --n-variations 4 --seed 7 --out-dir logs
```

This produces:
- `logs/summary_*.json`
- `logs/agent_runs_*.json`
- `logs/ads_*.csv`

## Running with Meta Ad Library API (Real Data)
You need a valid access token and API access for the Ad Library archive.

Set environment variables:
```bash
export META_ADLIB_TOKEN="YOUR_TOKEN"
export META_GRAPH_VERSION="v19.0"
```

Then run:
```bash
python3 run_demo.py --search-terms education --countries US --max-records 500
```

Official references:
- https://developers.facebook.com/docs/marketing-api/reference/ads_archive/
- https://github.com/facebookresearch/Ad-Library-API-Script-Repository

## Demo Notebook
Open `demo/demo.ipynb` to reproduce the simulation and plots. The notebook reads `data/synthetic_ads.csv` by default.

## Paper Summary
- English: `reports/paper_summary_en.md`
- Persian: `reports/paper_summary_fa.md`
- PDF (English): `reports/paper_summary.pdf`

If you need a Persian PDF, convert `reports/paper_summary_fa.md` with a local tool (e.g., pandoc + Persian font).

## Notes and Limitations
- The real paper uses **live A/B testing**; this repo provides a **simulation** with synthetic rewards when real data is not accessible.
- Ad Library API only exposes political/issue ads, not all ad categories.
- This is a **course prototype** and not a production-ready system.

## Reproducibility
All random seeds are configurable via CLI. See `experiments.md` for run settings and metrics.
