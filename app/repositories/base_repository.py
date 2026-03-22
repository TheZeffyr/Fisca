from typing import Type, TypeVar, Any, Generic, Union

from sqlalchemy import select, desc
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

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

    OPERATORS = {
        "eq": lambda c, v: c == v,
        "ne": lambda c, v: c != v,
        "gt": lambda c, v: c > v,
        "gte": lambda c, v: c >= v,
        "lt": lambda c, v: c < v,
        "lte": lambda c, v: c <= v,
        "like": lambda c, v: c.like(f"%{v}%"),
        "ilike": lambda c, v: c.ilike(f"%{v}%"),
        "in": lambda c, v: c.in_(v),
    }

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
        return model

    async def _get_by(self, **kwargs) -> ModelType | None:
            """Get a single record by arbitrary filters.

            Args:
                **kwargs: Field filters

            Returns:
                (ModelType, nullable): First matching record or None
            """
            query = select(self.model)
            for key, value in kwargs.items():
                colums = self.model.__table__.columns.keys()
                if key in colums:
                    query = query.where(getattr(self.model, key) == value)

            result = await self.session.execute(query)
            return result.scalars().first()

    async def _get_many(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Union[str, list[str]] | None = None,
        **filters: Any,
    ) -> list[ModelType]:
        """Get multiple records with filtering, pagination, and sorting.

        Args:
            skip: Number of records to skip
            limit: Maximum number to return
            order_by: Field(s) to sort by. Use "-field" for descending.
            **filters: Field filters with operators:
                       - Simple: field=value
                       - With operators: field__gt=100, field__in=[1,2,3]
                       - Special: field__between=[10,20], field__is_null=True

        Returns:
            list[ModelType]: List of matching records (always list)
        """
        limit = min(limit, 1000)

        query = select(self.model)

        columns = self.model.__table__.columns.keys()

        for key, value in filters.items():
            if value is None:
                continue

            if "__" in key:
                field_name, operator = key.split("__", 1)

                if field_name not in columns:
                    continue

                column: ColumnElement = getattr(self.model, field_name)

                if operator == "between" and isinstance(value, (list, tuple)):
                    if len(value) == 2:
                        query = query.where(column.between(value[0], value[1]))
                    continue

                if operator == "is_null":
                    query = query.where(
                        column.is_(None) if value else column.is_not(None)
                    )
                    continue

                if operator in self.OPERATORS:
                    query = query.where(self.OPERATORS[operator](column, value))

            else:
                if key in columns:
                    query = query.where(getattr(self.model, key) == value)

        if order_by:

            if isinstance(order_by, str):
                order_by = [order_by]

            for field in order_by:

                desc_order = field.startswith("-")
                field_name = field[1:] if desc_order else field

                if field_name not in columns:
                    continue

                column = getattr(self.model, field_name)

                query = query.order_by(desc(column) if desc_order else column)

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return list(result.scalars())

    async def get_by_id(self, id: int) -> ModelType | None:
        """Get a record by its primary key.

        Args:
            id: Primary key value

        Returns:
            ModelType|None: Record if found, None otherwise
        """
        return await self._get_by(id=id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Get all records with pagination.

        Args:
            skip: Number of records to skip (default: 0)
            limit: Maximum number to return (default: 100)

        Returns:
            List[ModelType]: List of records
        """
        return await self._get_many(skip=skip, limit=limit)


    async def _update(self, model: ModelType, **kwargs) -> ModelType:
        """Update an existing model instance (no commit).

        Args:
            model: Model instance to update
            **kwargs: Fields to update

        Returns:
            ModelType: Updated model instance
        """
        for key, value in kwargs.items():
            columns = model.__table__.columns.keys()
            if key in columns:
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
    
    async def exists(self, **kwargs) -> bool:
        """Check if any record exists with given filters.

        Args:
            **kwargs: Field filters

        Returns:
            bool: True if at least one record exists, False otherwise
        """

        query = select(self.model.id).filter_by(**kwargs).limit(1)
        result = await self.session.execute(query)
        return result.scalar() is not None