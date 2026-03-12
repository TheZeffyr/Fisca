from datetime import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    tg_id: int
    currency_id: int
    created_at: datetime
