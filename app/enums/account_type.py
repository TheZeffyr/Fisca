from enum import StrEnum


class AccountType(StrEnum):
    """Types of accounts in the system.
    
    Cash: Cash (wallet)
    Card: Bank cards (debit/credit)
    savings: Purpose-built savings
    """
    
    CASH = "cash"
    CARD = "card"
    SAVINGS = "savings"
