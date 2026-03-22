from datetime import date
from decimal import Decimal

from app.models import Account
from app.enums import AccountType
from app.repositories import BaseRepository


class AccountRepository(BaseRepository[Account]):
	"""Repository for Account model operations.

	Provides specialized methods for account management, including
	filtering by type and status.

	Attributes:
		session: SQLAlchemy async session
	"""

	def __init__(self, session):
		super().__init__(session, Account)

	async def create(
		self,
		name: str,
		type: AccountType,
		target_amount: Decimal | None,
		end_date: date | None,
		user_id: int
	) -> Account:
		"""Create a new account.

		Args:
			name: Account name (e.g., "Wallet", "Savings for car")
			type: Account type (CASH, CARD, or SAVINGS)
			user_id: ID of the user who owns this account
			target_amount: Target amount for SAVINGS accounts (required for SAVINGS)
			end_date: Target end date for SAVINGS accounts (optional)

		Returns:
			Account: Created account instance

		Raises:
			ValueError: If SAVINGS account created without target_amount
		"""
		return await self._create(
			name=name,
			type=type,
			target_amount=target_amount,
			end_date=end_date,
			user_id=user_id
		)

	async def get_by_user(
		self,
		user_id: int,
		skip: int = 0,
		limit: int = 100
	) -> list[Account]:
		"""Get all accounts owned by a specific user.

		Args:
			user_id: ID of the user
			skip: Number of records to skip (for pagination)
			limit: Maximum number of records to return

		Returns:
			list[Account]: List of user's accounts
		"""
		return await self._get_many(
			user_id=user_id,
			skip=skip,
			limit=limit
		)
	async def get_savings_by_user(
		self,
		user_id: int,
		skip: int = 0,
		limit: int = 100
	) -> list[Account]:
		"""Get active savings accounts for a user (not completed by default).

		Args:
			user_id: ID of the user
			skip: Number of records to skip (for pagination)
			limit: Maximum number of records to return
			include_completed: If True, include completed savings accounts

		Returns:
			list[Account]: List of user's savings accounts
		"""
		return await self._get_many(
			user_id=user_id,
			type=AccountType.SAVINGS,
			is_completed=False,
			skip=skip,
			limit=limit
	)
	async def get_all_savings_by_user(
		self,
		user_id: int,
		skip: int = 0,
		limit: int = 100
	) -> list[Account]:
		"""Get all savings accounts for a user (including completed).

		Args:
			user_id: ID of the user
			skip: Number of records to skip (for pagination)
			limit: Maximum number of records to return

		Returns:
			list[Account]: List of all user's savings accounts
		"""
		return await self._get_many(
			user_id=user_id,
			type=AccountType.SAVINGS,
			skip=skip,
			limit=limit
	)
	async def update(
		self,
		account_id: int,
		name: str | None,
		type: AccountType | None,
		target_amount: Decimal | None,
		end_date: date | None,
		is_completed: bool | None,
		balance: Decimal | None
	) -> Account | None:
		"""Update an existing account.

		Args:
			account_id: ID of the account to update
			name: New account name (optional)
			type: New account type (optional)
			target_amount: New target amount (optional)
			end_date: New end date (optional)
			is_completed: New completion status (optional)
			balance: New balance (optional)

		Returns:
			Account | None: Updated account if found, None otherwise

		Note:
			Only provided fields will be updated. None values are ignored.
			For SAVINGS accounts, validation should be done in service layer.
		"""
		account = await self.get_by_id(account_id)
		if account is None:
			return None
		
		update_data = {}
		if name is not None:
			update_data["name"] = name
		if type is not None:
			update_data["type"] = type
		if target_amount is not None:
			update_data["target_amount"] = target_amount
		if end_date is not None:
			update_data["end_date"] = end_date
		if is_completed is not None:
			update_data["is_completed"] = is_completed
		if balance is not None:
			update_data["balance"] = balance



		if not update_data:
			return account

		return await self._update(account, **update_data)

	async def delete(self, account: Account) -> None:
		"""Delete an account permanently.

		Warning: This is a hard delete. All associated transactions will be
		affected according to their ondelete rules:
		- Transactions: from_account_id/to_account_id set to NULL (if ondelete="RESTRICT" is configured)

		Args:
			account: Account instance to delete

		Note:
			Consider using soft delete (deactivate) instead for better data retention.
		"""
		await self._delete(account)
