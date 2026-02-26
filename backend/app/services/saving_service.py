import logging
from datetime import datetime

from app.models import Saving
from app.repositories import SavingRepository, UserRepository


class SavingService:
    """"""
    def __init__(self, session):
        self.saving_repository = SavingRepository(session)
        self.user_repository = UserRepository(session)
    
    async def create(
        self,
        user_tg_id: int,
        name: str,
        final_amount: int,
        deadline: datetime,
        created_at: datetime | None = None
    ) -> Saving:
        """"""
        user = await self.user_repository.get_by_tg_id(user_tg_id)
        if not user:
            raise ValueError(f"User not found: {user_tg_id}")
        return await self.saving_repository.create(
            user_id=user.id,
            name=name,
            final_amount=final_amount,
            deadline=deadline,
            created_at=created_at
        )

    async def get_by_user_tg_id(self, user_tg_id: int) -> list[Saving]:
        user = await self.user_repository.get_by_tg_id(user_tg_id)
        if not user:
            raise ValueError(f"User not found: {user_tg_id}")
        return await self.saving_repository.get_by_user_id(user.id)
