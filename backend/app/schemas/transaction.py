from datetime import datetime

from pydantic import BaseModel
from app.enums import TransactionType

class TransactionDTO(BaseModel):
    id: int
    amount: int 