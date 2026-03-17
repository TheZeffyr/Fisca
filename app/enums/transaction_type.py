from enum import StrEnum


class TransactionType(StrEnum):
    """Enumeration of possible transaction types."""
    INCOME = "income"
    EXPENSE = "expense"
