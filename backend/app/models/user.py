from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey

from .base import BaseModel

if TYPE_CHECKING:
    from .currency import Currency
    from .saving import Saving
    from .category import Category
    from .transaction import Transaction


class User(BaseModel):
    """User model representing a Telegram bot user.

    Attributes:
        tg_id (int): Telegram User ID (unique)
        currency_id (int): User’s currency id
    """

    tg_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, doc="Telegram user ID from Telegram API"
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT"), doc="IUser’s currency id"
    )

    currency: Mapped["Currency"] = relationship(back_populates="users")
    categories: Mapped[list["Category"]] = relationship(back_populates="users")
    savings: Mapped[list["Saving"]] = relationship(back_populates="users")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="users")
