from datetime import date as date_type
from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
	Numeric,
	Date,
    String,
	ForeignKey,
	CheckConstraint
)

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Category, Account


class Transaction(BaseModel):
    """Financial transaction of the user.
    
    Represents cash flow: expenditure, income or transfer between accounts.
    Each transaction is linked to a user and can be associated with a category
    (for expenses and revenues) and accounts (for all types).
    
    Transaction types are determined by the existence of accounts:
    - Expense: from_account_id specified, to_account_id = NULL
    - Revenue: to_account_id, from_account_id = NULL
    - Translation: both invoices (from and to) are specified
    
    Attributes:
        amount (Decimal): The sum of the transaction.
        date (date): The date when the transaction occurred. This field is required for reports and sorting.
        note (str | None): A note to the transaction.
        from_account_id (int | None): ID of the write-off account. For expenses and transfers. If null, transaction is revenue.
        to_account_id (int | None): ID of account entry. For revenue and transfers. If null, the transaction is an expense.
        user_id (int): ID of transaction owner user.
        category_id (int | None): ID of transaction category.
        from_account (Account | None): Write-off account.
        to_account (Account | None): A credit score.
        user (User): The transaction owner.
        category (Category | None): Transaction category.
    """
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        doc="The sum of the transaction."
    )
    date: Mapped[date_type] = mapped_column(
        Date,
        index=True,
        doc="The date when the transaction occurred."
    )
    note: Mapped[str | None] = mapped_column(
        String(200),
        doc="A note to the transaction."
	)
    from_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        doc="ID of the write-off account."
	)
    to_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        doc="ID of account entry."
	)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        doc="ID of transaction owner user."
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        doc="ID of transaction category."
    )
    
    from_account: Mapped["Account"] = relationship(
        foreign_keys=[from_account_id],
        back_populates="expenses"
    )
    to_account: Mapped["Account"] = relationship(
        foreign_keys=[to_account_id],
        back_populates="incomes"
    )
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="check_amount_positive"
        ),
        CheckConstraint(
            "(from_account_id IS NOT NULL) OR (to_account_id IS NOT NULL)",
            name="check_at_least_one_account"
        ),
        CheckConstraint(
            "from_account_id != to_account_id OR from_account_id IS NULL OR to_account_id IS NULL",
            name="check_different_accounts"
        )
    )
