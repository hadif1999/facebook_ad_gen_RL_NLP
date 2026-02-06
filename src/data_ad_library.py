import os
import time
from typing import Dict, Iterable, List, Optional

import requests

from .synthetic_data import generate_synthetic_ads

DEFAULT_FIELDS = [
    "id",
    "page_name",
    "ad_creation_time",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "ad_creative_body",
    "ad_creative_link_title",
    "ad_creative_link_description",
    "impressions",
    "spend",
    "currency",
    "estimated_audience_size",
    "ad_snapshot_url",
]

DEFAULT_PARAMS = {
    "ad_active_status": "ALL",
    "ad_type": "POLITICAL_AND_ISSUE_ADS",
}


def _extract_range(value: object) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, dict):
        lower = value.get("lower_bound")
        upper = value.get("upper_bound")
        if lower is not None and upper is not None:
            return (float(lower) + float(upper)) / 2.0
        return float(lower) if lower is not None else float(upper) if upper is not None else None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _merge_text(record: Dict) -> str:
    parts = []
    for key in (
        "ad_creative_body",
        "ad_creative_link_title",
        "ad_creative_link_description",
    ):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    return "\n".join(parts)


def normalize_ads(records: Iterable[Dict]) -> List[Dict]:
    normalized = []
    for rec in records:
        impressions = _extract_range(rec.get("impressions"))
        spend = _extract_range(rec.get("spend"))
        normalized.append(
            {
                "ad_id": rec.get("id"),
                "page_name": rec.get("page_name"),
                "ad_creation_time": rec.get("ad_creation_time"),
                "ad_delivery_start_time": rec.get("ad_delivery_start_time"),
                "ad_delivery_stop_time": rec.get("ad_delivery_stop_time"),
                "ad_creative_body": rec.get("ad_creative_body"),
                "ad_creative_link_title": rec.get("ad_creative_link_title"),
                "ad_creative_link_description": rec.get("ad_creative_link_description"),
                "text": _merge_text(rec),
                "impressions": impressions,
                "spend": spend,
                "currency": rec.get("currency"),
                "estimated_audience_size": rec.get("estimated_audience_size"),
                "ad_snapshot_url": rec.get("ad_snapshot_url"),
            }
        )
    return normalized


def build_params(
    search_terms: str,
    ad_reached_countries: List[str],
    fields: Optional[List[str]] = None,
    limit: int = 50,
    ad_active_status: str = "ALL",
    ad_type: str = "POLITICAL_AND_ISSUE_ADS",
    ad_delivery_date_min: Optional[str] = None,
    ad_delivery_date_max: Optional[str] = None,
) -> Dict:
    params = {
        "search_terms": search_terms,
        "ad_reached_countries": ",".join(ad_reached_countries),
        "ad_active_status": ad_active_status,
        "ad_type": ad_type,
        "limit": limit,
    }
    if fields:
        params["fields"] = ",".join(fields)
    if ad_delivery_date_min:
        params["ad_delivery_date_min"] = ad_delivery_date_min
    if ad_delivery_date_max:
        params["ad_delivery_date_max"] = ad_delivery_date_max
    return params


def fetch_ads(
    search_terms: str,
    ad_reached_countries: List[str],
    token: Optional[str] = None,
    max_records: int = 500,
    fields: Optional[List[str]] = None,
    graph_version: Optional[str] = None,
    sleep_seconds: float = 0.2,
    **kwargs,
) -> List[Dict]:
    token = token or os.getenv("META_ADLIB_TOKEN")
    if not token:
        return generate_synthetic_ads(n=min(max_records, 500))

    version = graph_version or os.getenv("META_GRAPH_VERSION", "v19.0")
    endpoint = f"https://graph.facebook.com/{version}/ads_archive"

    params = build_params(
        search_terms=search_terms,
        ad_reached_countries=ad_reached_countries,
        fields=fields or DEFAULT_FIELDS,
        **kwargs,
    )
    params["access_token"] = token

    all_records: List[Dict] = []
    next_url = endpoint
    while next_url and len(all_records) < max_records:
        response = requests.get(next_url, params=params, timeout=30)
        if response.status_code != 200:
            break
        payload = response.json()
        data = payload.get("data", [])
        all_records.extend(data)
        paging = payload.get("paging", {})
        next_url = paging.get("next")
        params = None
        if sleep_seconds:
            time.sleep(sleep_seconds)
        if not data:
            break
    if not all_records:
        return generate_synthetic_ads(n=min(max_records, 500))
    return normalize_ads(all_records[:max_records])


def load_ads_with_fallback(
    search_terms: str,
    ad_reached_countries: List[str],
    max_records: int = 500,
    token: Optional[str] = None,
) -> List[Dict]:
    try:
        data = fetch_ads(
            search_terms=search_terms,
            ad_reached_countries=ad_reached_countries,
            token=token,
            max_records=max_records,
        )
        return data
    except requests.RequestException:
        return generate_synthetic_ads(n=min(max_records, 500))
