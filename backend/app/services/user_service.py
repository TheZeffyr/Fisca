import logging
from datetime import datetime

from app.repositories import UserRepository, CurrencyRepository
from app.schemas.user import UserDTO
from exceptions.user import UserNotFoundError, UserAlreadyExistsError
from exceptions.currency import CurrencyNotFoundError

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related business logic.

    This service handles all operations related to users:
    - Registration of new users (Telegram users)
    - Retrieving user information by Telegram ID
    - Updating user preferences (currency)
    - Deleting user accounts

    The service works with UserRepository for user data and
    CurrencyRepository for currency validation. All methods
    return UserDTO objects to avoid exposing database models.

    Attributes:
        session: SQLAlchemy async session
        repository: UserRepository for user operations
        currency_repository: CurrencyRepository for currency validation
    """

    def __init__(self, session):
        self.session = session
        self.repository = UserRepository(session)
        self.currency_repository = CurrencyRepository(session)

    async def register_user(
        self, tg_id: int, currency_id: int, created_at: datetime | None = None
    ) -> UserDTO:
        """Register a new user in the system.

        This method creates a new user record. If a user with the same
        Telegram ID already exists, it raises an exception.

        Args:
            tg_id: Telegram user ID (unique identifier from Telegram)
            currency_id: ID of the user's preferred currency
            created_at: Optional registration timestamp.
                       If None, database will set current time.

        Returns:
            UserDTO: Created user data

        Raises:
            UserAlreadyExistsError: If user with given tg_id already exists

        Example:
            >>> user = await user_service.register_user(
            ...     tg_id=123456789,
            ...     currency_id=1  # USD
            ... )
            >>> print(f"User registered: {user.id}")
        """
        existing = await self.repository.get_by_tg_id(tg_id)#TODO: переписать на existing
        if existing:
            logger.warning(
                f"Attempt to register already existing user with tg_id {tg_id}"
            )
            raise UserAlreadyExistsError(tg_id=tg_id)

        user = await self.repository.create(
            tg_id=tg_id, currency_id=currency_id, created_at=created_at
        )
        await self.session.commit()
        logger.info(f"User registered successfully: \
            id={user.id}, tg_id={user.tg_id}, currency_id={user.currency_id}")
        return UserDTO.model_validate(user)

    async def get_user_by_tg_id(self, tg_id: int) -> UserDTO:
        """Get user by Telegram ID.

        Args:
            tg_id: Telegram user ID to search for

        Returns:
            UserDTO: User data if found

        Raises:
            UserNotFoundError: If user with given tg_id doesn't exist

        Example:
            >>> try:
            ...     user = await user_service.get_by_tg_id(123456789)
            ...     print(f"Found user: {user.id}")
            ... except UserNotFoundError:
            ...     print("User not registered")
        """
        user = await self.repository.get_by_tg_id(tg_id)

        if user is None:
            raise UserNotFoundError(tg_id=tg_id)

        return UserDTO.model_validate(user)
    
    async def get_user(self, user_id: int) -> UserDTO:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)

        return UserDTO.model_validate(user)
    
    async def update_user(self, user_id: int, currency_id: int) -> UserDTO:
        """update_user user's fields.


        Args:
            user_id: user ID
            currency_id: New currency ID

        Returns:
            UserDTO: Updated user data

        Raises:
            UserNotFoundError: If user with given tg_id doesn't exist
            CurrencyNotFoundError: If currency with given ID doesn't exist

        Example:
            >>> try:
            ...     user = await user_service.update_currency(
            ...         tg_id=123456789,
            ...         currency_id=2  # EUR
            ...     )
            ...     print(f"Currency updated to {user.currency_id}")
            ... except CurrencyNotFoundError:
            ...     print("Currency not found")
        """
        user = await self.get_user(user_id)
        currency_exists = await self.currency_repository.exists(currency_id=currency_id)

        if not currency_exists:
            raise CurrencyNotFoundError(currency_id)

        user = await self.repository.update_currency(
            user_id=user.id, currency_id=currency_id
        )

        if user is None:
            raise UserNotFoundError()
        await self.session.commit()

        return UserDTO.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        """Delete a user account permanently.

        This method removes the user and all associated data
        (transactions, categories, savings) from the database.

        Args:
            tg_id: Telegram user ID

        Raises:
            UserNotFoundError: If user with given tg_id doesn't exist

        Example:
            >>> try:
            ...     await user_service.delete(123456789)
            ...     print("User deleted successfully")
            ... except UserNotFoundError:
            ...     print("User not found")

        Warning:
            This operation is irreversible! All user data will be lost.
            Consider soft delete (deactivate) instead if you need to keep data.
        """
        user = await self.get_user(user_id)

        if not user:
            raise UserNotFoundError()

        await self.repository.delete(user.id)
        await self.session.commit()
        logger.info(f"User deleted successfully: \
                    id={user.id}, tg_id={user.tg_id}")
