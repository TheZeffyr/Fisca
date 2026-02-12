from app.models import Currency
from .base_repo import BaseRepository

class CurrencyRepository(BaseRepository):
    """
    Repository for Currency model operations.
    
    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session):
        super().__init__(session, Currency)
    
    async def get_all(self) -> list[Currency]:
        return await super().get_all()
