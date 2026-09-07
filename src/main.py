import argparse
import json
import os

from src.db.database import init_db, save_quotes
from src.scraper.runner import run_scraper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automation/data-extraction pipeline powered by Playwright."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the browser in headless mode (no GUI).",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=3,
        help="Maximum number of pages to walk through (default: 3).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/quotes.json",
        help="Path to the output JSON file (default: output/quotes.json).",
    )
    parser.add_argument(
        "--slow-mo",
        type=int,
        default=0,
        help="Delay in ms between Playwright actions, useful for visual debugging (default: 0).",
    )
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Skip saving results to the database (JSON output only).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("🚀 Starting Web Automation Pipeline...")

    print("🌐 Running scraper...")
    quotes = run_scraper(
        headless=args.headless,
        max_pages=args.max_pages,
        slow_mo=args.slow_mo,
    )
    print(f"   -> {len(quotes)} quotes extracted in total.")

    output_dir = os.path.dirname(args.output) or "."
    os.makedirs(output_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump([q.model_dump() for q in quotes], f, ensure_ascii=False, indent=2)
    print(f"📄 JSON output written to {args.output}")

    if not args.no_db:
        init_db()
        saved = save_quotes(quotes)
        print(f"💾 {saved} new records saved to the database.")

    print("✅ Pipeline completed successfully!")


if __name__ == "__main__":
    main()
