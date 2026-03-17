from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, CheckConstraint, Date, Numeric

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Transaction


class Saving(BaseModel):


    name: Mapped[str] = mapped_column(
        String(100),
        doc="Name of the savings goal"
    )
    target_amount: Mapped[int] = mapped_column(
        Numeric(10,2),
        doc="Target amount to save"
    )
    current_amount: ...
    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Optional target date to achieve the goal"
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        doc="ID of the user who owns this savings goal"
    )
    is_completed: Mapped[bool] = mapped_column(
        default=False,
        doc="Whether the goal has been achieved"
    )
    
    user: Mapped["User"] = relationship(back_populates="savings")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="saving"
    )
    
    __table_args__ = (
        CheckConstraint(
            "target_amount > 0",
            name='check_final_amount_positive'
        ),
        CheckConstraint(
            "name IS NOT NULL AND trim(name) != ''",
            name='check_name_not_empty'
        ),
        CheckConstraint(
            "end_date IS NULL OR end_date >= CURRENT_DATE",
            name='check_end_date_not_past'
        )
    )
