import logging
from datetime import datetime, date

from app.enums import TransactionType
from app.repositories import TransactionRepository, UserRepository

logger = logging.getLogger(__name__)

class TransactionService:
    """
    """
    async def create(
        self,
        user_id: int,
        amount: int,
        date: date,
        transaction_type: TransactionType,
        category_id: int | None = None,
        saving_id: int | None = None,
        created_at: datetime | None = None
    ) -> TransactionDTO
