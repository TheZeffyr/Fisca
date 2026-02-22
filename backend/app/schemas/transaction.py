from datetime import datetime

from pydantic import BaseModel
from app.enums import TransactionType

class TransactionCreate(BaseModel):
    user_tg_id: int
    category_id: int
    amount: int
    date_time: datetime
    transaction_type: TransactionType
    saving_id: int | None = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: int
    date_time: datetime
    transaction_type: TransactionType
    saving_id: int | None = None

    class Config:
        from_attributes = True