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
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        doc=""
    )
    date: Mapped[date_type] = mapped_column(
        Date,
        index=True,
        doc=""
    )
    note: Mapped[str | None] = mapped_column(
        String(200),
        doc=""
	)
    from_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        doc=""
	)
    to_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        doc=""
	)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        doc=""
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        doc=""
    )
    
    from_account: Mapped["Account"] = relationship(
        foreign_keys=[from_account_id],
        back_populates="expenses"  # ✅ expenses, не from_account_id
    )
    to_account: Mapped["Account"] = relationship(
        foreign_keys=[to_account_id],
        back_populates="incomes"  # ✅ incomes, не to_account_id
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
