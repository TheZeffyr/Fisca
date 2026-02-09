from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, Any, Generic
from sqlalchemy import select
from app.models import BaseModel


ModelType = TypeVar("ModelType", bound="BaseModel")


class BaseRepository(Generic[ModelType]):
    """Base class for all repositories.

    This class provides low-level CRUD operations for a single SQLAlchemy model.

    Attributes:
        session: SQLAlchemy async session
        model: SQLAlchemy model class this repository operates on.
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def _create(self, **kwargs: Any) -> ModelType:
        model = self.model(**kwargs)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model

    async def get(self, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        query = select(self.model)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def delete(self, id: int) -> bool:
        model = await self.session.get(self.model, id)

        if not model:
            return False

        await self.session.delete(model)

        return True

    async def _update(self, model: ModelType, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return model
