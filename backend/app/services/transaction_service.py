import logging
from datetime import datetime, date

from app.enums import TransactionType
from app.repositories import (
    TransactionRepository,
    UserRepository,
    CategoryRepository,
    SavingRepository,
)
from exceptions.user import UserNotFoundError
from exceptions.transaction import InvalidTransactionError, InsufficientFundsError
from exceptions.category import CategoryNotFoundError
from exceptions.saving import SavingNotFoundError
from app.schemas.transaction import TransactionDTO

logger = logging.getLogger(__name__)


class TransactionService:
    """ """

    def __init__(self, session):
        self.session = session
        self.repository = TransactionRepository(session)
        self.user_repository = UserRepository(session)
        self.category_repository = CategoryRepository(session)
        self.saving_repository = SavingRepository(session)

    async def create(
        self,
        user_id: int,
        amount: int,
        date: date,
        transaction_type: TransactionType,
        category_id: int | None = None,
        saving_id: int | None = None,
        created_at: datetime | None = None,
    ) -> TransactionDTO:
        """Create a new financial transaction.

        Args:
            user_id: ID of the user
            amount: Transaction amount in minor units (must be > 0)
            date: Date of transaction
            transaction_type: Type (income/expense)
            category_id: Category ID (required for regular transactions)
            saving_id: Saving ID (required for saving operations)
            created_at: Optional creation timestamp

        Returns:
            TransactionDTO: Created transaction data

        Raises:
            UserNotFoundError: If user doesn't exist
            CategoryNotFoundError: If category doesn't exist
            SavingNotFoundError: If saving doesn't exist
            InvalidTransactionError: If transaction data is invalid
            InsufficientFundsError: If not enough money for expense
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User not found: user_id={user_id}")
            raise UserNotFoundError()

        if category_id and saving_id:
            logger.warning(
                f"Transaction rejected: both category and saving provided. "
                f"category_id={category_id}, saving_id={saving_id}, "
                f"user_id={user_id}, type={transaction_type.value}"
            )
            raise InvalidTransactionError()

        if not category_id and not saving_id:
            logger.warning(
                f"Transaction rejected: neither category nor saving provided. "
                f"user_id={user_id}, type={transaction_type.value}, amount=  {amount}"
            )
            raise InvalidTransactionError()

        if category_id:
            category = await self.category_repository.get_by_id(category_id)
            if not category:
                logger.warning(f"Category not found: category_id={category_id}")
                raise CategoryNotFoundError()

            if category.transaction_type != transaction_type:
                logger.warning(
                    f"Category type mismatch: "
                    f"category_id={category_id}, category_type={category.transaction_type.value}, "
                    f"transaction_type={transaction_type.value}"
                )
                raise InvalidTransactionError()

            if category.user_id != user.id and category.user_id != None:
                logger.warning(
                    f"Category does not belong to user: "
                    f"category_id={category_id}, user_id={user.id}, "
                    f"category_user_id={category.user_id}"
                )
                raise InvalidTransactionError()

            balance = await self.repository.get_user_balance(user.id)
            if transaction_type == TransactionType.EXPENSE and amount > balance:
                logger.warning(
                    f"Insufficient funds for expense: "
                    f"user_id={user.id}, balance={balance}, amount={amount}"
                )
                raise InsufficientFundsError()

        if saving_id:
            saving = await self.saving_repository.get_by_id(saving_id)

            if not saving:
                logger.warning(f"Saving not found: saving_id={saving_id}")
                raise SavingNotFoundError()

            if saving.user_id != user.id:
                logger.warning(
                    f"Saving does not belong to user: "
                    f"saving_id={saving_id}, user_id={user.id}, saving_user_id={saving.user_id}"
                )
                raise InvalidTransactionError()

            balance = await self.repository.get_saving_balance(saving.id)
            if transaction_type == TransactionType.EXPENSE and amount > balance:
                logger.warning(
                    f"Insufficient funds in saving {saving_id}: "
                    f"balance={balance}, amount={amount}"
                )
                raise InsufficientFundsError()

        transaction = await self.repository.create(
            user_id=user_id,
            amount=amount,
            date=date,
            transaction_type=transaction_type,
            category_id=category_id,
            saving_id=saving_id,
            created_at=created_at,
        )
        await self.session.commit()
        logger.info(
            f"Transaction created successfully: "
            f"id={transaction.id}, user_id={user_id}, amount={amount}, "
            f"type={transaction_type.value}, date={date}, "
            f"category={category_id}, saving={saving_id}"
        )
        return TransactionDTO.model_validate(transaction)

    async def get_user_balance(self, user_tg_id: int) -> int:
        user = await self.user_repository.get_by_tg_id(user_tg_id)
        if not user:
            logger.warning(f"")
            raise UserNotFoundError()

        return await self.repository.get_user_balance(user.id)

    async def get_saving_balance(self, saving_id: int) -> int:
        saving = await self.saving_repository.get_by_id(saving_id)
        if not saving:
            logger.warning(f"")
            raise SavingNotFoundError

        return await self.repository.get_saving_balance(saving.id)
