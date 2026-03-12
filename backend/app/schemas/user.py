from datetime import datetime

from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    id: int
    tg_id: int
    currency_id: int
    created_at: datetime

class UserCreate(BaseModel):
    tg_id: int 
    currency_id: int = Field(gt=0)
    created_at: datetime | None

class UserUpdate(BaseModel):
    currency_id: int = Field(gt=0)