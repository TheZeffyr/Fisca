from app.models import Category
from .base_repo import BaseRepository
from sqlalchemy import select, or_
from app.enums.transaction_type import TransactionType


class CategoryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Category)
    
    async def get_all(self) -> list[Category]:
        return await super().get_all()

    async def get_by_transaction_type_and_user(
        self,
        user_id: int,
        transaction_type: TransactionType
    ) -> list[Category]:
        query = select(Category).where(
            or_(
                Category.is_global==True,
                Category.user_id==user_id,
            ),
            Category.transaction_type==transaction_type
        ).order_by(Category.is_global.desc(), Category.name)

        result = await self.session.execute(query)
        return list(result.scalars().all())
