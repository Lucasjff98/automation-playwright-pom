from typing import List

from playwright.sync_api import Page

from src.models import Quote
from src.pages.base_page import BasePage


class QuotesPage(BasePage):
    URL = "https://quotes.toscrape.com/"

    # Page Selectors
    QUOTE_CARD = ".quote"
    TEXT = ".text"
    AUTHOR = ".author"
    NEXT_BUTTON = "li.next > a"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def navigate(self) -> None:
        self.page.goto(self.URL)
        self.wait_for_quotes_to_load()

    def wait_for_quotes_to_load(self, timeout: int = 5000) -> None:
        """Ensures the current page's quote cards have rendered before we
        try to extract data — avoids scraping an empty page right after a
        navigation/pagination action.
        """
        self.page.locator(self.QUOTE_CARD).first.wait_for(state="visible", timeout=timeout)

    def scrape_current_page_quotes(self) -> List[Quote]:
        """Extract every quote on the current page using the Locator API.

        Locators re-query the DOM on every action and auto-wait for the
        element to be actionable, which makes this far less prone to
        flakiness than caching element handles from `query_selector`.
        """
        quotes_data = []
        cards = self.page.locator(self.QUOTE_CARD)
        count = cards.count()

        for i in range(count):
            card = cards.nth(i)
            text = card.locator(self.TEXT).inner_text()
            author = card.locator(self.AUTHOR).inner_text()
            quotes_data.append(Quote(quote=text, author=author))

        return quotes_data

    def has_next_page(self) -> bool:
        return self.page.locator(self.NEXT_BUTTON).is_visible()

    def go_to_next_page(self) -> None:
        self.safe_click(self.NEXT_BUTTON)
        self.wait_for_quotes_to_load()
