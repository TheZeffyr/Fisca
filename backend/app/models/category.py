from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey

from .base import BaseModel
if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction

class Category(BaseModel):
    """
    A category model for classifying transactions.

    Allows users to group transactions by type of expenses/income.

    Fields:
        id (int): Unique category identifier (PK)
        user_id (int): ID of the category owner (FK → User.id )
        name (str): Category name (for example, "Food", "Transport")
        type (CategoryType): Category type
        created_at (datetime): Date the category was created
    """
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id"),
        nullable=True
    )
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
    )

