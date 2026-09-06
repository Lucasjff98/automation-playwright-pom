# Web Automation & Data Extraction Engine

A web automation and data-extraction pipeline built with **Python**, **Playwright**, and the **Page Object Model (POM)** design pattern. Demonstrates resilient element selection, dynamic pagination, Pydantic-validated output, and fault-tolerant execution trace auditing (target site: [quotes.toscrape.com](https://quotes.toscrape.com/), a public scraping sandbox).

---

## 🎯 What it does

- Automates multi-page navigation and structured data extraction.
- Waits explicitly for content before scraping (both on initial load and after pagination), instead of assuming the DOM is ready.
- Validates every extracted record through a Pydantic model before writing it out.
- Captures failure artifacts (screenshots and Playwright execution traces) on error.
- Exports structured output in JSON for downstream analytics or database ingestion.

---

## 🏗️ Architecture

```text
automation-playwright-pom/
├── src/
│   ├── pages/
│   │   ├── base_page.py      # Core browser actions, waits & trace artifacts
│   │   └── quotes_page.py    # Page Object Model for the target UI
│   ├── models.py             # Pydantic model for validated output
│   └── main.py               # CLI, orchestration pipeline & tracing setup
├── tests/
│   ├── test_models.py        # Unit tests (no browser needed)
│   └── test_quotes_page.py   # Integration tests (spin up a real browser)
├── artifacts/                # Generated failure screenshots and trace.zip files
├── output/                   # Extracted JSON data files
├── pyproject.toml            # Project setup & dependencies
└── README.md
```

---

## ▶️ Usage

```bash
pip install -r requirements.txt
playwright install chromium

# Headless run, default settings
python -m src.main --headless

# Visible browser, slower for debugging, custom output path and page limit
python -m src.main --slow-mo 500 --max-pages 5 --output output/result.json
```

Run `python -m src.main --help` for all options.

## ✅ Tests

```bash
pytest -m "not integration"   # unit tests, fast, no browser
pytest -m integration         # integration tests, needs `playwright install`
```