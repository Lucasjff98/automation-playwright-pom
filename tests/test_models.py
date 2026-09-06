import pytest
from pydantic import ValidationError

from src.models import Quote


def test_quote_strips_curly_quotes():
    quote = Quote(quote="“The world is a stage.”", author="  Shakespeare  ")
    assert quote.quote == "The world is a stage."
    assert quote.author == "Shakespeare"


def test_quote_rejects_empty_text():
    with pytest.raises(ValidationError):
        Quote(quote="   ", author="Someone")


def test_quote_rejects_empty_author():
    with pytest.raises(ValidationError):
        Quote(quote="Something wise", author="")
