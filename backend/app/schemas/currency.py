from datetime import datetime

from pydantic import BaseModel, Field

class CurrencyDTO(BaseModel):
    id: int
    currency_code: str = Field(min_length=3,max_length=3)
    name: str = Field(min_length=1, max_length=50)
    symbol: str = Field(min_length=1, max_length=1)
    created_at: datetime