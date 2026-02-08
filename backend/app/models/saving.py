from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, func

from .base import BaseModel
if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction

class Saving(BaseModel):
    """
    The model of the accumulation goal (piggy bank).

    Allows users to set financial goals and track progress.

    Fields:
        id (int): Unique goal identifier (PK)
        user_id (int): ID of the goal owner (FK → User.id )
        name (str): The name of the goal (for example, "For vacation", "For a car")
        final_amount (int): Target amount in pennies/cents
        description (str, nullable): Detailed description of the goal
        deadline (datetime, nullable): The planned goal completion date
        created_at (datetime): Goal creation date
    """
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(100))
    final_amount: Mapped[int] = mapped_column()
    deadline: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="savings")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="saving")
