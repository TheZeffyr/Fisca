from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
	create_async_engine,
	async_sessionmaker,
	AsyncSession
)


class Database:
	"""Async database manager for SQLAlchemy.
    
    This class handles the database connection setup and provides session management
    for asynchronous operations using SQLAlchemy's async features.
    
    Attributes:
        engine: The SQLAlchemy async engine instance
        SessionLocal: Async session factory for creating database sessions

	Note:
		The engine is created with echo=False to disable SQL query logging.
		Sessions are configured with expire_on_commit=False to allow accessing
		object attributes after a commit.
	"""
	def __init__(self, db_url: str):
		self.engine = create_async_engine(db_url, echo=False)
		self.SessionLocal = async_sessionmaker(
			bind=self.engine,
			class_=AsyncSession,
			expire_on_commit=False
		)
	
	async def get_session(self) -> AsyncGenerator[AsyncSession]:
		"""Get an async database session.

		This method creates a new async session and yields it for use in a
		context manager. The session is automatically closed when the context
		manager exits.

		Yields:
			AsyncSession: SQLAlchemy async session instance
		"""
		async with self.SessionLocal() as session:
			yield session
