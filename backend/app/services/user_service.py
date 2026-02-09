import logging
from datetime import datetime

from app.repositories import UserRepository
from app.models import User


logger = logging.getLogger(__name__)

class UserService:
    """
    Business logic service for User operations.
    """
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def register_user(
          self,
          tg_id: int,
          currency_id: int,
          created_at: datetime | None = None
    ) -> User:
        """
        Register a new Telegram user in the system.
        
        Performs the complete user registration workflow:
            1. Checks if user already exists (prevent duplicates)
            
        Args:
            tg_id: Telegram user ID. Must be unique across the system.
            currency_id: ID of the default currency for the user.
                         Typically selected during onboarding.
            created_at: Optional timestamp for user creation.
                       If None, the repository will use current time.
        
        Returns:
            User: The newly registered user entity with database-generated ID.
        
        Raises:
            ValueError: If user with given tg_id already exists.
        """
        existing = await self.repository.get_by_tg_id(tg_id)
        if existing:
            logger.warning(
                f"Attempt to register already existing user with tg_id {tg_id}"
            )
            raise ValueError(f"User with tg_id {tg_id} already exists")
        user = await self.repository.create(
            tg_id=tg_id,
            currency_id=currency_id,
            created_at=created_at
        )
        logger.info(
            f"User registered successfully: \
            id={user.id}, tg_id={user.tg_id}, currency_id={user.currency_id}"
        )
        return user