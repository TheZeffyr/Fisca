from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CHAR, String, DateTime, func

from .base import BaseModel
if TYPE_CHECKING:
    from .user import User

class Currency(BaseModel):
    """
    The currency model for financial transactions.

    Stores information about supported currencies using the ISO 4217 standard.

    Fields:
        id (int): Unique Currency Identifier (PK)
        currency_code (str, 3 chars): Three-letter currency code (ISO 4217)
        name (str): Full name of the currency
        symbol (str, 1 char): Currency symbol (₽, $, €, etc.)
        created_at (datetime): Date the currency was added
    """
    currency_code: Mapped[str] = mapped_column(
        CHAR(3),
        unique=True,
        index=True,
        doc="Three-letter currency code according to ISO 4217"
    )
    name: Mapped[str] = mapped_column(
        String(50),
        doc="Full name of the currency"
    )
    symbol: Mapped[str] = mapped_column(
        CHAR(1),
        default="",
        doc="Currency symbol. For currencies without a symbol, an empty string."
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
    
    users: Mapped[list["User"]] = relationship(back_populates="currency")
