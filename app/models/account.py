from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import date



from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, Date, ForeignKey, CheckConstraint, Enum, select, func, cast
from sqlalchemy.ext.hybrid import hybrid_property

from app.models import BaseModel
from app.enums import AccountType


if TYPE_CHECKING:
    from app.models import User, Transaction


class Account(BaseModel):
    name: Mapped[str] = mapped_column(
        String(100),
        doc=""
    )
    type: Mapped[AccountType] = mapped_column(
        Enum(AccountType),
        doc=""
	)
    target_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10,2),
        nullable=True,
        doc=""
	)
    
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc=""
    )
    is_completed: Mapped[bool | None] = mapped_column(
        default=False,
        nullable=True,
        doc=""
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        doc=""
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        default=0,
        doc=""
    )
    @hybrid_property
    def calc_balance(self) -> Decimal:#type: ignore
        income_sum = sum(t.amount for t in self.incomes)
        expense_sum = sum(t.amount for t in self.expenses)
        
        return Decimal(str(income_sum - expense_sum))

    
    @calc_balance.expression
    def calc_balance(cls):
        from app.models import Transaction
        income_sum = select(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(
            Transaction.to_account_id == cls.id
        ).scalar_subquery()
        
        expense_sum = select(
            func.coalesce(func.sum(Transaction.amount), 0)
        ).where(
            Transaction.from_account_id == cls.id
        ).scalar_subquery()
        
        return cast(income_sum - expense_sum, Numeric(10, 2))

    incomes: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        primaryjoin="Transaction.to_account_id == Account.id",
        back_populates="to_account",
        lazy="selectin",
        viewonly=True
    )
    
    expenses: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        primaryjoin="Transaction.from_account_id == Account.id",
        back_populates="from_account",
        lazy="selectin",
        viewonly=True
    )
    
    user: Mapped["User"] = relationship(back_populates="accounts")

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_account_name_not_empty"
        ),
        CheckConstraint(
            "target_amount IS NULL OR target_amount > 0",
            name="check_target_amount_positive"
        ),
        CheckConstraint(
            "balance >= 0",
            name="check_balance_non_negative"
        ),     
        CheckConstraint(
            "(type != 'SAVINGS' AND target_amount IS NULL) OR "
            "(type = 'SAVINGS')",
            name="check_target_amount_only_for_savings"
        ),
        
        CheckConstraint(
            "(type != 'SAVINGS' AND end_date IS NULL) OR "
            "(type = 'SAVINGS')",
            name="check_end_date_only_for_savings"
        ),
        CheckConstraint(
            "(type != 'SAVINGS' AND is_completed = False) OR "
            "(type = 'SAVINGS')",
            name="check_is_completed_only_for_savings"
        )
    )

