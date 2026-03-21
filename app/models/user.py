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
    """
    """

    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        doc=""
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT"),
        doc=""
    )

    currency: Mapped["Currency"] = relationship(back_populates="users")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")
    accounts: Mapped[list["Account"]] = relationship(back_populates="user")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user"
    )
