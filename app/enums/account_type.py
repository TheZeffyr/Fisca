from enum import StrEnum


class AccountType(StrEnum):
    """Types of accounts in the system.
    
    Cash: Cash (wallet)
    Card: Bank cards (debit/credit)
    PiggyBank: Purpose-built piggybacks
    """
    
    CASH = "cash"
    CARD = "card"
    PIGGY_BANK = "piggy_bank"