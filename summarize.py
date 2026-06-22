import requests

from scripts.config import ANTHROPIC_API_KEY, ENABLE_TR_SUMMARY

PROMPT = (
    "Aşağıdaki plastik cerrahi makale abstract'ını bir asistan hekim için "
    "3-4 cümlelik, klinik anlamı vurgulayan Türkçe özete çevir. "
    "Yöntem, ana bulgu ve klinik çıkarım net olsun.\n\nAbstract:\n\n"
)


def summarize_tr(abstract: str) -> str:
    if not ENABLE_TR_SUMMARY or not ANTHROPIC_API_KEY or not abstract.strip():
        return ""
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": PROMPT + abstract}],
            },
            timeout=60,
        )
        data = resp.json()
        return "".join(b.get("text", "") for b in data.get("content", []))
    except Exception:
        return ""
