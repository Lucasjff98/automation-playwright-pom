from fastapi import APIRouter, Query

from src.api.schemas import QuoteListResponse, QuoteResponse, ScrapeResponse
from src.db import database
from src.scraper.runner import run_scraper

router = APIRouter()


@router.get("/quotes", response_model=QuoteListResponse)
def get_quotes(
    author: str | None = Query(default=None, description="Filter by author (partial match)"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """List quotes stored in the database, with optional author filtering
    and pagination.
    """
    session = database.SessionLocal()
    try:
        records = database.list_quotes(author=author, limit=limit, offset=offset, session=session)
        return QuoteListResponse(
            total=len(records),
            items=[QuoteResponse(id=r.id, quote=r.quote, author=r.author) for r in records],
        )
    finally:
        session.close()


@router.post("/scrape", response_model=ScrapeResponse)
def trigger_scrape(max_pages: int = Query(default=3, ge=1, le=20)):
    """Run the scraper synchronously and persist any new quotes found.

    Runs headless and blocks until finished — fine for a portfolio demo,
    but in a production setting this should be a background job instead
    of a request-blocking call.
    """
    quotes = run_scraper(headless=True, max_pages=max_pages)
    saved = database.save_quotes(quotes)

    return ScrapeResponse(
        scraped=len(quotes),
        saved=saved,
        message=f"Scraped {len(quotes)} quotes, {saved} new records saved.",
    )