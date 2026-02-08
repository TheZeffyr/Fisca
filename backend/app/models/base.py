from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.database import Base


class BaseModel(AsyncAttrs, Base):
    """
    The base class for all SQLAlchemy models with async support.
    Attributes:
        id (int): Primary key, automatically incremented

    Methods:
        __tablename__: Automatically generates a table name
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Automatically generates a table name based on the class name."""
        import re
        name = cls.__name__
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return name

    id: Mapped[int] = mapped_column(primary_key=True)