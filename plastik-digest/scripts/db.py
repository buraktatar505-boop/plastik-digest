import json
import os
import sqlite3
from datetime import datetime

from scripts.config import DATA_DIR, DB_PATH

_COLS = (
    "date", "category", "pmid", "title", "authors", "journal", "year",
    "doi", "pubmed_url", "citation_count", "rcr", "abstract", "abstract_tr", "score",
)


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS shown_articles (
                pmid       TEXT PRIMARY KEY,
                category   TEXT,
                shown_date TEXT
            );
            CREATE TABLE IF NOT EXISTS daily_pick (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                date           TEXT,
                category       TEXT,
                pmid           TEXT,
                title          TEXT,
                authors        TEXT,
                journal        TEXT,
                year           INTEGER,
                doi            TEXT,
                pubmed_url     TEXT,
                citation_count INTEGER,
                rcr            REAL,
                abstract       TEXT,
                abstract_tr    TEXT,
                score          REAL
            );
        """)


def already_shown(pmids: list[str]) -> set[str]:
    if not pmids:
        return set()
    with _conn() as con:
        placeholders = ",".join("?" * len(pmids))
        rows = con.execute(
            f"SELECT pmid FROM shown_articles WHERE pmid IN ({placeholders})", pmids
        ).fetchall()
    return {row[0] for row in rows}


def save_pick(row: dict) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    with _conn() as con:
        con.execute(
            f"INSERT INTO daily_pick ({','.join(_COLS)}) VALUES ({','.join(['?']*len(_COLS))})",
            (
                today,
                row.get("category", ""),
                row.get("pmid", ""),
                row.get("title", ""),
                row.get("authors", ""),
                row.get("journal", ""),
                row.get("year"),
                row.get("doi", ""),
                row.get("pubmed_url", ""),
                row.get("citation_count", 0),
                row.get("rcr"),
                row.get("abstract", ""),
                row.get("abstract_tr", ""),
                row.get("score"),
            ),
        )
        con.execute(
            "INSERT OR IGNORE INTO shown_articles (pmid, category, shown_date) VALUES (?,?,?)",
            (row.get("pmid", ""), row.get("category", ""), today),
        )


def export_json() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    with _conn() as con:
        rows = con.execute(
            f"SELECT {','.join(_COLS)} FROM daily_pick ORDER BY date DESC, category"
        ).fetchall()

    all_picks = [dict(zip(_COLS, r)) for r in rows]
    today_picks = [p for p in all_picks if p["date"] == today]

    with open(os.path.join(DATA_DIR, "today.json"), "w", encoding="utf-8") as f:
        json.dump({"date": today, "articles": today_picks}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(DATA_DIR, "archive.json"), "w", encoding="utf-8") as f:
        json.dump(all_picks, f, ensure_ascii=False, indent=2)
