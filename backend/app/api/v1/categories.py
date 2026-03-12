from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services import CategoryService
from app.schemas.category import CategoryResponse
from app.enums import TransactionType

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/filter", response_model=list[CategoryResponse])
async def get_categories(
    user_tg_id: int,
    transaction_type: TransactionType,
    session: AsyncSession = Depends(get_session),
):
    service = CategoryService(session)
    categories = await service.get_by_type_and_user(user_tg_id, transaction_type)
    if categories is None:
        raise HTTPException(status_code=404, detail="Categories not found")
    return categories


@router.get("/{id}", response_model=CategoryResponse)
async def get_by_id(id: int, session: AsyncSession = Depends(get_session)):
    servise = CategoryService(session)
    category = await servise.get_by_id(id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
