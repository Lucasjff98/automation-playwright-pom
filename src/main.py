import json
import os
from playwright.sync_api import sync_playwright
from src.pages.quotes_page import QuotesPage


def main():
    print("🚀 Starting Web Automation Pipeline...")

    with sync_playwright() as p:
        # Launching browser (set headless=True for background execution)
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        quotes_page = QuotesPage(page)

        all_quotes = []

        try:
            print("🌐 Navigating to target website...")
            quotes_page.navigate()

            page_count = 1
            while True:
                print(f"📄 Scraping data from page {page_count}...")
                quotes = quotes_page.scrape_current_page_quotes()
                all_quotes.extend(quotes)
                print(f"   -> {len(quotes)} quotes extracted from current page.")

                if quotes_page.has_next_page() and page_count < 3:
                    print("➡️ Navigating to next page...")
                    quotes_page.go_to_next_page()
                    page_count += 1
                else:
                    break

            os.makedirs("output", exist_ok=True)
            with open("output/quotes.json", "w", encoding="utf-8") as f:
                json.dump(all_quotes, f, ensure_ascii=False, indent=2)

            print(
                f"✅ Pipeline completed successfully! Total records saved: {len(all_quotes)}"
            )

        except Exception as e:
            print(f"❌ Execution error: {e}")
        finally:
            os.makedirs("artifacts", exist_ok=True)
            context.tracing.stop(path="artifacts/trace.zip")
            browser.close()
            print("🔒 Browser closed. Trace artifacts saved to artifacts/trace.zip")


if __name__ == "__main__":
    main()