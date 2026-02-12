from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserResponse
from app.database import get_session
from app.repositories import UserRepository
from app.services import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    service = UserService(repo)
    user = await service.register_user(
        tg_id=data.tg_id,
        currency_id=data.currency_id
    )
    return user

@router.get("/tg/{user_tg_id}", response_model=UserResponse)
async def get_user_by_tg_id(
    user_tg_id: int,
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    user = await repo.get_by_tg_id(user_tg_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user