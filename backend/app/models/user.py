from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, BigInteger, DateTime, ForeignKey

from .base import BaseModel
if TYPE_CHECKING:
    from.currency import Currency
    from .saving import Saving
    from .category import Category
    from .transaction import Transaction

class User(BaseModel):
    """
    The user model.

    Represents the bot user, stores basic information and settings.

    Fields:
        id (int): Unique User Identifier (PK)
        tg_id (int): Telegram User ID (unique)
        currency_id (int, nullable): Default currency ID (FK → Currency.id)
        created_at (datetime): Date and time of registration (automatically)
    """
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    currency: Mapped["Currency"] = relationship(back_populates="users")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")
    savings: Mapped[list["Saving"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")
