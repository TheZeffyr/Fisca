from pydantic import BaseModel

class CurrencyResponse(BaseModel):
    id: int
    currency_code: str
    name: str
    symbol: str
    class Config:
        from_attributes = True