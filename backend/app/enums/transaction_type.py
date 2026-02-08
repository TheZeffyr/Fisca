from enum import StrEnum


class TransactionType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"