import time
import requests

BASE = "https://icite.od.nih.gov/api/pubs"


def _get(params: dict, retries: int = 3):
    for attempt in range(retries):
        try:
            time.sleep(0.2)
            resp = requests.get(BASE, params=params, timeout=30)
            resp.raise_for_status()
            return resp
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)


def lookup(pmids: list[str]) -> dict[str, dict]:
    """Fetch citation/RCR data for up to any number of PMIDs (batched at 100)."""
    if not pmids:
        return {}
    result: dict[str, dict] = {}
    for i in range(0, len(pmids), 100):
        batch = pmids[i : i + 100]
        resp = _get({"pmids": ",".join(batch), "format": "json"})
        for pub in resp.json().get("data", []):
            pmid = str(pub.get("pmid", ""))
            if pmid:
                result[pmid] = pub
    return result
