from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, Any, Generic
from sqlalchemy import select
from app.models import BaseModel


ModelType = TypeVar("ModelType", bound="BaseModel")


class BaseRepository(Generic[ModelType]):
    """Base class for all repositories.

    Provides common CRUD operations for SQLAlchemy models.
    All methods work within the current transaction - commit should be handled by the service layer.
    
    Attributes:
        session: SQLAlchemy async session
        model: SQLAlchemy model class this repository operates on
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def _create(self, **kwargs: Any) -> ModelType:
        """Create a new model instance and add to session (no commit).
        
        Args:
            **kwargs: Field values for the new model
            
        Returns:
            ModelType: Created model instance with refreshed data
            
        Note:
            Does NOT commit transaction. Call session.commit() separately.
            Automatically refreshes the instance to get generated fields.
        """
        model = self.model(**kwargs)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return model
    
    async def _update(self, model: ModelType, **kwargs) -> ModelType:
        """Update an existing model instance (no commit).
        
        Args:
            model: Model instance to update
            **kwargs: Fields to update
            
        Returns:
            ModelType: Updated model instance
        """
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)

        await self.session.flush()
        await self.session.refresh(model)
        return model
    async def _delete(self, model: ModelType) -> None:
        """Delete a model instance (no commit).
        
        Args:
            model: Model instance to delete
        """
        await self.session.delete(model)
        await self.session.flush()
    
    async def _get_by(self, **kwargs) -> ModelType | None:
        """Get a single record by arbitrary filters.
        
        Args:
            **kwargs: Field filters
            
        Returns:
            Optional[ModelType]: First matching record or None
        """
        query = select(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_id(self, id: int) -> ModelType | None:
        """Get a record by its primary key.
        
        Args:
            id: Primary key value
            
        Returns:
            Optional[ModelType]: Record if found, None otherwise
        """
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Get all records with pagination.
        
        Args:
            skip: Number of records to skip (default: 0)
            limit: Maximum number to return (default: 100)
            
        Returns:
            List[ModelType]: List of records
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def exists(self, **kwargs) -> bool:
        """Check if any record exists with given filters.
        
        Args:
            **kwargs: Field filters
            
        Returns:
            bool: True if at least one record exists, False otherwise
        """
        from sqlalchemy import exists
        
        query = select(exists().where(
            *[getattr(self.model, key) == value for key, value in kwargs.items()]
        ))
        result = await self.session.execute(query)
        return result.scalar_one()
