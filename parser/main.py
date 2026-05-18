from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import psycopg2
import requests
from normalizer import deduplicate, normalize_source_a, normalize_source_b

BASE_DIR = Path(__file__).resolve().parent


def load_json_from_url_or_file(env_name: str, fallback_file: str) -> Any:
    url = os.getenv(env_name)
    if url:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.json()
    with open(BASE_DIR / fallback_file, encoding="utf-8") as file:
        return json.load(file)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "football"),
        user=os.getenv("POSTGRES_USER", "football_user"),
        password=os.getenv("POSTGRES_PASSWORD", "football_password"),
    )


def insert_matches(matches: list[dict[str, Any]]) -> int:
    sql = """
        INSERT INTO matches
        (source, league, home_team, away_team, home_goals, away_goals, match_date)
        VALUES (%(source)s, %(league)s, %(home_team)s, %(away_team)s, %(home_goals)s, %(away_goals)s, %(match_date)s)
        ON CONFLICT (league, home_team, away_team, match_date) DO UPDATE SET
            source = EXCLUDED.source,
            home_goals = EXCLUDED.home_goals,
            away_goals = EXCLUDED.away_goals,
            updated_at = NOW();
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(sql, matches)
        conn.commit()
    return len(matches)


def run() -> int:
    source_a = load_json_from_url_or_file("SOURCE_A_URL", "sample_source_a.json")
    source_b = load_json_from_url_or_file("SOURCE_B_URL", "sample_source_b.json")
    matches = normalize_source_a(source_a) + normalize_source_b(source_b)
    matches = deduplicate(matches)
    return insert_matches(matches)


if __name__ == "__main__":
    total = run()
    print(f"Loaded {total} normalized football matches")
