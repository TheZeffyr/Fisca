from datetime import datetime

from pydantic import BaseModel, Field
from app.enums import TransactionType

class CategoryDTO(BaseModel):
    id: int
    user_id: int | None
    name: str = Field(min_length=1,max_length=100)
    transaction_type: TransactionType
    created_at: datetime