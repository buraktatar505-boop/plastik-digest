import os
from dotenv import load_dotenv

load_dotenv()

NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")
NCBI_TOOL = os.getenv("NCBI_TOOL", "PlastikDigest")
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ENABLE_TR_SUMMARY = os.getenv("ENABLE_TR_SUMMARY", "true").lower() == "true"
MODE = os.getenv("MODE", "balanced")
RECENCY_YEARS = int(os.getenv("RECENCY_YEARS", "5"))
DB_PATH = os.getenv("DB_PATH", "data/digest.sqlite")
DATA_DIR = os.getenv("DATA_DIR", "data")

# Scoring weights per mode (rcr, cite_rate, journal_whitelist, recency)
WEIGHTS: dict[str, dict[str, float]] = {
    "balanced": {"rcr": 0.45, "cite": 0.25, "jrnl": 0.20, "recent": 0.10},
    "landmark": {"rcr": 0.35, "cite": 0.45, "jrnl": 0.15, "recent": 0.00},
    "trending": {"rcr": 0.30, "cite": 0.45, "jrnl": 0.15, "recent": 0.10},
}

JOURNAL_WHITELIST: set[str] = {
    # Full names
    "plastic and reconstructive surgery",
    "aesthetic surgery journal",
    "journal of plastic, reconstructive & aesthetic surgery",
    "annals of plastic surgery",
    "aesthetic plastic surgery",
    "plastic and reconstructive surgery - global open",
    "plastic and reconstructive surgery global open",
    "journal of reconstructive microsurgery",
    "microsurgery",
    "journal of hand surgery",
    "journal of hand surgery, american volume",
    "journal of hand surgery european volume",
    # Common abbreviations
    "plast reconstr surg",
    "aesthetic surg j",
    "j plast reconstr aesthet surg",
    "ann plast surg",
    "aesthet plast surg",
    "plast reconstr surg glob open",
    "j reconstr microsurg",
    "j hand surg",
    "j hand surg am",
    "j hand surg eur vol",
}
