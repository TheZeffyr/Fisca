from datetime import datetime
from pydantic import BaseModel


class SavingCreate(BaseModel):
    user_tg_id: int
    name: str
    final_amount: int
    deadline: datetime

class SavingResponse(BaseModel):
    id: int
    user_id: int
    name: str
    final_amount: int
    deadline: datetime
    created_at: datetime