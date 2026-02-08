from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, Enum

from .base import BaseModel
from app.enums import TransactionType
if TYPE_CHECKING:
    from .user import User
    from .category import Category
    from .saving import Saving

class Transaction(BaseModel):
    """
    The financial transaction model (income/expense).

The main entity for accounting of all financial transactions of the user.

    Fields:
        id (int): Unique Transaction Identifier (PK)
        user_id (int): User ID (FK → User.id )
        category_id (int): Category ID (FK → Category.id )
        saving_id (int, nullable): ID of the accumulation goal (FK → Saving.id )
        amount (int): Transaction amount in pennies/cents (always positive)
        date_time (datetime): Date and time of the transaction
        transaction_type (TransactionType): Type of financial transaction
        created_at (datetime): Date the record was created
    """
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    saving_id: Mapped[int | None] = mapped_column(
        ForeignKey("saving.id"),
        nullable=True
    )
    amount: Mapped[int] = mapped_column(Integer)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType)
    )

    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")
    saving: Mapped["Saving"] = relationship(back_populates="transactions")