from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CHAR, String, CheckConstraint

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User


class Currency(BaseModel):
    """
    """

    code: Mapped[str] = mapped_column(
        CHAR(3),
        unique=True,
        doc=""
    )
    name: Mapped[str] = mapped_column(
        String(50),
        doc=""
    )
    symbol: Mapped[str] = mapped_column(
        CHAR(1),
        doc=""
    )

    users: Mapped[list["User"]] = relationship(back_populates="currency")
    
    __table_args__ = (
        CheckConstraint(
            "length(trim(code)) > 0",
            name="check_currency_code_not_empty"
        ),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_currency_name_not_empty"
        ),
        CheckConstraint(
            "length(trim(symbol)) > 0",
            name="check_currency_symbol_not_empty"
        )
    )
