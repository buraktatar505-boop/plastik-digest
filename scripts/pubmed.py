import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from scripts.config import NCBI_API_KEY, NCBI_TOOL, NCBI_EMAIL, RECENCY_YEARS, MODE

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

QUERIES: dict[str, str] = {
    "aesthetic": (
        '("Surgery, Plastic"[Mesh] OR "Esthetics"[Mesh] OR aesthetic*[tiab] OR cosmetic*[tiab])'
        ' AND (rhinoplasty[tiab] OR "breast augmentation"[tiab] OR mammaplasty[tiab]'
        ' OR rhytidectomy[tiab] OR facelift[tiab] OR blepharoplasty[tiab]'
        ' OR liposuction[tiab] OR abdominoplasty[tiab] OR "body contouring"[tiab]'
        ' OR "fat grafting"[tiab] OR botulinum[tiab] OR filler*[tiab])'
        " AND English[lang] AND Journal Article[ptyp]"
    ),
    "reconstructive": (
        '("Reconstructive Surgical Procedures"[Mesh] OR "Free Tissue Flaps"[Mesh]'
        ' OR "Surgical Flaps"[Mesh] OR "Perforator Flap"[Mesh]'
        ' OR microsurg*[tiab] OR "breast reconstruction"[tiab]'
        ' OR "flap reconstruction"[tiab] OR "free flap"[tiab]'
        ' OR "tissue expansion"[tiab] OR "nerve transfer"[tiab]'
        ' OR "wound reconstruction"[tiab] OR replantation[tiab])'
        " AND English[lang] AND Journal Article[ptyp]"
    ),
}


def _common_params(json_mode: bool = True) -> dict:
    p: dict = {"tool": NCBI_TOOL, "email": NCBI_EMAIL}
    if json_mode:
        p["retmode"] = "json"
    if NCBI_API_KEY:
        p["api_key"] = NCBI_API_KEY
    return p


def _date_range() -> str:
    if MODE == "landmark":
        years = 15
    elif MODE == "trending":
        years = 2
    else:
        years = RECENCY_YEARS
    start = (datetime.now() - timedelta(days=365 * years)).strftime("%Y/%m/%d")
    return f' AND ("{start}"[PDat] : "3000"[PDat])'


def _get(url: str, params: dict, retries: int = 3):
    # Respect NCBI rate limits: ~3 req/s without key, ~10 req/s with key
    delay = 0.15 if NCBI_API_KEY else 0.4
    for attempt in range(retries):
        try:
            time.sleep(delay)
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)


def esearch(category: str, retmax: int = 200) -> list[str]:
    query = QUERIES[category] + _date_range()
    params = {
        **_common_params(),
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "sort": "relevance",
    }
    resp = _get(BASE + "esearch.fcgi", params)
    return resp.json().get("esearchresult", {}).get("idlist", [])


def esummary(pmids: list[str]) -> dict:
    if not pmids:
        return {}
    params = {**_common_params(), "db": "pubmed", "id": ",".join(pmids)}
    resp = _get(BASE + "esummary.fcgi", params)
    result = resp.json().get("result", {})
    return {pmid: result[pmid] for pmid in pmids if pmid in result}


def efetch_abstract(pmid: str) -> str:
    params = {
        **_common_params(json_mode=False),
        "db": "pubmed",
        "id": pmid,
        "rettype": "abstract",
        "retmode": "xml",
    }
    resp = _get(BASE + "efetch.fcgi", params)
    try:
        root = ET.fromstring(resp.text)
        parts = []
        for elem in root.iter("AbstractText"):
            label = elem.get("Label", "")
            text = (elem.text or "").strip()
            if label and text:
                parts.append(f"{label}: {text}")
            elif text:
                parts.append(text)
        return " ".join(parts)
    except ET.ParseError:
        return ""
