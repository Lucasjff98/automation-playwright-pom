from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes import router
from src.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Quotes Automation API",
    description=(
        "Exposes quotes collected by the Playwright scraper. "
        "Data is validated through the same Pydantic model used by the "
        "scraping pipeline, so what you get from the API is the same "
        "guarantee you get from the CLI."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}