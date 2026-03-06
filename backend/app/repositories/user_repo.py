from datetime import datetime

from .base_repo import BaseRepository
from app.models import User


class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    
    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session):
        super().__init__(session, User)
    
    async def create(
        self,
        tg_id: int,
        currency_id: int,
        created_at: datetime | None = None
    ) -> User:
        """
        Create a new user with Telegram ID.

        Args:
            tg_id (int): Telegram user ID (unique)
            currency_id (int): ID of the user's default currency
            created_at (datetime): Optional creation timestamp. If None, database will set current timestamp.
        Returns:
            User: Created User instance
        """
        return await super()._create(
            tg_id=tg_id,
            currency_id=currency_id,
            created_at=created_at
        )
    
    async def get_by_tg_id(self, tg_id: int) -> User | None:
        """
        Retrieve user by Telegram ID.
        
        Args:
            tg_id: Telegram user ID to search for
        
        Returns:
            User | None: User instance if found, None otherwise
        """
        return await self._get_by(tg_id=tg_id)
    
    async def update_currency(self, user_id: int, currency_id: int) -> User |None:
        """Update user's default currency.
    
        Args:
            user_id: ID of the user to update
            currency_id: New currency ID

        Returns:
            User | None: Updated user if found, None otherwise
        """
        user = await self.get_by_id(user_id)
        if not user:
            return None
        return await self._update(user, currency_id=currency_id)

    async def delete(self, user_id: int) -> bool:
        """Delete a user by ID.
        
        This is a HARD DELETE - removes user permanently.

        Args:
            user_id: ID of the user to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self._delete(user)
        return True
    
