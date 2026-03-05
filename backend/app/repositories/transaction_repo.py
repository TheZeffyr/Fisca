from datetime import datetime
from calendar import monthrange

from sqlalchemy import func, case, select

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
    async def get_balance_for_user(self, user_id: int) -> float:
        query = select(
            func.sum(
            case(
                (Transaction.transaction_type == TransactionType.INCOME, Transaction.amount),
                (Transaction.transaction_type == TransactionType.EXPENSE, -Transaction.amount)
            , else_=0).label('total_balance')
        )).where(Transaction.user_id==user_id)
        result = await self.session.execute(query)
        return result.scalar_one() or 0.0
    async def get_balance_for_saving(self, saving_id: int) -> float:
        query = select(
            func.sum(
                case(
                    (Transaction.transaction_type == TransactionType.DEPOSIT, Transaction.amount),
                    (Transaction.transaction_type == TransactionType.WITHDRAWAL,-Transaction.amount),
                    else_=0).label('total_balance')
                )
            ).where(Transaction.saving_id==saving_id)
        result = await self.session.execute(query)
        return result.scalar_one() or 0.0

    async def get_last_month_by_user(self, user_id: int) -> list[Transaction]:
        now = datetime.now()
        
        start_date = datetime(now.year, now.month, 1)
        
        last_day = monthrange(now.year, now.month)[1]
        end_date = datetime(now.year, now.month, last_day, 23, 59, 59)
        
        query = select(Transaction).where(
            Transaction.user_id == user_id,
            Transaction.date_time.between(start_date, end_date)
        ).order_by(Transaction.date_time.desc())
        
        result = await self.session.execute(query)
        return list(result.scalars().all())