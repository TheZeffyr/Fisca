from datetime import date, datetime

from sqlalchemy import select, func, case

from .base_repo import BaseRepository
from app.models import Transaction
from app.enums import TransactionType


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for Transaction model operations.
    
    Attributes:
        session: SQLAlchemy async session
    """
    def __init__(self, session):
        super().__init__(session, Transaction)
    
    async def create(
        self,
        user_id: int,
        amount: int,
        date: date,
        transaction_type: TransactionType,
        category_id: int | None = None,
        saving_id: int | None = None,
        created_at: datetime | None = None
    ) -> Transaction:
        """Create a new transaction.
        
        Args:
            user_id: ID of the user who owns this transaction
            amount: Transaction amount in minor units (e.g., 1000 = 10.00)
            date: Date when transaction occurred
            transaction_type: Type (income, expense, deposit, withdrawal)
            category_id: ID of category (required for income/expense)
            saving_id: ID of saving goal (required for deposit/withdrawal)
            created_at: Optional creation timestamp
            
        Returns:
            Transaction: Created transaction instance
        """
        return await self._create(
            user_id=user_id,
            category_id=category_id,
            saving_id=saving_id,
            amount=amount,
            date=date,
            transaction_type=transaction_type,
            created_at=created_at
        )
    
    async def update(
        self,
        transaction_id: int,
        category_id: int | None = None,
        saving_id: int | None = None,
        amount: int | None = None,
        date: date | None = None,
        transaction_type: TransactionType | None = None
    ) -> Transaction | None:
        """Update an existing transaction.
        
        Only provided fields will be updated. Both category_id and saving_id
        can be updated independently.
        
        Args:
            transaction_id: ID of the transaction to update
            category_id: New category ID (if changing)
            saving_id: New saving ID (if changing)
            amount: New amount in minor units (if changing)
            date: New transaction date (if changing)
            transaction_type: New transaction type (if changing)
            
        Returns:
            Optional[Transaction]: Updated transaction or None if not found
        """
        transaction = await self.get_by_id(transaction_id)
        if transaction is None:
            return None
        
        update_data = {}
        if category_id is not None:
            update_data["category_id"] = category_id
        elif saving_id is not None:
            update_data["saving_id"] = saving_id
        if amount is not None:
            update_data["amount"] = amount
        if date is not None:
            update_data["date"] = date
        if transaction_type is not None:
            update_data["transaction_type"] = transaction_type

        return await self._update(
            transaction,
            **update_data
        )
    async def get_user_balance(self, user_id: int) -> int:
        """Calculate user's current balance based on all transactions.
        
        Balance = sum(income) - sum(expenses)
        
        Args:
            user_id: ID of the user
            
        Returns:
            int: Current balance in minor units (cents/pennies)
                 Can be negative if expenses exceed income.
        """
        total_income = func.sum(
            case(
                (Transaction.transaction_type == TransactionType.INCOME, Transaction.amount),
                else_=0
            )
        ).label('total_income')

        total_expense = func.sum(
            case(
                (Transaction.transaction_type == TransactionType.EXPENSE, Transaction.amount),
                else_=0
            )
        ).label('total_expense')

        query = select(
            total_income,
            total_expense
        ).where(Transaction.user_id == user_id)

        result = await self.session.execute(query)
        row = result.one()

        total_income = row.total_income or 0
        total_expense = row.total_expense or 0

        return total_income - total_expense

    async def get_saving_balance(self, user_id: int, saving_id: int) -> int:
        """Calculate current balance of a specific saving goal.
        
        Balance = sum(deposits) - sum(withdrawals)
        
        Args:
            user_id: ID of the user (for security)
            saving_id: ID of the saving goal
            
        Returns:
            int: Current saving balance in minor units (always >= 0)
        """
        total_income = func.sum(
            case(
                (
                    (Transaction.transaction_type == TransactionType.INCOME) &
                    (Transaction.saving_id == saving_id),
                    Transaction.amount
                ),
                else_=0
            )
        ).label('total_income')
        
        total_expense = func.sum(
            case(
                (
                    (Transaction.transaction_type == TransactionType.EXPENSE) &
                    (Transaction.saving_id == saving_id),
                    Transaction.amount
                ),
                else_=0
            )
        ).label('total_expense')
        
        query = select(
            total_income,
            total_expense
        ).where(
            Transaction.user_id == user_id,
            Transaction.saving_id == saving_id
        )
        
        result = await self.session.execute(query)
        row = result.one()
        
        total_income = row.income or 0
        total_expense = row.expense or 0
        
        balance = total_income - total_expense
        
        if balance < 0:
            balance = 0
            
        return balance

    async def get_last_month(self, user_id: int) -> list[Transaction]:
        """ Get all transactions from the previous calendar month.
        
        Automatically calculates the previous month based on current date.
        
        Args:
            user_id: ID of the user
            
        Returns:
            list[Transaction]: Transactions from last month, newest first
        """
        today = datetime.now()
        first_of_current_month = date(today.year, today.month, 1)
        
        if today.month == 1:
            first_of_last_month = date(today.year - 1, 12, 1)
        else:
            first_of_last_month = date(today.year, today.month - 1, 1)
        return await self._get_many(
            user_id=user_id,
            date__gte=first_of_last_month,
            date__lt=first_of_current_month,
            order_by="-date"
        )

    async def get_by_month(self, user_id: int, month: date) ->list[Transaction]:
        """Get all transactions for a specific month.
        
        Args:
            user_id: ID of the user
            month: Any date in the target month (day is ignored)
            
        Returns:
            list[Transaction]: Transactions from that month, newest first
        """
        start_date = date(month.year, month.month, 1)
        if month.month == 12:
            end_date = date(month.year + 1, 1, 1)
        else:
            end_date = date(month.year, month.month + 1, 1)
        return await self._get_many(
            user_id=user_id,
            date__gte=start_date,
            date__lt=end_date,
            order_by="-date"
        )

    async def get_by_user(self, user_id) -> list[Transaction]:
        """Get all transactions for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            list[Transaction]: All user transactions, newest first
        """
        return  await self._get_many(user_id=user_id)
    
    async def get_by_category(
        self,
        user_id: int,
        category_id: int
    ) -> list[Transaction]:
        """
        Get all transactions in a specific category.
        
        Args:
            user_id: ID of the user
            category_id: ID of the category
            
        Returns:
            list[Transaction]: Transactions in that category
        """
        return await self._get_many(
            user_id=user_id,
            category_id=category_id,
            order_by="-date"
        )


    async def delete(self, transaction_id: int) -> bool:
        """Delete a transaction permanently.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            bool: True if deleted, False if not found
        
        Note:
            This performs a hard delete. Consider soft delete if you need history.
        """
        transaction = await self.get_by_id(transaction_id)
        
        if transaction is None:
            return False
        
        await self._delete(transaction)
        return True
        
