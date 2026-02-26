from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services import TransactionService
from app.schemas.transaction import TransactionResponse, TransactionCreate, BalanceResponse


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

@router.get("/balance/main", response_model=BalanceResponse)
async def get_main_balance(
    user_tg_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = TransactionService(session)
    balance = await service.get_balance_for_user(user_tg_id)
    return BalanceResponse(
        user_tg_id=user_tg_id,
        balance=balance,
        balance_type="main"
    )