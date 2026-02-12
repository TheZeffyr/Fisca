from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types.message import Message

from api.currency import get_all_currencies
from keyboards.inline import PaginationData, get_currencies_pg_kb
from strings.errors import MESSAGE_NOT_FOUND_TEXT, MESSAGE_NOT_UNAVAILABLE_TEXT


router = Router(name="pagination_router")

@router.callback_query(PaginationData.filter())
async def handle_currency(
    callback: CallbackQuery,
    callback_data: PaginationData
):
    page = callback_data.page
    prefix = callback_data.prefix
    if not callback.message:
        await callback.answer(MESSAGE_NOT_FOUND_TEXT)
        return
    
    if not isinstance(callback.message, Message):
        await callback.answer(MESSAGE_NOT_UNAVAILABLE_TEXT)
        return
    
    currencies = await get_all_currencies()
    
    try:
        if prefix == "cur":
            await callback.message.edit_reply_markup(
                reply_markup=get_currencies_pg_kb(
                    currencies=currencies,
                    page=page
                )
            )
        await callback.answer()        
    except Exception as e:
        await callback.answer(f"❌ Ошибка: {str(e)[:20]}...")#TODO: Довести до нормального вида