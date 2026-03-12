from datetime import date as date_type
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, ForeignKey, Enum, CheckConstraint, Index

from app.enums import TransactionType

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .saving import Saving


class Transaction(BaseModel):
    """
    The financial transaction model (income/expense).

    The main entity for accounting of all financial transactions of the user.

    Attributes:
        user_id (int): ID of the transaction owner.
        category_id (int): ID of the transaction category.
        saving_id (int, nullable): ID of the associated saving goal. For expense transactions - source saving. For income transactions - target saving.
        amount (int): Transaction size.
        date (date): Transaction date.
        transaction_type (TransactionType): Type: income (money in), expense (money out).
    """

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
        CheckConstraint(
            "transaction_type IN ('income', 'expense')",
            name="check_transaction_type_valid",
        ),
        CheckConstraint(
            """
            (saving_id IS NULL AND category_id IS NOT NULL)
            OR
            (saving_id IS NOT NULL AND category_id IS NULL)
            """,
            name="check_category_saving_consistency",
        ),
        Index("idx_transactions_user_date", "user_id", "date"),
        Index("idx_transactions_type", "transaction_type"),
        Index("idx_transactions_saving", "saving_id"),
        Index("idx_transactions_category", "category_id"),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), doc="ID of the transaction owner."
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        doc="ID of the transaction category.",
    )
    saving_id: Mapped[int | None] = mapped_column(
        ForeignKey("savings.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="ID of the associated saving goal. For expense transactions - source saving. For income transactions - target saving.",
    )
    amount: Mapped[int] = mapped_column(Integer, doc="Transaction size.")

    date: Mapped[date_type] = mapped_column(Date, index=True, doc="Transaction date.")

    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), doc="Type: income (money in), expense (money out)."
    )

    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")
    saving: Mapped["Saving"] = relationship(back_populates="transactions")
