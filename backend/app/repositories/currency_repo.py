from datetime import datetime

from app.models import Currency
from .base_repo import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    """
    Repository for Currency model operations.

    Inherits common CRUD operations from BaseRepository.

    Attributes:
        session: SQLAlchemy async session
    """

    def __init__(self, session):
        super().__init__(session, Currency)

    async def create(
        self,
        currency_code: str,
        name: str,
        symbol: str,
        created_at: datetime | None = None,
    ) -> Currency:
        """
        Create a new currency.

        Args:
            currency_code (str, 3 chars): Three-letter currency code (ISO 4217)
            name (str): Full name of the currency
            symbol (str, 1 char): Currency symbol (₽, $, €, etc.)
            created_at: Optional creation date. If None, database will set current date.

        Returns:
            Currency: Created Currency instance
        """
        return await self._create(
            currency_code=currency_code, name=name, symbol=symbol, created_at=created_at
        )

    async def update(
        self,
        currency_id: int,
        currency_code: str | None,
        name: str | None,
        symbol: str | None,
    ) -> Currency | None:
        """Update currency information.

        Args:
            currency_id: ID of currency to update
            currency_code: New currency code (if changing)
            name: New currency name (if changing)
            symbol: New currency symbol (if changing)
            is_active: New active status (if changing)

        Returns:
            Currency|None: Updated currency if found, None otherwise
        """
        currency = await self.get_by_id(currency_id)
        if not currency:
            return None

        update_data = {}
        if currency_code is not None:
            if currency_code != currency.currency_code:
                update_data["currency_code"] = currency_code

        if name is not None:
            update_data["name"] = name
        if symbol is not None:
            update_data["symbol"] = symbol

        if not update_data:
            return currency

        return await self._update(currency, **update_data)

    async def get_by_currency_code(self, currency_code: str) -> Currency | None:
        """Get currency by ISO 4217 code.

        Args:
            currency_code: Three-letter currency code (e.g., 'USD', 'EUR', 'RUB')

        Returns:
            Currency|None: Currency if found, None otherwise

        """
        return await self._get_by(currency_code=currency_code)

    async def delete(self, currency_id: int) -> bool:
        """Delete a currency by ID (hard delete).

        Warning: Only use if currency has no associated transactions/users.
        Consider soft delete (deactivate) instead.

        Args:
            currency_id: ID of the currency to delete

        Returns:
            bool: True if deleted, False if not found
        """
        currency = await self.get_by_id(currency_id)

        if not currency:
            return False

        await self._delete(currency)
        return True
