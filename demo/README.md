# Demo Data

This folder is used to run the notebook and generate plots.

## Real Data (Ad Library API)
To fetch real ad data, use the Meta Ad Library API. This API only covers political/issue ads and requires an approved access token.

- Official docs: https://developers.facebook.com/docs/marketing-api/reference/ads_archive/
- Official extraction tool: https://github.com/facebookresearch/Ad-Library-API-Script-Repository

After downloading, save the data as `demo/ads_real.csv` and load the text columns in the notebook. Do not commit the CSV to the repo.

## Synthetic Data
If `demo/ads_real.csv` does not exist, the notebook will generate synthetic ads on the fly (no file is saved).
