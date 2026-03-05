import logging
from datetime import datetime

from app.models import Category
from app.enums import TransactionType
from app.repositories import CategoryRepository, UserRepository


class CategoryService:
    """"""
    def __init__(self, session):
        self.repository = CategoryRepository(session)
        self.user_repository = UserRepository(session)
    
    async def get_by_type_and_user(
        self,
        user_tg_id: int,
        transaction_type: TransactionType
    ) -> list[Category]:
        user = await self.user_repository.get_by_tg_id(user_tg_id)
        if user:
            return await self.repository.get_by_transaction_type_and_user(user.id,transaction_type)
        return []
    async def get_by_id(self, id: int) -> Category | None:
        return await self.repository.get_by_id(id=id)
    
