from pydantic import BaseModel

class UserCreate(BaseModel):
    tg_id: int
    currency_id: int

class UserResponse(BaseModel):
    id: int
    tg_id: int
    currency_id: int

    class Config:
        from_attributes = True