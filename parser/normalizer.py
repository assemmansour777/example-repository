from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def parse_date(value: str) -> datetime:
    value = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)


def normalize_source_a(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        score = row.get("score", {}).get("fullTime", {})
        normalized.append(
            {
                "source": "source_a_json",
                "league": row.get("league", "Unknown"),
                "home_team": row.get("homeTeam"),
                "away_team": row.get("awayTeam"),
                "home_goals": int(score.get("home", 0)),
                "away_goals": int(score.get("away", 0)),
                "match_date": parse_date(row.get("utcDate")),
            }
        )
    return normalized


def normalize_source_b(payload: dict[str, Any]) -> list[dict[str, Any]]:
    normalized = []
    for row in payload.get("matches", []):
        normalized.append(
            {
                "source": "source_b_json",
                "league": row.get("competition", "Unknown"),
                "home_team": row.get("team_home"),
                "away_team": row.get("team_away"),
                "home_goals": int(row.get("goals_home", 0)),
                "away_goals": int(row.get("goals_away", 0)),
                "match_date": parse_date(row.get("date")),
            }
        )
    return normalized


def deduplicate(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, str]] = set()
    result = []
    for match in matches:
        key = (
            match["league"],
            match["home_team"],
            match["away_team"],
            match["match_date"].isoformat(),
        )
        if key not in seen:
            seen.add(key)
            result.append(match)
    return result
