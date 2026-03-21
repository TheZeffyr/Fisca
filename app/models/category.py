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
    """
    """

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc=""
    )
    name: Mapped[str] = mapped_column(
        String(100),
        doc=""
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType),
        doc=""
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
