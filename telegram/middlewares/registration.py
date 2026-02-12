import logging
from typing import Callable, Any, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import TelegramObject, Message, CallbackQuery, User

from api.user import get_user_by_tg_id


logger = logging.getLogger(__name__)


class RegistrationMiddleware(BaseMiddleware):
    """
    Middleware that checks if a user is registered in the system.
    
    For unregistered users:
        - Intercepts the event
        - Creates FSM state
        - Sends currency selection keyboard
        - Prevents original handler execution
    
    For registered users:
        - Adds user object to data
        - Passes event to next handler
    
    Special cases:
        - Callbacks with 'cur:' and 'pag:' prefixes are always passed through
        - Non-Message/Non-Callback events are passed through
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Execute middleware logic.
        
        Args:
            handler: Next handler in chain
            event: Incoming Telegram event
            data: Context data dictionary
            
        Returns:
            Handler result or None if registration started
        """
        if not isinstance(event, (Message, CallbackQuery)):
            logger.debug(f"Skipping non-handled event type: {type(event).__name__}")
            return await handler(event, data)
        
        if isinstance(event, Message):
            from_user: User = event.from_user
            chat_id: int = event.chat.id
            event_type = "message"
        else:
            from_user: User = event.from_user
            chat_id: int = event.message.chat.id if event.message else from_user.id
            event_type = "callback"
        
        if isinstance(event, CallbackQuery) and event.data:
            if event.data.startswith("cur:") or event.data.startswith("pag:"):
                logger.debug(
                    f"Passing registration-related callback | "
                    f"tg_id={from_user.id} | "
                    f"data={event.data}"
                )
                return await handler(event, data)
        
        logger.info(
            f"Checking registration status | "
            f"tg_id={from_user.id} | "
            f"username=@{from_user.username or 'no_username'} | "
            f"event={event_type}"
        )
        
        try:
            user = await get_user_by_tg_id(from_user.id)
            data["user"] = user
            
            logger.info(
                f"User found in database | "
                f"tg_id={from_user.id} | "
                f"user_id={user.get('id')} | "
                f"currency_id={user.get('currency_id')}"
            )
            
            return await handler(event, data)
            
        except Exception as e:
            error_str = str(e)
            
            if "404" in error_str:
                logger.info(
                    f"User not found, starting registration | "
                    f"tg_id={from_user.id} | "
                    f"username=@{from_user.username or 'no_username'} | "
                    f"chat_id={chat_id}"
                )
                
                return await self.start_registration(
                    event=event,
                    data=data,
                    from_user=from_user,
                    chat_id=chat_id
                )
            else:
                logger.error(
                    f"Unexpected error while checking user | "
                    f"tg_id={from_user.id} | "
                    f"error={error_str}"
                )
                raise e
    
    async def start_registration(
        self,
        event: TelegramObject,
        data: Dict[str, Any],
        from_user: User,
        chat_id: int
    ) -> None:
        """
        Initialize registration process for new user.
        
        Creates FSM context, stores it in data, and sends currency selection.
        
        Args:
            event: Original Telegram event
            data: Context data dictionary
            from_user: Telegram user object
            chat_id: Chat ID for state key
            
        Returns:
            None - always interrupts handler chain
        """
        bot = data["bot"]
        
        storage = data.get("fsm_storage")
        if not storage:
            storage = MemoryStorage()
            data["fsm_storage"] = storage
            logger.debug("Created new MemoryStorage for FSM")
        
        state_key = StorageKey(
            bot_id=bot.id,
            chat_id=chat_id,
            user_id=from_user.id
        )
        
        state = FSMContext(storage=storage, key=state_key)
        data["state"] = state
        
        logger.debug(
            f"FSM context created | "
            f"tg_id={from_user.id} | "
            f"chat_id={chat_id} | "
            f"bot_id={bot.id}"
        )
        
        await self.request_currency(event, state, from_user)
        
        logger.info(
            f"Registration started - currency selection sent | "
            f"tg_id={from_user.id} | "
            f"username=@{from_user.username or 'no_username'}"
        )
        
        return None
    
    async def request_currency(
        self,
        event: TelegramObject,
        state: FSMContext,
        from_user: User
    ) -> None:
        """
        Send currency selection keyboard to user.
        
        Args:
            event: Original Telegram event
            state: FSM context for registration
            from_user: Telegram user object
        """
        from strings.messages import REGISTRATION_TEXT
        from api.currency import get_all_currencies
        from keyboards.inline import get_currencies_pg_kb
        
        try:
            currencies = await get_all_currencies()
            logger.debug(
                f"Fetched {len(currencies)} currencies for registration | "
                f"tg_id={from_user.id}"
            )
            
            if isinstance(event, Message):
                await event.answer(
                    text=REGISTRATION_TEXT,
                    reply_markup=get_currencies_pg_kb(currencies)
                )
                logger.debug(f"Sent registration message to {from_user.id}")
                
            elif isinstance(event, CallbackQuery) and event.message:
                await event.message.answer(
                    text=REGISTRATION_TEXT,
                    reply_markup=get_currencies_pg_kb(currencies)
                )
                await event.answer()
                logger.debug(f"Sent registration message via callback to {from_user.id}")
                
        except Exception as e:
            logger.error(
                f"Failed to send currency selection | "
                f"tg_id={from_user.id} | "
                f"error={str(e)}"
            )
            raise e