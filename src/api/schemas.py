from typing import List

from pydantic import BaseModel, ConfigDict

from src.models import Quote


class QuoteResponse(Quote):
    """Same validation as Quote, plus the database id."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class QuoteListResponse(BaseModel):
    total: int
    items: List[QuoteResponse]


class ScrapeResponse(BaseModel):
    scraped: int
    saved: int
    message: str