CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    source VARCHAR(80) NOT NULL,
    league VARCHAR(120) NOT NULL,
    home_team VARCHAR(120) NOT NULL,
    away_team VARCHAR(120) NOT NULL,
    home_goals INT NOT NULL DEFAULT 0,
    away_goals INT NOT NULL DEFAULT 0,
    match_date TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_match UNIQUE (league, home_team, away_team, match_date)
);

CREATE OR REPLACE VIEW team_statistics AS
SELECT
    league,
    team,
    COUNT(*) AS matches_played,
    SUM(goals_for) AS goals_for,
    SUM(goals_against) AS goals_against,
    SUM(CASE WHEN goals_for > goals_against THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN goals_for = goals_against THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN goals_for < goals_against THEN 1 ELSE 0 END) AS losses,
    SUM(CASE
        WHEN goals_for > goals_against THEN 3
        WHEN goals_for = goals_against THEN 1
        ELSE 0
    END) AS points
FROM (
    SELECT league, home_team AS team, home_goals AS goals_for, away_goals AS goals_against FROM matches
    UNION ALL
    SELECT league, away_team AS team, away_goals AS goals_for, home_goals AS goals_against FROM matches
) t
GROUP BY league, team;
