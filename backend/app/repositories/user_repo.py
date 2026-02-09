from datetime import datetime

from sqlalchemy import select

from app.models import User
from .base_repo import BaseRepository

class UserRepository(BaseRepository):
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
            tg_id: Telegram user ID (unique)
            currency_id: ID of the user's default currency
            created_at: Optional creation timestamp. 
                       If None, database will set current timestamp.
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
        query = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()