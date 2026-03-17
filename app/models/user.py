from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, CheckConstraint

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import (
        Currency,
        Category,
        Transaction,
        Account
    )


class User(BaseModel):
    """User model representing a Telegram bot user.
    
    This model stores users who interact with the bot via Telegram. Each user has their own isolated data: categories, accounts, transactions. All financial operations are scoped to the user.
    
    Attributes:
        tg_id (int): Telegram user ID from Telegram API (unique)
        currency_id (int): IUser’s currency id

    Relationships:
        currency: User's preferred currency
        categories: User's expense/income categories
        accounts: User's financial accounts
        transactions: User's financial operations
    """

    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        doc="Telegram user ID from Telegram API"
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT"),
        doc="IUser’s currency id"
    )

    currency: Mapped["Currency"] = relationship(back_populates="users")
    categories: Mapped[list["Category"]] = relationship(back_populates="users")
    accounts: Mapped[list["Account"]] = relationship(back_populates="users")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="users"
    )

    __table_args__ = (
        CheckConstraint('currency_id > 0', name='check_currency_id_positive'),
    )
