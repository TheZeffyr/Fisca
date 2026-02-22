from datetime import datetime

from app.models import Saving
from .base_repo import BaseRepository


class SavingRepository(BaseRepository):
    """"""
    async def __init__(self, session):
        super().__init__(session, Saving)
    
    async def create(
        self,
        user_id: int,
        name: str,
        final_amount: int,
        deadline: datetime,
        created_at: datetime | None = None
    ) -> Saving:
        """"""
        return await super()._create(
            user_id=user_id,
            name=name,
            final_amount=final_amount,
            deadline=deadline,
            created_at=created_at
        )