from datetime import datetime

from scripts.config import MODE, WEIGHTS, JOURNAL_WHITELIST


def _normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    min_v, max_v = min(values), max(values)
    if max_v == min_v:
        return [0.5] * len(values)
    return [(v - min_v) / (max_v - min_v) for v in values]


def _recency_bonus(year: int | None) -> float:
    if year is None:
        return 0.0
    age = datetime.now().year - year
    return max(0.0, 1.0 - age * 0.15)


def _in_whitelist(journal: str | None) -> bool:
    if not journal:
        return False
    return journal.lower().strip() in JOURNAL_WHITELIST


def score_articles(candidates: list[dict]) -> list[dict]:
    """Score and sort articles; highest score first."""
    weights = WEIGHTS.get(MODE, WEIGHTS["balanced"])

    rcr_vals = [c.get("rcr") or 0.0 for c in candidates]
    cite_vals = [c.get("citations_per_year") or 0.0 for c in candidates]

    norm_rcr = _normalize(rcr_vals)
    norm_cite = _normalize(cite_vals)

    scored = []
    for i, c in enumerate(candidates):
        jrnl = 1.0 if _in_whitelist(c.get("journal")) else 0.0
        recent = _recency_bonus(c.get("year"))
        s = (
            weights["rcr"] * norm_rcr[i]
            + weights["cite"] * norm_cite[i]
            + weights["jrnl"] * jrnl
            + weights["recent"] * recent
        )
        scored.append({**c, "score": round(s, 4)})

    # Primary: score desc, tiebreak: newer year first
    return sorted(scored, key=lambda x: (-x["score"], -(x.get("year") or 0)))
