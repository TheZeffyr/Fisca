from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services import SavingService
from app.schemas.saving import SavingCreate, SavingResponse
from app.schemas.transaction import BalanceResponse

router = APIRouter(prefix="/savings", tags=["savings"])


@router.post("/", response_model=SavingResponse)
async def create_saving(
    data: SavingCreate, session: AsyncSession = Depends(get_session)
):
    service = SavingService(session)
    saving = await service.create(
        user_tg_id=data.user_tg_id,
        name=data.name,
        final_amount=data.final_amount,
        deadline=data.deadline,
    )
    return saving


@router.get("/", response_model=list[SavingResponse])
async def get_savings_by_user_tg_id(
    user_tg_id: int, session: AsyncSession = Depends(get_session)
):
    service = SavingService(session)
    savings = await service.get_by_user_tg_id(user_tg_id)
    return savings
