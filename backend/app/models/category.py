from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum
from app.enums import TransactionType

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction


class Category(BaseModel):
    """
    A category model for classifying transactions.

    Allows users to group transactions by type of expenses/income.

    Attributes:
        user_id (int | None): ID of the category owner. NULL means global category.
        name (str): Category name
        transaction_type (CategoryType): Operation type used category
    """
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        doc="ID of the category owner. NULL means global category."
    )
    name: Mapped[str] = mapped_column(
        String(100),
        doc="Category name"
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType),
        doc="Operation type used category"
    )

    user: Mapped["User"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
    )

