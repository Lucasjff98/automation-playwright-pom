import argparse
import json
import os
from playwright.sync_api import sync_playwright
from src.pages.quotes_page import QuotesPage


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pipeline de automação/extração de dados com Playwright."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Roda o navegador em modo headless (sem interface gráfica).",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=3,
        help="Número máximo de páginas a percorrer (padrão: 3).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/quotes.json",
        help="Caminho do arquivo JSON de saída (padrão: output/quotes.json).",
    )
    parser.add_argument(
        "--slow-mo",
        type=int,
        default=0,
        help="Atraso em ms entre ações do Playwright, útil para debug visual (padrão: 0).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("🚀 Starting Web Automation Pipeline...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless, slow_mo=args.slow_mo)
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

                if quotes_page.has_next_page() and page_count < args.max_pages:
                    print("➡️ Navigating to next page...")
                    quotes_page.go_to_next_page()
                    page_count += 1
                else:
                    break

            output_dir = os.path.dirname(args.output) or "."
            os.makedirs(output_dir, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(
                    [q.model_dump() for q in all_quotes],
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

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
