from datetime import date, datetime

from app.models import Transaction
from app.enums import TransactionType
from app.repositories import BaseRepository


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
        note: str | None,
        from_account_id: int | None,
        to_account_id: int | None,
        category_id: int | None = None,
        created_at: datetime | None = None
    ) -> Transaction:
        """Create a new transaction.

        Args:
            amount (Decimal): The sum of the transaction.
        	date (date): The date when the transaction occurred. This field is required for reports and sorting.
        	note (str | None): A note to the transaction.
        	from_account_id (int | None): ID of the write-off account. For expenses and transfers. If null, transaction is revenue.
        	to_account_id (int | None): ID of account entry. For revenue and transfers. If null, the transaction is an expense.
        	user_id (int): ID of transaction owner user.
        	category_id (int | None): ID of transaction category.
        	from_account (Account | None): Write-off account.
        	to_account (Account | None): A credit score.
        	user (User): The transaction owner.
        	category (Category | None): Transaction category.

        Returns:
            Transaction: Created transaction instance
        """
        return await self._create(
            user_id=user_id,
            amount=amount,
            date=date,
            note=note,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            category_id=category_id,
            created_at=created_at
        )
    
    async def get_last_month(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Transaction]:
        """Get all transactions from the previous calendar month.

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
            order_by="-date",
            skip=skip,
            limit=limit
        )

    async def get_by_month(
        self,
        user_id: int,
        month: date,
        skip: int = 0,
        limit: int = 100
    ) -> list[Transaction]:
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
            order_by="-date",
            skip=skip,
            limit=limit
        )

    async def get_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Transaction]:
        """Get all transactions for a user.

        Args:
            user_id: ID of the user

        Returns:
            list[Transaction]: All user transactions, newest first
        """
        return await self._get_many(
            user_id=user_id,
            skip=skip,
            limit=limit
        )

    async def get_by_category(
        self,
        user_id: int,
        category_id: int,
        skip: int = 0,
        limit: int = 100
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
            order_by="-date",
            skip=skip,
            limit=limit
        )
    
    async def update(
        self,
        transaction_id: int,
        category_id: int | None = None,
        from_account_id: int | None = None,
        to_account_id: int | None = None,
        note: str | None = None,
        amount: int | None = None,
        date: date | None = None,
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
        elif from_account_id is not None:
            update_data["from_account_id"] = from_account_id
        if amount is not None:
            update_data["amount"] = amount
        if date is not None:
            update_data["date"] = date
        if to_account_id is not None:
            update_data["to_account_id"] = to_account_id
        if note is not None:
            update_data["note"] = note

        return await self._update(transaction, **update_data)


    async def delete(self, transaction: Transaction) -> None:
        """Delete a transaction permanently.

        Args:
            transaction_id: ID of the transaction to delete

        Returns:
            bool: True if deleted, False if not found

        Note:
            This performs a hard delete. Consider soft delete if you need history.
        """
        await self._delete(transaction)
