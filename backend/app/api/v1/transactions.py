from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services import TransactionService
from app.schemas.transaction import TransactionResponse, TransactionCreate


router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    data: TransactionCreate,
    session: AsyncSession = Depends(get_session)
):
    service = TransactionService(session)
    transaction = await service.create(
        user_tg_id=data.user_tg_id,
        category_id=data.category_id,
        saving_id=data.saving_id,
        amount=data.amount,
        date_time=data.date_time,
        transaction_type=data.transaction_type
    )
    return transaction