import logging
from datetime import datetime

from app.schemas.category import CategoryDTO
from app.enums import TransactionType
from app.repositories import CategoryRepository, UserRepository
from app.exceptions.category import CategoryNotFoundError, CategoryAlreadyExistsError
from app.exceptions.user import UserNotFoundError


logger = logging.getLogger(__name__)

class CategoryService:
    """Service for managing transaction categories.
    
    This service handles all operations related to categories:
    - Creating new categories (personal or global)
    - Retrieving categories available to users
    - Updating category details
    - Deleting categories
    
    Categories can be personal (belonging to a specific user) or global
    (available to all users). Global categories have user_id = None.
    """
    
    def __init__(self, session):
        self.session = session
        self.repository = CategoryRepository(session)
        self.user_repository = UserRepository(session)
    
    async def create(
        self,
        user_id: int,
        name: str,
        transaction_type: TransactionType,
        created_at: datetime | None = None
    ) -> CategoryDTO:
        """Create a new category for a user.
        
        Args:
            user_id: ID of the user who will own this category
            name: Category name (must be unique for this user)
            transaction_type: Type of transactions (income/expense)
            created_at: Optional creation timestamp
            
        Returns:
            CategoryDTO: Created category data
            
        Raises:
            CategoryAlreadyExistsError: If user already has a category with this name
            UserNotFoundError: If user with given ID doesn't exist
            
        Example:
            >>> category = await category_service.create(
            ...     user_id=1,
            ...     name="Groceries",
            ...     transaction_type=TransactionType.EXPENSE
            ... )
        """
        existing = await self.repository.exists(name=name, user_id=user_id)
        
        if existing:
            logger.warning(
                f"Attempt to create duplicate category: "
                f"user_id={user_id}, name={name}"
            )
            raise CategoryAlreadyExistsError(
                f"Category with name '{name}' already exists for this user"
            )
        
        existing_user = await self.user_repository.exists(id=user_id)
        
        if not existing_user:
            logger.warning(f"User not found when creating category: user_id={user_id}")
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        category = await self.repository.create(
            user_id=user_id,
            name=name,
            transaction_type=transaction_type,
            created_at=created_at
        )
        await self.session.commit()
        
        logger.info(
            f"Category created successfully: "
            f"id={category.id}, user_id={user_id}, "
            f"name={name}, type={transaction_type.value}"
        )
        
        return CategoryDTO.model_validate(category)

    async def get_available_for_user_and_type(
        self,
        user_id: int,
        transaction_type: TransactionType
    ) -> list[CategoryDTO]:
        """Get all categories available to a user for a specific transaction type.
        
        This includes:
        - User's personal categories of the specified type
        - Global categories of the specified type
        
        Args:
            user_id: ID of the user
            transaction_type: Type of transactions (income/expense)
            
        Returns:
            list[CategoryDTO]: List of available categories
            
        Raises:
            UserNotFoundError: If user with given ID doesn't exist
            
        Example:
            >>> expense_categories = await category_service.get_available_for_user_and_type(
            ...     user_id=1,
            ...     transaction_type=TransactionType.EXPENSE
            ... )
            >>> for cat in expense_categories:
            ...     print(f"{cat.name} ({'global' if cat.user_id is None else 'personal'})")
        """
        existing_user = await self.user_repository.exists(id=user_id)
        
        if not existing_user:
            logger.warning(
                f"User not found when getting available categories: user_id={user_id}"
            )
            raise UserNotFoundError(f"User with id {user_id} not found")
        
        categories = await self.repository.get_available_for_user_and_type(
            user_id=user_id,
            transaction_type=transaction_type
        )
        
        logger.info(
            f"Retrieved {len(categories)} categories for user {user_id} "
            f"with type {transaction_type.value}"
        )
        
        return list(map(CategoryDTO.model_validate, categories))
    
    async def update(
        self,
        category_id: int,
        name: str | None = None,
        transaction_type: TransactionType | None = None
    ) -> CategoryDTO:
        """Update an existing category.
        
        Only provided fields will be updated. This method is useful for
        renaming categories or changing their type.
        
        Args:
            category_id: ID of the category to update
            name: New category name (if changing)
            transaction_type: New transaction type (if changing)
            
        Returns:
            CategoryDTO: Updated category data
            
        Raises:
            CategoryNotFoundError: If category with given ID doesn't exist
            CategoryAlreadyExistsError: If trying to rename to an already existing name
            
        Example:
            >>> # Rename a category
            >>> updated = await category_service.update(
            ...     category_id=1,
            ...     name="Supermarket"  # was "Groceries"
            ... )
            >>> await session.commit()
        """
        existing_category = await self.repository.get_by_id(category_id)
        if existing_category is None:
            logger.warning(f"Category not found when updating: category_id={category_id}")
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        update_data = {}
        
        if name is not None and name != existing_category.name:
            name_exists = await self.repository.exists(
                user_id=existing_category.user_id,
                name=name
            )
            if name_exists:
                logger.warning(
                    f"Attempt to rename to existing category name: "
                    f"category_id={category_id}, new_name={name}, "
                    f"user_id={existing_category.user_id}"
                )
                raise CategoryAlreadyExistsError(
                    f"Category with name '{name}' already exists for this user"
                )
            update_data["name"] = name
        
        if transaction_type is not None and transaction_type != existing_category.transaction_type:
            update_data["transaction_type"] = transaction_type
        
        if not update_data:
            logger.info(f"No updates provided for category {category_id}")
            return CategoryDTO.model_validate(existing_category)
        
        updated_category = await self.repository.update(
            category_id=category_id,
            **update_data
        )
        
        if updated_category is None:
            logger.warning(f"Category not found during update: category_id={category_id}")
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        await self.session.commit()
        
        updated_fields = ', '.join(update_data.keys())
        logger.info(
            f"Category updated successfully: "
            f"id={category_id}, updated_fields=[{updated_fields}], "
            f"new_name={updated_category.name}, "
            f"new_type={updated_category.transaction_type.value}"
        )
        
        return CategoryDTO.model_validate(updated_category)

    async def delete(self, category_id: int) -> None:
        """Delete a category permanently.
        
        Args:
            category_id: ID of the category to delete
            
        Raises:
            CategoryNotFoundError: If category with given ID doesn't exist
            
        Example:
            >>> try:
            ...     await category_service.delete(1)
            ...     print("Category deleted")
            ... except CategoryNotFoundError:
            ...     print("Category not found")
            
        Warning:
            This operation is irreversible!
        """
        is_deleted = await self.repository.delete(category_id)
        
        if not is_deleted:
            logger.warning(f"Category not found when deleting: category_id={category_id}")
            raise CategoryNotFoundError(f"Category with id {category_id} not found")
        
        await self.session.commit()
        
        logger.info(f"Category deleted successfully: category_id={category_id}")