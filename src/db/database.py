from typing import Iterable, List, Optional

from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from src.models import Quote

DATABASE_URL = "sqlite:///quotes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class QuoteRecord(Base):
    """Database representation of an extracted quote."""

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quote: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False, index=True)

    def to_pydantic(self) -> Quote:
        return Quote(quote=self.quote, author=self.author)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def save_quotes(quotes: Iterable[Quote], session: Optional[Session] = None) -> int:
    """Persist extracted quotes, skipping exact duplicates
    (same text + same author). Returns how many new records were saved.
    """
    owns_session = session is None
    session = session or SessionLocal()
    saved = 0

    try:
        for quote in quotes:
            exists = (
                session.query(QuoteRecord)
                .filter_by(quote=quote.quote, author=quote.author)
                .first()
            )
            if exists:
                continue

            session.add(QuoteRecord(quote=quote.quote, author=quote.author))
            saved += 1

        session.commit()
    finally:
        if owns_session:
            session.close()

    return saved


def list_quotes(
    author: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    session: Optional[Session] = None,
) -> List[QuoteRecord]:
    owns_session = session is None
    session = session or SessionLocal()

    try:
        query = session.query(QuoteRecord)
        if author:
            query = query.filter(QuoteRecord.author.ilike(f"%{author}%"))
        return query.offset(offset).limit(limit).all()
    finally:
        if owns_session:
            session.close()
