from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, CheckConstraint

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction


class Saving(BaseModel):
    """
    The model of the accumulation goal (piggy bank).

    Allows users to set financial goals and track progress.

    Attributes:
        user_id (int): ID of the user who owns this savings goal
        name (str): Name of the savings goal
        final_amount (int): Target amount to save
        deadline (datetime, nullable): Optional target date to achieve the goal
        is_completed (bool): Whether the goal has been achieved
    """

    __table_args__ = (
        CheckConstraint('target_amount > 0', name='check_target_amount_positive'),
        CheckConstraint('current_amount >= 0', name='check_current_amount_non_negative'),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        doc="ID of the user who owns this savings goal"
    )
    name: Mapped[str] = mapped_column(
        String(100),
        doc="Name of the savings goal"
    )
    final_amount: Mapped[int] = mapped_column(
        doc="Target amount to save"
    )
    deadline: Mapped[datetime | None] = mapped_column(
        nullable=True,
        doc="Optional target date to achieve the goal"
    )
    is_completed: Mapped[bool] = mapped_column(
        default=False,
        doc="Whether the goal has been achieved"
    )

    user: Mapped["User"] = relationship(back_populates="savings")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="saving"
    )
