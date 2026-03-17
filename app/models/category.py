from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    ForeignKey,
    Enum,
    UniqueConstraint,
    CheckConstraint
)

from app.enums import TransactionType
from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Transaction


class Category(BaseModel):
    """A category model for classifying transactions.

    Allows users to group transactions by type of expenses/income.

    Attributes:
        user_id (int | None): ID of the category owner. NULL means global category.
        name (str): Category name
        transaction_type (CategoryType): Operation type used category
    """

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
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

    __table_args__ = (
        UniqueConstraint(
            "user_id", "name", "transaction_type", 
            name="uq_user_category_name_type"
        ),
        CheckConstraint(
            "LENGTH(TRIM(name)) > 0", 
            name="check_category_name_not_empty"
        )
    )
