from typing import List, Dict
from playwright.sync_api import Page
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

    def scrape_current_page_quotes(self) -> List[Dict[str, str]]:
        quotes_data = []
        cards = self.page.query_selector_all(self.QUOTE_CARD)

        for card in cards:
            text_el = card.query_selector(self.TEXT)
            author_el = card.query_selector(self.AUTHOR)

            if text_el and author_el:
                quotes_data.append({
                    "quote": text_el.inner_text().strip("”").strip("“"),
                    "author": author_el.inner_text().strip(),
                })
        return quotes_data

    def has_next_page(self) -> bool:
        return self.page.is_visible(self.NEXT_BUTTON)

    def go_to_next_page(self) -> None:
        self.safe_click(self.NEXT_BUTTON)