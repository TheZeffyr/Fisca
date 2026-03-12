from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.schemas.user import UserDTO, UserCreate, UserUpdate
from app.database import get_session
from app.services import UserService
from app.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from app.exceptions.currency import CurrencyNotFoundError

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create user"
)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new user in the system.

    Registers a new user with Telegram ID and preferred currency.
    The creation timestamp can be optionally provided.

    Args:
        data (UserCreate): User creation data containing:
            - tg_id (int): Unique Telegram user identifier
            - currency_id (int): ID of user's preferred currency
            - created_at (datetime, optional): Custom creation timestamp.
                If not provided, current time will be used.

    Returns:
        UserDTO: Created user data including:
            - id (int): Internal user ID
            - tg_id (int): Telegram ID
            - currency_id (int): Preferred currency ID
            - created_at (datetime): Creation timestamp

    Raises:
        HTTPException 409: If user with this tg_id already exists
            Detail: User with tg_id '{tg_id}' already exists
    """
    user_service = UserService(session)
    try:
        user = await user_service.register_user(
            tg_id=data.tg_id,
            currency_id=data.currency_id,
            created_at=data.created_at
        )
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )

@router.get(
    "/{user_id}",
    response_model=UserDTO,
    summary="Get user by id"
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a user by their internal ID.

    Args:
        user_id (int): Internal user ID (primary key in database)
        session (AsyncSession): SQLAlchemy async session (injected)

    Returns:
        UserDTO: User data including:
            - id (int): Internal user ID
            - tg_id (int): Telegram ID
            - currency_id (int): Preferred currency ID
            - created_at (datetime): Creation timestamp

    Raises:
        HTTPException 404: If user with specified ID doesn't exist
            Detail: User with id '{user_id}' not found
    """
    user_service = UserService(session)
    try:
        user = await user_service.get_user(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.get(
    "/",
    response_model=UserDTO,
    summary="Get user by telegram id"
)
async def get_user_by_tg_id(
    tg_id: int = Query(..., description="Telegram ID"),
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a user by their Telegram ID.

    This endpoint uses query parameter for searching by Telegram ID.
    Example: GET /users?tg_id=123456789

    Args:
        tg_id (int): Telegram user ID (required query parameter)
        session (AsyncSession): SQLAlchemy async session (injected)

    Returns:
        UserDTO: User data including:
            - id (int): Internal user ID
            - tg_id (int): Telegram ID
            - currency_id (int): Preferred currency ID
            - created_at (datetime): Creation timestamp

    Raises:
        HTTPException 404: If user with specified Telegram ID doesn't exist
            Detail: User with tg_id '{tg_id}' not found
    """
    user_service = UserService(session)
    try:
        user = await user_service.get_user_by_tg_id(tg_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.patch(
    "/{user_id}",
    response_model=UserDTO,
    summary="Update fields for user"
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update specific fields of an existing user.

    Currently supports updating:
    - currency_id: Change user's preferred currency

    Only provided fields will be updated (partial update).

    Args:
        user_id (int): Internal user ID
        data (UserUpdate): Update data containing:
            - currency_id (int, optional): New currency ID
        session (AsyncSession): SQLAlchemy async session (injected)

    Returns:
        UserDTO: Updated user data

    Raises:
        HTTPException 404: If user doesn't exist
            Detail: User with id '{user_id}' not found
        HTTPException 404: If specified currency doesn't exist
            Detail: Currency with id '{currency_id}' not found
    """
    user_service = UserService(session)
    try:
        user = await user_service.update_user(
            user_id=user_id,
            **data.model_dump(exclude_unset=True)
        )
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except CurrencyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleted user"
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a user from the system.

    Permanently removes user from database.
    Returns 204 No Content on success.

    Args:
        user_id (int): Internal user ID to delete
        session (AsyncSession): SQLAlchemy async session (injected)

    Raises:
        HTTPException 404: If user with specified ID doesn't exist
            Detail: User with id '{user_id}' not found
    """
    user_service = UserService(session)
    try:
        await user_service.delete_user(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )