from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    ForeignKey,
    Enum,
    CheckConstraint,
    UniqueConstraint
)

from app.enums import TransactionType
from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Transaction


class Category(BaseModel):
    """Category to classify transactions.
    
    Allows you to group transactions by types (revenue/expense) and themes.
    Categories can be as personal (belong to a particular user),
    also general (user_id = NULL), accessible to all users.
    
    Attributes:
        user_id (int | None): Category owner user ID. If NULL - the category is shared by all users.
        name (str): Category name.
        transaction_type (TransactionType): Category transaction type.Determines which transactions fall into this category.
        user (User | None): A connection to the owner user. If category is general, value None.
        transactions (list[Transaction]): A list of transactions that are categorized.
    """

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Category owner user ID.\
        If NULL - the category is shared by all users."
    )
    name: Mapped[str] = mapped_column(
        String(100),
        doc="Category name."
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType),
        doc="Category transaction type. \
        Determines which transactions fall into this category."
    )

    user: Mapped["User"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
    )

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_category_name_not_empty"
        ),
        UniqueConstraint(
            "user_id", "name",
            name="uq_user_category_name"
        )
    )
