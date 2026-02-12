import logging

from aiogram import Router
from aiogram.types.message import Message
from aiogram.types.callback_query import CallbackQuery

from api.user import register_user
from keyboards.reply import get_main_kb
from keyboards.inline import CurrenciesData
from strings.messages import POST_REGISTRATION_TEXT
from strings.errors import MESSAGE_NOT_FOUND_TEXT, MESSAGE_NOT_UNAVAILABLE_TEXT, REGISTRATION_ERROR_TEXT


router = Router(name="currency_router")
logger = logging.getLogger(__name__)


@router.callback_query(CurrenciesData.filter())
async def handle_currency(
    callback: CallbackQuery,
    callback_data: CurrenciesData
):
    
    if not callback.message:
        await callback.answer(MESSAGE_NOT_FOUND_TEXT)
        return
    
    if not isinstance(callback.message, Message):
        await callback.answer(MESSAGE_NOT_UNAVAILABLE_TEXT)
        return
    
    currency_id = callback_data.id
    user = await register_user(
        tg_id=callback.from_user.id,
        currency_id=currency_id
    )
    await callback.message.delete()
    if user:
        logger.info(
            f"User registered successfully | "
            f"tg_id={callback.from_user.id} | "
            f"currency_id={currency_id} | "
            f"user_id={user.get('id')}"
        ) 
        await callback.message.answer(
            text=POST_REGISTRATION_TEXT,
            reply_markup=get_main_kb()
        )
        await callback.answer()
    else:
        logger.error(
            f"User registration failed | "
            f"tg_id={callback.from_user.id} | "
            f"currency_id={currency_id}"
        )
        await callback.message.answer(REGISTRATION_ERROR_TEXT)
        await callback.answer()