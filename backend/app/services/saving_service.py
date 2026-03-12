import logging
from datetime import datetime, date

from schemas.saving import SavingDTO
from app.repositories import SavingRepository, UserRepository
from exceptions.user import UserNotFoundError
from exceptions.saving import SavingNotFoundError

logger = logging.getLogger(__name__)


class SavingService:
    """Service for managing savings goals (piggy banks).

    This service handles all operations related to user savings goals:
    - Creating new savings goals
    - Retrieving savings by user (all, active)
    - Updating savings details (name, deadline)
    - Marking savings as completed
    - Deleting savings goals

    All methods include user verification via Telegram ID and proper error handling.
    """

    def __init__(self, session):
        self.session = session
        self.repository = SavingRepository(session)
        self.user_repository = UserRepository(session)

    async def create(
        self,
        user_tg_id: int,
        name: str,
        final_amount: int,
        deadline: datetime,
        created_at: datetime | None = None,
    ) -> SavingDTO:
        """Create a new savings goal for a user.

        Args:
            user_tg_id: Telegram ID of the user
            name: Name of the savings goal
            final_amount: Target amount to save
            deadline: Target date to achieve the goal
            created_at: Optional creation timestamp


        Raises:
            UserNotFoundError: If user with given tg_id doesn't exist

        Returns:
            SavingDTO: Created savings goal data
        """
        user = await self.user_repository.get_by_tg_id(tg_id=user_tg_id)
        if not user:
            logger.warning(f"User not found when creating saving: tg_id={user_tg_id}")
            raise UserNotFoundError()

        saving = await self.repository.create(
            user_id=user.id,
            name=name,
            final_amount=final_amount,
            deadline=deadline,
            created_at=created_at,
        )
        await self.session.commit()
        logger.info(
            f"Saving created successfully: id={saving.id}, user_tg_id={user_tg_id}, name={name}, final_amount={final_amount}"
        )
        return SavingDTO.model_validate(saving)

    async def get_by_user_tg_id(self, user_tg_id: int) -> list[SavingDTO]:
        """Get all savings goals for a user by their Telegram ID.

        Args:
            user_tg_id: Telegram ID of the user


        Raises:
            UserNotFoundError: If user with given tg_id doesn't exist

        Returns:
            list[SavingDTO]: List of all user's savings goals
        """
        user = await self.user_repository.get_by_tg_id(user_tg_id)
        if user is None:
            raise UserNotFoundError()

        savings = await self.repository.get_by_user_id(user.id)
        return list(map(SavingDTO.model_validate, savings))

    async def get_active(self, user_tg_id: int) -> list[SavingDTO]:
        """Get active (not completed) savings goals for a user.

        Args:
            user_tg_id: Telegram ID of the user

        Raises:
            UserNotFoundError: If user with given tg_id doesn't exist

        Returns:
            list[SavingDTO]: List of active savings goals
        """
        user = await self.user_repository.get_by_tg_id(tg_id=user_tg_id)
        if not user:
            raise UserNotFoundError()

        savings = await self.repository.get_active(user.id)
        return list(map(SavingDTO.model_validate, savings))

    async def update_name(self, saving_id: int, name: str) -> SavingDTO:
        """
        Update the name of a savings goal.

        Args:
            saving_id: ID of the savings goal
            name: New name for the savings goal

        Raises:
            SavingNotFoundError: If saving with given id doesn't exist

        Returns:
            SavingDTO: Updated savings goal data
        """
        saving = await self.repository.update_name(saving_id, name)
        if saving is None:
            logger.warning(
                f"Saving not found when updating name: saving_id={saving_id}"
            )
            raise SavingNotFoundError()

        await self.session.commit()
        logger.info(f"Saving name updated: saving_id={saving_id}, new_name={name}")
        return SavingDTO.model_validate(saving)

    async def update_deadline(self, saving_id: int, deadline: date) -> SavingDTO:
        """Update the deadline of a savings goal.

        Args:
            saving_id: ID of the savings goal
            deadline: New deadline date

        Raises:
            SavingNotFoundError: If saving with given id doesn't exist

        Returns:
            SavingDTO: Updated savings goal data
        """
        saving = await self.repository.update_deadline(saving_id, deadline)
        if saving is None:
            logger.warning(
                f"Saving not found when updating deadline: saving_id={saving_id}"
            )
            raise SavingNotFoundError()

        await self.session.commit()
        logger.info(
            f"Saving deadline updated: saving_id={saving_id}, new_deadline={deadline}"
        )
        return SavingDTO.model_validate(saving)

    async def mark_completed(self, saving_id: int) -> SavingDTO:
        """Mark a savings goal as completed.

        Args:
            saving_id: ID of the savings goal

        Raises:
            SavingNotFoundError: If saving with given id doesn't exist

        Returns:
            SavingDTO: Updated savings goal data
        """
        saving = await self.repository.mark_completed(saving_id)

        if saving is None:
            logger.warning(
                f"Saving not found when marking completed: saving_id={saving_id}"
            )
            raise SavingNotFoundError()

        await self.session.commit()
        logger.info(
            f"Saving marked as completed: saving_id={saving_id}, name={saving.name}"
        )
        return SavingDTO.model_validate(saving)

    async def delete(self, saving_id: int) -> None:
        """Delete a savings goal permanently.

        Args:
            saving_id: ID of the savings goal to delete

        Raises:
            SavingNotFoundError: If saving with given id doesn't exist
        """
        is_deleted = await self.repository.delete(saving_id)
        if not is_deleted:
            logger.warning(f"Saving not found when deleting: saving_id={saving_id}")
            raise SavingNotFoundError()
        await self.session.commit()
        logger.info(f"Saving deleted successfully: saving_id={saving_id}")
