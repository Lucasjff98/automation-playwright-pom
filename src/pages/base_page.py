import os
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import structlog

logger = structlog.get_logger()


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def safe_click(self, selector: str, timeout: int = 5000) -> None:
        """Clicks an element ensuring visibility and explicit wait handling."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            self.page.click(selector)
            logger.info("click_executed", selector=selector)
        except PlaywrightTimeoutError:
            logger.error("click_timeout", selector=selector)
            self.capture_failure_artifact("click_failed")
            raise

    def capture_failure_artifact(self, name_prefix: str) -> str:
        """Generates a failure screenshot when an unexpected exception occurs."""
        os.makedirs("artifacts", exist_ok=True)
        path = f"artifacts/{name_prefix}_error.png"
        self.page.screenshot(path=path, full_page=True)
        logger.info("artifact_saved", path=path)
        return path