"""
Günlük orkestrasyon betiği.
Çalıştırma: python -m scripts.daily_job  (proje kök dizininden)
"""
from datetime import datetime

from scripts import config
from scripts.db import already_shown, export_json, init_db, save_pick
from scripts.icite import lookup as icite_lookup
from scripts.pubmed import efetch_abstract, esearch, esummary
from scripts.scoring import score_articles
from scripts.summarize import summarize_tr


def _build_candidate(pmid: str, summaries: dict, icite: dict) -> dict | None:
    pub = icite.get(pmid, {})
    s = summaries.get(pmid, {})
    if not pub and not s:
        return None

    # Authors: ilk 3 + et al.
    authors_raw = s.get("authors", [])
    if isinstance(authors_raw, list):
        names = [a.get("name", "") for a in authors_raw[:3]]
        authors = ", ".join(n for n in names if n)
        if len(authors_raw) > 3:
            authors += " et al."
    else:
        authors = str(authors_raw)

    # Year
    year: int | None = pub.get("year")
    if year is None:
        raw_date = s.get("pubdate", "")
        try:
            year = int(str(raw_date)[:4])
        except (ValueError, TypeError):
            year = None

    return {
        "pmid": pmid,
        "title": pub.get("title") or s.get("title", ""),
        "authors": authors,
        "journal": pub.get("journal") or s.get("fulljournalname") or s.get("source", ""),
        "year": year,
        "doi": pub.get("doi") or "",
        "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "citation_count": pub.get("citation_count") or 0,
        "rcr": pub.get("relative_citation_ratio"),
        "citations_per_year": pub.get("citations_per_year") or 0.0,
    }


def run() -> dict:
    init_db()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] Daily job starting — MODE={config.MODE}, RECENCY={config.RECENCY_YEARS}yr")

    results: dict[str, dict] = {}

    for category in ["aesthetic", "reconstructive"]:
        print(f"\n  [{category}] PubMed aranıyor...")
        pmids = esearch(category, retmax=200)
        print(f"  [{category}] {len(pmids)} aday bulundu")

        shown = already_shown(pmids)
        pmids = [p for p in pmids if p not in shown]
        print(f"  [{category}] {len(pmids)} aday (tekrar filtresi sonrası)")

        if not pmids:
            print(f"  [{category}] Yeni makale yok, atlanıyor.")
            continue

        print(f"  [{category}] iCite skoru alınıyor...")
        icite = icite_lookup(pmids)

        print(f"  [{category}] esummary meta verisi alınıyor...")
        summaries = esummary(pmids)

        candidates = []
        for pmid in pmids:
            c = _build_candidate(pmid, summaries, icite)
            if c:
                c["category"] = category
                candidates.append(c)

        if not candidates:
            print(f"  [{category}] Aday oluşturulamadı, atlanıyor.")
            continue

        scored = score_articles(candidates)
        best = scored[0]
        print(f"  [{category}] En iyi: PMID={best['pmid']} skor={best['score']}")

        print(f"  [{category}] Abstract alınıyor...")
        abstract = efetch_abstract(best["pmid"])
        best["abstract"] = abstract

        print(f"  [{category}] Türkçe özet üretiliyor...")
        best["abstract_tr"] = summarize_tr(abstract)

        save_pick(best)
        results[category] = best
        print(f"  [{category}] Kaydedildi ✓")

    export_json()
    print(f"\n[{today}] Tamamlandı. {len(results)} makale kaydedildi.")
    return results


if __name__ == "__main__":
    run()
        from scripts.render import render_today, render_archive
    import json, os
    with open(os.path.join(config.DATA_DIR, "today.json"), encoding="utf-8") as f:
        today_data = json.load(f)
    with open(os.path.join(config.DATA_DIR, "archive.json"), encoding="utf-8") as f:
        archive_data = json.load(f)
    render_today(today_data)
    render_archive(archive_data)
    print(f"[{today}] HTML oluşturuldu.")

