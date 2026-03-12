import re
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from app.utils import strings


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Base model class for all database entities.

    This abstract base class provides common functionality for all models:
        - Automatic table name generation (CamelCase → snake_case + plural)
        - Primary key 'id' for all models
        - 'created_at' timestamp with database default
        - Async support via SQLAlchemy's AsyncAttrs

    All model classes should inherit from this BaseModel to maintain consistency across the application.

    Attributes:
        id (int): Auto-incrementing primary key
        created_at (datetime): Timestamp when record was created (set by database)
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Automatically generates a table name based on the class name.

        Converts CamelCase class name to snake_case and applies English
        pluralization rules (handles exceptions like person → people).

        Returns:
            str: Pluralized table name in snake_case
        """
        name = cls.__name__

        name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
        name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
        name = name.lower()

        return strings.pluralize(name)

    def __repr__(self) -> str:
        pk = f"id={self.id}" if hasattr(self, "id") else "no id"
        return f"<{self.__class__.__name__}({pk})>"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        index=True
    )
