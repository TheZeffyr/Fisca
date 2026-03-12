import logging
from datetime import datetime

from app.repositories import UserRepository, CurrencyRepository
from app.schemas.currency import CurrencyDTO
from exceptions.user import UserNotFoundError
from exceptions.currency import CurrencyNotFoundError, CurrencyAlreadyExistsError

logger = logging.getLogger(__name__)


class CurrencyService:
    """Service for currency-related business logic.

    This service handles all operations related to currencies:
    - Creating new currencies (admin functionality)
    - Retrieving currency information by ID or code
    - Updating currency details
    - Deleting currencies (with caution)

    Currencies are typically static and rarely change. Most operations
    are reads. Creation/update/delete should be restricted to admins.

    Attributes:
        session: SQLAlchemy async session
        repository: CurrencyRepository for currency operations
    """

    async def __init__(self, session):
        self.session = session
        self.repository = CurrencyRepository(session)

    async def create(
        self,
        currency_code: str,
        name: str,
        symbol: str,
        created_at: datetime | None = None,
    ) -> CurrencyDTO:
        """Create a new currency.

        This method creates a new currency record. Currency codes must be
        unique according to ISO 4217 standard.

        Args:
            currency_code: Three-letter ISO 4217 currency code (e.g., 'USD', 'EUR', 'RUB')
            name: Full currency name (e.g., 'US Dollar', 'Euro', 'Russian Ruble')
            symbol: Currency symbol (e.g., '$', '€', '₽')
            created_at: Optional creation timestamp. If None, database sets current time.

        Returns:
            CurrencyDTO: Created currency data

        Raises:
            CurrencyAlreadyExistsError: If currency with given code already exists
            ValueError: If currency_code is not 3 characters or contains invalid chars

        Example:
            >>> # Create a new currency
            >>> usd = await currency_service.create(
            ...     currency_code="USD",
            ...     name="US Dollar",
            ...     symbol="$"
            ... )
            >>> print(f"Created currency: {usd.currency_code}")
        """
        existing = await self.repository.get_by_currency_code(currency_code)
        if existing:
            logger.warning(
                f"Attempt to create duplicate currency: code={currency_code}"
            )
            raise CurrencyAlreadyExistsError()

        currency = await self.repository.create(
            currency_code=currency_code, name=name, symbol=symbol, created_at=created_at
        )

        await self.session.commit()
        logger.info(
            f"Currency created successfully:\
                    id={currency.id}, currency_code={currency.currency_code},name={currency.name}, symbol={currency.symbol}"
        )
        return CurrencyDTO.model_validate(currency)

    async def get_by_id(self, currency_id: int) -> CurrencyDTO:
        """Get currency by its ID.

        Args:
            currency_id: ID of the currency to retrieve

        Returns:
            CurrencyDTO: Currency data

        Raises:
            CurrencyNotFoundError: If currency with given ID doesn't exist

        Example:
            >>> try:
            ...     currency = await currency_service.get_by_id(1)
            ...     print(f"Found: {currency.name}")
            ... except CurrencyNotFoundError:
            ...     print("Currency not found")
        """
        currency = await self.repository.get_by_id(currency_id)

        if currency is None:
            raise CurrencyNotFoundError()

        return CurrencyDTO.model_validate(currency)

    async def get_by_currency_code(self, currency_code: str) -> CurrencyDTO:
        """Get currency by its ISO 4217 code.

        Args:
            currency_code: Three-letter currency code (e.g., 'USD', 'EUR')

        Returns:
            CurrencyDTO: Currency data

        Raises:
            CurrencyNotFoundError: If currency with given code doesn't exist

        Example:
            >>> # Get currency by code
            >>> usd = await currency_service.get_by_currency_code('USD')
            >>> print(f"USD symbol: {usd.symbol}")
        """
        currency = await self.repository.get_by_currency_code(currency_code)

        if currency is None:
            raise CurrencyNotFoundError()

        return CurrencyDTO.model_validate(currency)

    async def update(
        self,
        currency_id: int,
        currency_code: str | None,
        name: str | None,
        symbol: str | None,
    ) -> CurrencyDTO:
        """Update an existing currency.

        Only provided fields will be updated. This method is useful for
        correcting currency details or updating symbols.

        Args:
            currency_id: ID of the currency to update
            currency_code: New currency code (if changing)
            name: New currency name (if changing)
            symbol: New currency symbol (if changing)

        Returns:
            CurrencyDTO: Updated currency data

        Raises:
            CurrencyNotFoundError: If currency with given ID doesn't exist
            CurrencyAlreadyExistsError: If trying to change to an existing code

        Example:
            >>> # Update currency symbol
            >>> updated = await currency_service.update(
            ...     currency_id=1,
            ...     symbol="€"  # Change from something else to Euro symbol
            ... )
            >>> await session.commit()
            >>> print(f"Updated symbol: {updated.symbol}")
        """
        currency = await self.repository.update(
            currency_id, currency_code, name, symbol
        )

        if currency is None:
            raise CurrencyNotFoundError()

        await self.session.commit()

        logger.info(
            f"Currency updated successfully: "
            f"id={currency_id}, "
            f"code={currency.currency_code}, "
            f"name={currency.name}, "
            f"symbol={currency.symbol}"
        )
        return CurrencyDTO.model_validate(currency)

    async def delete(self, currency_id: int) -> None:
        """Delete a currency permanently.

        Args:
            currency_id: ID of the currency to delete

        Raises:
            CurrencyNotFoundError: If currency with given ID doesn't exist

        Example:
            >>> try:
            ...     await currency_service.delete(1)
            ...     print("Currency deleted")
            ... except CurrencyNotFoundError:
            ...     print("Currency not found")

        Warning:
            This operation is irreversible! Only delete currencies that are
            not used in any transactions or user preferences. Consider
            deactivating instead of deleting.
        """
        currency = await self.get_by_id(currency_id)
        is_deleted = await self.repository.delete(currency_id)

        if not is_deleted:
            raise CurrencyNotFoundError()

        self.session.commit()
        logger.info(
            f"Currency deleted successfully:"
            f"id={currency_id}"
            f"currency_code={currency.currency_code}"
            f"name={currency.name}"
            f"symbol={currency.symbol}"
        )
