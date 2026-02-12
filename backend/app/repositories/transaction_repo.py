from datetime import datetime


from app.models import Transaction
from .base_repo import BaseRepository
from app.enums import TransactionType


class TransactionRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Transaction)
    
    async def create(
        self,
        user_id: int,
        category_id: int,
        amount: int,
        date_time: datetime,
        transaction_type: TransactionType,
        saving_id: int | None = None,
    ) -> Transaction:
        return await super()._create(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            date_time=date_time,
            transaction_type=transaction_type,
            saving_id=saving_id
        )