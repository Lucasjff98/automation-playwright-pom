import pytest
from playwright.sync_api import Page

from src.pages.quotes_page import QuotesPage


@pytest.mark.integration
def test_scrape_first_page_returns_ten_quotes(page: Page):
    quotes_page = QuotesPage(page)
    quotes_page.navigate()

    quotes = quotes_page.scrape_current_page_quotes()

    assert len(quotes) == 10
    assert all(q.quote and q.author for q in quotes)


@pytest.mark.integration
def test_has_next_page_on_first_page(page: Page):
    quotes_page = QuotesPage(page)
    quotes_page.navigate()

    assert quotes_page.has_next_page() is True
