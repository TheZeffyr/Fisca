from datetime import datetime

from app.models import Currency
from app.repositories import BaseRepository


class CurrencyRepository(BaseRepository[Currency]):
    """Repository for Currency model operations.

    Inherits common CRUD operations from BaseRepository.

    Attributes:
        session: SQLAlchemy async session
    """

    def __init__(self, session):
        super().__init__(session, Currency)

    async def create(
        self,
        code: str,
        name: str,
        symbol: str,
        created_at: datetime | None = None,
    ) -> Currency:
        """
        Create a new currency.

        Args:
            code (str, 3 chars): Three-letter currency code (ISO 4217)
            name (str): Full name of the currency
            symbol (str, 1 char): Currency symbol (₽, $, €, etc.)
            created_at: Optional creation date. If None, database will set current date.

        Returns:
            Currency: Created Currency instance
        """
        return await self._create(
            code=code,
            name=name,
            symbol=symbol,
            created_at=created_at
        )

    async def get_by_code(self, code: str) -> Currency | None:
        """Get currency by ISO 4217 code.

        Args:
            code: Three-letter currency code (e.g., 'USD', 'EUR', 'RUB')

        Returns:
            Currency|None: Currency if found, None otherwise

        """
        return await self._get_by(code=code)

    async def update(
        self,
        currency_id: int,
        code: str | None,
        name: str | None,
        symbol: str | None,
    ) -> Currency | None:
        """Update currency information.

        Args:
            currency_id: ID of currency to update
            code: New currency code (if changing)
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
        if code is not None:
            if code != currency.code:
                update_data["code"] = code

        if name is not None:
            update_data["name"] = name
        if symbol is not None:
            update_data["symbol"] = symbol

        if not update_data:
            return currency

        return await self._update(currency, **update_data)

    async def delete(self, currency: Currency) -> None:
        """Delete a currency by ID (hard delete).

        Warning: Only use if currency has no associated transactions/users.
        Consider soft delete (deactivate) instead.

        Args:
            currency_id: ID of the currency to delete
        """
        await self._delete(currency)
