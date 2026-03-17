from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CHAR, String

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User


class Currency(BaseModel):
    """The currency model for financial transactions

    Stores information about supported currencies using the ISO 4217 standard.

    Attributes:
        code (str, 3 chars): Three-letter currency code according to ISO 4217.
        name (str): Full name of the currency.
        symbol (str, 1 char): Currency symbol. For currencies without a symbol, an empty string.
    """

    code: Mapped[str] = mapped_column(
        CHAR(3),
        unique=True,
        doc="Three-letter currency code according to ISO 4217"
    )
    name: Mapped[str] = mapped_column(
        String(50),
        doc="Full name of the currency"
    )
    symbol: Mapped[str] = mapped_column(
        CHAR(1),
        nullable=True,
        doc="Currency symbol. " \
        "For currencies without a symbol, an empty string."
    )

    users: Mapped[list["User"]] = relationship(back_populates="currency")
