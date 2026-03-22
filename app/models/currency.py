from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CHAR, String, CheckConstraint

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User


class Currency(BaseModel):
    """Currency for financial transactions.
    
    Stores information about the currencies available in the system (for example, RUB, USD, EUR).
    Used to display amounts in accounts and transactions in the user’s currency.
    
    Attributes:
        code (str): The three-letter currency code according to ISO 4217 (RUB, USD, EUR).
        name (str): Full name of the currency in Russian.
        symbol (str): The currency symbol (₽, $, €).
        users (list[User]): A list of users using this currency.
    """

    code: Mapped[str] = mapped_column(
        CHAR(3),
        unique=True,
        doc="The three-letter currency code according\
        to ISO 4217 (RUB, USD, EUR)."
    )
    name: Mapped[str] = mapped_column(
        String(50),
        doc="Full name of the currency in Russian."
    )
    symbol: Mapped[str] = mapped_column(
        CHAR(1),
        doc="The currency symbol (₽, $, €)."
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
