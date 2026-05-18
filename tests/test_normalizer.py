import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "parser"))

from normalizer import deduplicate, normalize_source_a, normalize_source_b  # noqa: E402


def test_normalize_source_a():
    data = [{"league": "Test", "homeTeam": "A", "awayTeam": "B", "score": {"fullTime": {"home": 1, "away": 0}}, "utcDate": "2026-01-01T10:00:00Z"}]
    result = normalize_source_a(data)
    assert result[0]["home_team"] == "A"
    assert result[0]["home_goals"] == 1


def test_normalize_source_b():
    data = {"matches": [{"competition": "Test", "team_home": "A", "team_away": "B", "goals_home": 2, "goals_away": 2, "date": "2026-01-01 10:00:00"}]}
    result = normalize_source_b(data)
    assert result[0]["away_team"] == "B"
    assert result[0]["away_goals"] == 2


def test_deduplicate():
    rows = normalize_source_a([
        {"league": "Test", "homeTeam": "A", "awayTeam": "B", "score": {"fullTime": {"home": 1, "away": 0}}, "utcDate": "2026-01-01T10:00:00Z"},
        {"league": "Test", "homeTeam": "A", "awayTeam": "B", "score": {"fullTime": {"home": 1, "away": 0}}, "utcDate": "2026-01-01T10:00:00Z"},
    ])
    assert len(deduplicate(rows)) == 1
