import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.db import database
from src.db.database import Base, QuoteRecord


@pytest.fixture(autouse=True)
def use_in_memory_db(monkeypatch):
    """Points the app at an isolated in-memory SQLite database for each
    test, so tests never touch the real quotes.db file.

    StaticPool forces every connection in the pool to reuse the same
    underlying SQLite connection — without it, each new connection would
    open a *separate* in-memory database, and tables created by
    `create_all()` would vanish on the very next query.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_quotes_empty(client):
    response = client.get("/quotes")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 0
    assert body["items"] == []


def test_get_quotes_returns_seeded_data(client):
    session = database.SessionLocal()
    session.add(QuoteRecord(quote="Stay hungry, stay foolish.", author="Steve Jobs"))
    session.add(QuoteRecord(quote="Simplicity is the soul of efficiency.", author="Austin Freeman"))
    session.commit()
    session.close()

    response = client.get("/quotes")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2


def test_get_quotes_filters_by_author(client):
    session = database.SessionLocal()
    session.add(QuoteRecord(quote="A quote.", author="Ada Lovelace"))
    session.add(QuoteRecord(quote="Another quote.", author="Alan Turing"))
    session.commit()
    session.close()

    response = client.get("/quotes", params={"author": "Ada"})
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["author"] == "Ada Lovelace"