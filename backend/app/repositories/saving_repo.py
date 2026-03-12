from datetime import date, datetime

from app.models import Saving
from .base_repo import BaseRepository


class SavingRepository(BaseRepository[Saving]):
    """
    Repository for Savings model operations.

    Inherits common CRUD operations from BaseRepository.

    Attributes:
        session: SQLAlchemy async session
    """

    def __init__(self, session):
        super().__init__(session, Saving)

    async def create(
        self,
        user_id: int,
        name: str,
        final_amount: int,
        deadline: date | None = None,
        created_at: datetime | None = None,
    ) -> Saving:
        """Create a new savings goal.

        Args:
            user_id: ID of the user who owns this saving.
            name: Name of the savings goal (e.g., "New Car", "Vacation", "Emergency Fund").
            final_amount: Target amount to save in minor units (e.g., 1000000 = 10,000.00).
            deadline: Optional target date to achieve the goal.
            created_at: Optional creation date. If None, database sets current date.

        Returns:
            Saving: Created saving instance.
        """
        return await super()._create(
            user_id=user_id,
            name=name,
            final_amount=final_amount,
            deadline=deadline,
            created_at=created_at,
        )

    async def get_by_user_id(self, user_id: int) -> list[Saving]:
        """Get all savings goals for a specific user.

        Args:
            user_id: ID of the user.

        Returns:
            list[Saving]: List of user's savings goals (empty list if none).

        Note:
            Always returns a list even if no savings exist.
        """
        return await self._get_many(user_id=user_id)

    async def get_active(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Saving]:
        """Get active (not completed) savings goals for a user.

        Args:
            user_id: ID of the user.
            skip: Number of records to skip (for pagination).
            limit: Maximum number of records to return.

        Returns:
            list[Saving]: List of active savings.

        Note:
            Completed savings (is_completed=True) are excluded.
            Results are ordered by deadline (soonest first).
        """
        return await self._get_many(
            user_id=user_id,
            is_completed=False,
            order_by="deadline",
            skip=skip,
            limit=limit,
        )

    async def update(
        self,
        saving_id: int,
        name: str | None = None,
        final_amount: int | None = None,
        deadline: date | None = None,
        is_completed: bool | None = None,
    ) -> Saving | None:
        """Update savings goal details.

        This is a general-purpose update method for modifying multiple fields at once.
        Only provided fields are updated.

        Args:
            saving_id: ID of the saving to update.
            name: New name (if changing).
            final_amount: New target amount (if changing).
            deadline: New deadline (if changing).
            is_completed: New completion status (if changing).

        Returns:
            Saving | None: Updated saving instance or None if not found.

        Note:
            If no fields are provided for update, returns the existing saving unchanged.
            Does NOT commit transaction — call session.commit() separately.
        """
        saving = await self.get_by_id(saving_id)

        if not saving:
            return None

        update_data = {
            "name": name,
            "final_amount": final_amount,
            "deadline": deadline,
            "is_completed": is_completed,
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            return saving

        return await self._update(saving, **update_data)

    async def update_name(self, saving_id: int, name: str) -> Saving | None:
        """Update only the name of a savings goal.
        Args:
            saving_id: ID of the saving to update.
            name: New name for the saving.

        Returns:
            Saving | None: Updated saving or None if not found.
        """
        saving = await self.get_by_id(saving_id)

        if not saving:
            return None

        return await self._update(saving, name=name)

    async def update_deadline(self, saving_id: int, deadline: date) -> Saving | None:
        """Update only the deadline of a savings goal.

        Args:
            saving_id: ID of the saving to update.
            deadline: New deadline date.

        Returns:
            Saving | None: Updated saving or None if not found.
        """
        saving = await self.get_by_id(saving_id)

        if not saving:
            return None

        return await self._update(saving, deadline=deadline)

    async def mark_completed(self, saving_id: int) -> Saving | None:
        """Mark a savings goal as completed.

        Args:
            saving_id: ID of the saving to mark as completed.

        Returns:
            Saving | None: Updated saving or None if not found.

        Note:
            Sets is_completed=True.
        """
        saving = await self.get_by_id(saving_id)

        if not saving:
            return None

        return await self._update(saving, is_completed=True)

    async def delete(self, saving_id: int) -> bool:
        """Delete a savings goal.

        Args:
            saving_id: ID of the saving to delete.

        Returns:
            bool: True if deleted, False if saving not found.

        Note:
            This performs a hard delete. Consider soft delete if you need history.
        """
        saving = await self.get_by_id(saving_id)

        if not saving:
            return False

        await self._delete(saving)

        return True
