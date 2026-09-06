from typing import List
from playwright.sync_api import Page
from src.pages.base_page import BasePage
from src.models import Quote


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
        """Garante que os cards de citação da página atual já renderizaram
        antes de tentar extrair dados — evita raspar uma página ainda vazia
        logo após uma navegação/paginação."""
        self.page.wait_for_selector(self.QUOTE_CARD, state="visible", timeout=timeout)

    def scrape_current_page_quotes(self) -> List[Quote]:
        quotes_data = []
        cards = self.page.query_selector_all(self.QUOTE_CARD)

        for card in cards:
            text_el = card.query_selector(self.TEXT)
            author_el = card.query_selector(self.AUTHOR)

            if text_el and author_el:
                quotes_data.append(
                    Quote(quote=text_el.inner_text(), author=author_el.inner_text())
                )
        return quotes_data

    def has_next_page(self) -> bool:
        return self.page.is_visible(self.NEXT_BUTTON)

    def go_to_next_page(self) -> None:
        self.safe_click(self.NEXT_BUTTON)
        self.wait_for_quotes_to_load()