from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters.command import Command

from strings.messages import HELP_TEXT
from keyboards.reply import get_main_kb


router = Router(name="help_router")

@router.message(Command("help"))
async def help_start(message: Message) -> None:
    await message.answer(
        text=HELP_TEXT,
        reply_markup=get_main_kb()
        )
