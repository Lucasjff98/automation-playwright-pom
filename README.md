![CI](https://github.com/Lucasjff98/playwright-scraper-api/actions/workflows/ci.yml/badge.svg)

# Web Automation & Data Extraction API

A web automation and data-extraction pipeline built with **Python**, **Playwright**, **FastAPI**, and the **Page Object Model (POM)** design pattern. The scraper collects data with resilient element selection and dynamic pagination, persists it in a database, and exposes it through a REST API — turning a one-off script into a small service (target site: [quotes.toscrape.com](https://quotes.toscrape.com/), a public scraping sandbox).

---

## 🎯 What it does

- Automates multi-page navigation and structured data extraction.
- Waits explicitly for content before scraping (both on initial load and after pagination), instead of assuming the DOM is ready.
- Validates every extracted record through a Pydantic model — the same model is reused for both the scraper's output and the API's schema, so both give the same guarantee.
- Persists results in a SQLite database, skipping exact duplicates on re-runs.
- Exposes the collected data through a FastAPI service, with filtering, pagination, and an endpoint to trigger a fresh scrape on demand.
- Captures failure artifacts (screenshots and Playwright execution traces) on error.

---

## 🏗️ Architecture

```text
automation-playwright-pom/
├── src/
│   ├── pages/
│   │   ├── base_page.py      # Core browser actions, waits & trace artifacts
│   │   └── quotes_page.py    # Page Object Model for the target UI
│   ├── scraper/
│   │   └── runner.py         # Orchestrates the scraping pipeline (no I/O side effects)
│   ├── db/
│   │   └── database.py       # SQLAlchemy models & persistence helpers
│   ├── api/
│   │   ├── main.py           # FastAPI app entrypoint
│   │   ├── routes.py         # /quotes and /scrape endpoints
│   │   └── schemas.py        # API request/response schemas
│   ├── models.py             # Shared Pydantic model for validated output
│   └── main.py               # CLI entrypoint: scrape, save to JSON and DB
├── tests/
│   ├── test_models.py        # Unit tests (no browser needed)
│   ├── test_api.py           # API unit tests (isolated in-memory database)
│   └── test_quotes_page.py   # Integration tests (spin up a real browser)
├── artifacts/                # Generated failure screenshots and trace.zip files
├── output/                   # Extracted JSON data files
├── pyproject.toml            # Project setup & dependencies
└── README.md
```

---

## ▶️ Usage

### CLI (scrape once, save to JSON and database)

```bash
pip install -r requirements.txt
playwright install chromium

# Headless run, default settings
python -m src.main --headless

# Visible browser, slower for debugging, custom output path and page limit
python -m src.main --slow-mo 500 --max-pages 5 --output output/result.json
```

Run `python -m src.main --help` for all options.

### API (serve the collected data)

```bash
uvicorn src.api.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for interactive API documentation.

- `GET /quotes` — list stored quotes, with optional `author` filter and pagination (`limit`, `offset`)
- `POST /scrape` — run the scraper on demand and persist any new results
- `GET /health` — health check

## ✅ Tests

```bash
pytest -m "not integration"   # unit tests (models + API), fast, no browser
pytest -m integration         # integration tests, needs `playwright install`
```
