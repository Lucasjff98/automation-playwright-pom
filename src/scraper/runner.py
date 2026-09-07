import os
from typing import List

from playwright.sync_api import sync_playwright

from src.models import Quote
from src.pages.quotes_page import QuotesPage


def run_scraper(
    headless: bool = True,
    max_pages: int = 3,
    slow_mo: int = 0,
    trace_path: str = "artifacts/trace.zip",
) -> List[Quote]:
    """Run the scraping pipeline and return the extracted quotes.

    This function does not persist or save anything — it only collects and
    returns data. Callers decide what to do with the result (write it to
    JSON, store it in a database, etc.), keeping extraction decoupled from
    the destination.
    """
    all_quotes: List[Quote] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        quotes_page = QuotesPage(page)

        try:
            quotes_page.navigate()

            page_count = 1
            while True:
                quotes = quotes_page.scrape_current_page_quotes()
                all_quotes.extend(quotes)

                if quotes_page.has_next_page() and page_count < max_pages:
                    quotes_page.go_to_next_page()
                    page_count += 1
                else:
                    break
        finally:
            trace_dir = os.path.dirname(trace_path) or "."
            os.makedirs(trace_dir, exist_ok=True)
            context.tracing.stop(path=trace_path)
            browser.close()

    return all_quotes
