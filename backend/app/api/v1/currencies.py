from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.currency import CurrencyResponse
from app.database import get_session
from app.repositories import CurrencyRepository


router = APIRouter(prefix="/currencies", tags=["currencies"])

@router.get("/", response_model=list[CurrencyResponse])
async def get_currencies(
    session: AsyncSession = Depends(get_session)
):
    repo = CurrencyRepository(session)
    currencies = await repo.get_all()
    if not currencies:
        raise HTTPException(status_code=404, detail="User not found")
    return currencies