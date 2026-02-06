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

## CLI Arguments (run_demo.py)
- `--search-terms`: Search keywords for Ad Library API queries. If no API token is provided, it does not change synthetic data generation. Default: `education`.
- `--countries`: Comma-separated country codes for `ad_reached_countries` in the Ad Library API. Default: `US`.
- `--max-records`: Maximum number of ads to fetch or generate. Default: `300`.
- `--token`: Access token for Meta Ad Library API. If omitted, the script uses synthetic fallback data. Default: `None`.
- `--n-variations`: Number of text variations generated per ad. Default: `5`.
- `--seed`: Random seed for reproducible generation and sampling. Default: `42`.
- `--out-dir`: Output directory for run artifacts. Default: `logs`.

## Running with Real data Meta Ad Library API (Optional)
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

## Outputs and Interpretation
The prototype produces a few key outputs to make results easy to interpret:

- **Notebook plots (`demo/demo.ipynb`)**: A histogram of reward improvements (`delta = best_score - original_score`). This shows how often the selected variation improves the reward and how large those improvements are.
- **Run summary JSON (`logs/summary_*.json`)**:
  - `count`: number of texts evaluated.
  - `mean_original`: average reward of the original texts.
  - `mean_best`: average reward of the selected best variations.
  - `mean_delta`: mean improvement (`best - original`).
  - `median_delta`: median improvement.
  - `improvement_rate`: fraction of cases where the best variation scores higher than the original.
- **Agent trace JSON (`logs/agent_runs_*.json`)**: Two example runs with the original text, generated variations, reward scores, and the selected best text. This provides a qualitative sanity check.
- **Ads CSV (`logs/ads_*.csv`)**: The processed dataset snapshot (text + proxy scores + metadata) for further analysis.

## Paper Summary
- PDF : `reports/report.pdf`


## Notes and Limitations
- The real paper uses **live A/B testing**; this repo provides a **simulation** with synthetic rewards when real data is not accessible.
- Ad Library API only exposes political/issue ads, not all ad categories.
- This is a **course prototype** and not a production-ready system.

## Reproducibility
All random seeds are configurable via CLI. See `experiments.md` for run settings and metrics.

### project video link 
https://drive.google.com/file/d/1XAQF1NJEWgyr3Kl9dkaUCsAdUWYZK_Vg/view?usp=drive_link

### presentation video link 
https://drive.google.com/file/d/1EIfssUWH0sL1ZAE9eJqcefhM1oQhEvB6/view?usp=drive_link

