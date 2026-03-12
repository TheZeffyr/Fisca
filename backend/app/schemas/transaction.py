from datetime import datetime, date

from pydantic import BaseModel, Field
from app.enums import TransactionType


class TransactionDTO(BaseModel):
    """DTO for Transaction model.

    This DTO is used to transfer transaction data between layers
    without exposing database models. Includes validation rules
    that match the database constraints.

    Attributes:
        id: Unique transaction identifier
        user_id: ID of the user who owns this transaction
        category_id: ID of the category (for regular transactions)
        saving_id: ID of the saving goal (for saving operations)
        amount: Transaction amount in minor units (cents/pennies)
        date: When the transaction occurred
        transaction_type: Type (income/expense)
        created_at: When the record was created
    """

    id: int
    user_id: int
    category_id: int | None
    saving_id: int | None
    amount: int = Field(gt=0)
    date: date
    transaction_type: TransactionType
    created_at: datetime
