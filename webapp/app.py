from __future__ import annotations

import os

import psycopg2
from flask import Flask, redirect, render_template, request

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "football"),
        user=os.getenv("POSTGRES_USER", "football_user"),
        password=os.getenv("POSTGRES_PASSWORD", "football_password"),
    )


def fetch_all(query: str, params: tuple = ()):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]


@app.route("/")
def index():
    matches = fetch_all("SELECT * FROM matches ORDER BY match_date DESC LIMIT 20")
    stats = fetch_all("SELECT * FROM team_statistics ORDER BY points DESC, goals_for DESC LIMIT 10")
    return render_template("index.html", matches=matches, stats=stats)


@app.route("/matches")
def matches_page():
    league = request.args.get("league", "")
    if league:
        matches = fetch_all("SELECT * FROM matches WHERE league ILIKE %s ORDER BY match_date DESC", (f"%{league}%",))
    else:
        matches = fetch_all("SELECT * FROM matches ORDER BY match_date DESC")
    return render_template("matches.html", matches=matches, league=league)


@app.route("/logs")
def logs():
    return render_template("logs.html")


@app.route("/analytics")
def analytics():
    return redirect("/metabase")


@app.route("/admin")
def admin():
    return redirect("/pgadmin")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
