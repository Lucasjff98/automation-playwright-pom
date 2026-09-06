from pydantic import BaseModel, field_validator


class Quote(BaseModel):
    """Registro validado de uma citação extraída."""

    quote: str
    author: str

    @field_validator("quote")
    @classmethod
    def strip_curly_quotes(cls, value: str) -> str:
        return value.strip("\u201c\u201d").strip()

    @field_validator("quote", "author")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("campo não pode ser vazio")
        return value.strip()
