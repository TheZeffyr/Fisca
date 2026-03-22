from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import (
        Currency,
        Category,
        Transaction,
        Account
    )


class User(BaseModel):
    """The Telegram Bot user.
    
    Stores information about the Telegram user, its settings and links to all its data: categories, accounts, and transactions.
    
    Attributes:
        tg_id: Telegram unique user ID
        currency_id: Default currency ID for user
        currency: Link to the Currency model 
        categories: List of user categories (expenses/revenue)
        accounts: User’s list of accounts (cash, cards, savings)
        transactions: A list of all user transactions
    """

    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        doc="Telegram unique user ID"
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT"),
        doc="User’s currency"
    )

    currency: Mapped["Currency"] = relationship(back_populates="users")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")
    accounts: Mapped[list["Account"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user"
    )
