import logging
from datetime import datetime

from app.models import Transaction
from app.enums import TransactionType
from app.repositories import TransactionRepository, UserRepository


class TransactionService:
    """"""
    def __init__(self, session):
        self.repository = TransactionRepository(session)
        self.user_repository = UserRepository(session)
    
    async def create(
            self,
            user_tg_id: int,
            category_id: int,
            amount: int,
            date_time: datetime,
            transaction_type: TransactionType,
            saving_id: int | None = None,
        ) -> Transaction:
            user = await self.user_repository.get_by_tg_id(user_tg_id)
            if not user:
                raise ValueError(f"User not found: {user_tg_id}")
            return await self.repository.create(
                user_id=user.id,
                category_id=category_id,
                amount=amount,
                date_time=date_time,
                transaction_type=transaction_type,
                saving_id=saving_id
            )
    async def get_balance_for_user(self, user_tg_id: int) -> float:
        user = await self.user_repository.get_by_tg_id(user_tg_id)
        if not user:
            raise ValueError(f"User not found: {user_tg_id}")
        return await self.repository.get_balance_for_user(user.id)