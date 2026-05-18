# Architecture

```text
External JSON Source A ----\
                         Parser + Normalizer ---- PostgreSQL ---- Metabase
External JSON Source B ----/                         |              |
                                                     |              |
                                                   Web App       pgAdmin
                                                     \              /
                                                      \            /
                                                         Nginx
```

## Components

- Parser: collects football data from two sources and normalizes it.
- PostgreSQL: stores normalized match data.
- Web App: displays home page, matches page and logs page.
- Metabase: analytics and dashboards.
- pgAdmin: database administration.
- Nginx: single entry point and reverse proxy.
- GitHub Actions: linting and automated tests.
