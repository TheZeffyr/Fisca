from datetime import datetime

from app.models import Category
from app.enums import TransactionType
from app.repositories import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model operations.

    Categories are used to classify transactions (income/expense). They can be:
    - Personal: Owned by a specific user (user_id = user.id) - created by users
    - Global: Available to all users (user_id = NULL) - system defaults

    Attributes:
        session: SQLAlchemy async session
    """

    def __init__(self, session):
        super().__init__(session, Category)

    async def create(
        self,
        user_id: int | None,
        name: str,
        transaction_type: TransactionType,
        created_at: datetime | None = None,
    ) -> Category:
        """Create a new personal category for a user.

        Args:
            user_id: ID of the user who will own this category
            name: Category name (e.g., "Food", "Salary", "Transport")
            transaction_type: Type of transactions this category is for
                            (income or expense)

        Returns:
            Category: Created category instance
        """
        return await self._create(
            user_id=user_id,
            name=name,
            transaction_type=transaction_type,
            created_at=created_at
        )

    async def get_global(self) -> list[Category]:
        """Get all global categories (available to all users).

        Global categories have user_id = NULL and serve as defaults
        for all users.

        Returns:
            list[Category]: List of global categories
        """
        return await self._get_many(user_id=None)

    async def get_by_user(self, user_id: int) -> list[Category]:
        """Get personal categories created by a specific user.

        Args:
            user_id: ID of the user

        Returns:
            list[Category]: List of user's personal categories
        """
        return await self._get_many(user_id=user_id)

    async def get_available_for_user(self, user_id: int) -> list[Category]:
        """Get all categories available to a specific user.

        This includes:
        - User's personal categories (created by them)
        - Global categories (available to everyone)

        This is the main method to get categories for transaction forms,
        dropdowns, and category selection interfaces.

        Args:
            user_id: ID of the user

        Returns:
            list[Category]: Combined list of personal and global categories,
                          sorted by transaction type and name
        """
        personal_categories = await self._get_many(user_id=user_id)
        global_categories = await self._get_many(user_id=None)
        return personal_categories + global_categories

    async def get_by_user_and_type(
        self,
        user_id: int,
        transaction_type: TransactionType,
        skip: int = 0,
        limit: int = 100
    ) -> list[Category]:
        """Get personal categories for a user filtered by transaction type.

        Args:
            user_id: ID of the user
            transaction_type: Type of transactions (income or expense)

        Returns:
            list[Category]: User's categories of the specified type
        """
        return await self._get_many(
            user_id=user_id,
            transaction_type=transaction_type,
            skip=skip,
            limit=limit
        )
    

    async def get_available_by_user_and_type(
        self,
        user_id: int,
        transaction_type: TransactionType,
        skip: int = 0,
        limit: int = 100
    ) -> list[Category]:
        """Get all categories available to a user for a specific transaction type.

        Args:
            user_id: ID of the user
            transaction_type: Type of transaction (income or expense)

        Returns:
            list[Category]: Combined list of personal and global categories of the specified type
        """
        personal_categories = await self.get_by_user_and_type(
            user_id=user_id,
            transaction_type=transaction_type,
            skip=skip,
            limit=limit
        )
        global_categories = await self._get_many(
            user_id=None,
            transaction_type=transaction_type,
            skip=skip,
            limit=limit
        )
        return personal_categories + global_categories

    async def update(
        self,
        category_id: int,
        name: str | None = None,
        transaction_type: str | None = None,
    ) -> Category | None:
        """Update an existing category.

        Only provided fields will be updated. This method is useful for
        editing category details without affecting other properties.

        Args:
            category_id: ID of the category to update
            name: New category name (if changing)
            transaction_type: New transaction type (if changing)

        Returns:
            Optional[Category]: Updated category or None if not found
        """
        category = await self.get_by_id(category_id)
        if category is None:
            return None
        
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if transaction_type is not None:
            update_data["transaction_type"] = transaction_type

        if not update_data:
            return category

        return await self._update(category, **update_data)

    async def delete(self, category: Category) -> None:
        """Delete a category permanently.

        Warning: Only use if currency has no associated transactions/users.
        Consider soft delete (deactivate) instead.

        Args:
            category_id: ID of the category to delete
        """
        await self._delete(category)
