# Football Data Aggregator - DevOps Control Work

A complete DevOps project for collecting, normalizing, storing and visualizing football match data from multiple sources.

## Goal

The system demonstrates:

- GitHub repository structure
- Python parser and data normalization
- PostgreSQL database design
- Web application with multiple pages
- pgAdmin for database administration
- Metabase for dashboards and visualization
- Docker and Docker Compose containerization
- Nginx reverse proxy as a single entry point
- GitHub Actions CI pipeline with linting and tests

## Architecture

```text
Source A JSON ----\
                  Parser + Normalizer ---- PostgreSQL ---- Metabase
Source B JSON ----/                         |              |
                                            |              |
                                          Web App       pgAdmin
                                            \              /
                                             \            /
                                                Nginx
```

## Services

| Service | Description | URL |
|---|---|---|
| Nginx | Single entry point | http://localhost |
| Web App | Main interface | http://localhost |
| Matches Page | Match data | http://localhost/matches |
| Logs Page | Log instructions | http://localhost/logs |
| pgAdmin | Database administration | http://localhost/pgadmin |
| Metabase | Analytics dashboards | http://localhost/metabase |
| PostgreSQL | Database | localhost:5432 |

Direct development URLs are also exposed:

- Web App: http://localhost:5000
- pgAdmin: http://localhost:5050
- Metabase: http://localhost:3000

## Database credentials

```text
POSTGRES_DB=football
POSTGRES_USER=football_user
POSTGRES_PASSWORD=football_password
```

pgAdmin login:

```text
Email: admin@example.com
Password: admin123
```

PostgreSQL server inside pgAdmin:

```text
Host: postgres
Port: 5432
Database: football
Username: football_user
Password: football_password
```

## Run the project

```bash
docker compose up --build
```

The parser runs after PostgreSQL is healthy and inserts normalized sample football data.

To run the parser again:

```bash
docker compose run --rm parser
```

To stop everything:

```bash
docker compose down
```

To remove volumes and reset data:

```bash
docker compose down -v
```

## Metabase dashboard setup

1. Open http://localhost/metabase
2. Create the first admin account.
3. Add PostgreSQL database:
   - Host: `postgres`
   - Port: `5432`
   - Database: `football`
   - User: `football_user`
   - Password: `football_password`
4. Create at least one dashboard.
5. Recommended charts:
   - Goals by team from `team_statistics`
   - Points by team from `team_statistics`
   - Matches by league from `matches`

## Data model

Main table: `matches`

| Field | Type | Description |
|---|---|---|
| id | SERIAL PRIMARY KEY | Unique row ID |
| source | VARCHAR | Data source name |
| league | VARCHAR | League name |
| home_team | VARCHAR | Home team |
| away_team | VARCHAR | Away team |
| home_goals | INT | Home goals |
| away_goals | INT | Away goals |
| match_date | TIMESTAMPTZ | Match date |
| created_at | TIMESTAMPTZ | Creation timestamp |
| updated_at | TIMESTAMPTZ | Update timestamp |

The project also creates a `team_statistics` view for analytics.

## Normalization example

Source A:

```json
{
  "homeTeam": "Arsenal",
  "awayTeam": "Chelsea",
  "score": {"fullTime": {"home": 2, "away": 1}},
  "utcDate": "2026-05-01T18:00:00Z"
}
```

Source B:

```json
{
  "team_home": "Tottenham",
  "team_away": "Newcastle",
  "goals_home": 0,
  "goals_away": 0,
  "date": "2026-05-04 15:00:00"
}
```

Unified schema:

```json
{
  "source": "source_a_json",
  "league": "Premier League",
  "home_team": "Arsenal",
  "away_team": "Chelsea",
  "home_goals": 2,
  "away_goals": 1,
  "match_date": "2026-05-01T18:00:00Z"
}
```

## External sources

By default, the project uses local sample JSON files so it works without API keys.

You can replace them with HTTP JSON APIs using environment variables in `docker-compose.yml`:

```yaml
environment:
  SOURCE_A_URL: "https://example.com/source-a.json"
  SOURCE_B_URL: "https://example.com/source-b.json"
```

## CI/CD

GitHub Actions runs on push and pull request:

- installs dependencies
- runs Ruff linter
- runs Pytest tests

Workflow file:

```text
.github/workflows/ci.yml
```

## Project structure

```text
football-devops-project/
├── db/
│   └── init.sql
├── docs/
│   └── architecture.md
├── nginx/
│   └── default.conf
├── parser/
│   ├── Dockerfile
│   ├── main.py
│   ├── normalizer.py
│   ├── requirements.txt
│   ├── sample_source_a.json
│   └── sample_source_b.json
├── tests/
│   └── test_normalizer.py
├── webapp/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── requirements-dev.txt
└── README.md
```

## Kubernetes optional extension

For additional complexity, replace Docker Compose with Kubernetes resources:

- Deployment for webapp
- Deployment or CronJob for parser
- StatefulSet or external service for PostgreSQL
- Services for webapp, pgAdmin and Metabase
- Ingress for routing instead of Nginx reverse proxy

## Screenshots

Add screenshots after running the project:

- Home page
- Matches page
- pgAdmin connection
- Metabase dashboard
- GitHub Actions successful run

### Kubernetes files included

Basic Kubernetes manifests are included in `k8s/`:

```bash
docker build -t football-webapp:latest ./webapp
docker build -t football-parser:latest ./parser
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/webapp.yaml
kubectl apply -f k8s/parser-job.yaml
kubectl apply -f k8s/ingress.yaml
```

For local testing without Ingress:

```bash
kubectl port-forward service/football-webapp 8080:80
```
