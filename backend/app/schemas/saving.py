from datetime import datetime, date
from pydantic import BaseModel, Field


class SavingDTO(BaseModel):
    id: int
    user_id: int
    final_amount: int = Field(gt=0)
    deadline: date | None
    is_completed: bool
    created_at: datetime