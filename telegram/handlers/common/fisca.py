from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters.command import Command

from strings.messages import FISCA_TEXT
from keyboards.reply import get_main_kb


router = Router(name="fisca_router")


@router.message(Command("fisca"))
async def cmd_fisca(message: Message) -> None:
    await message.answer(
        text=FISCA_TEXT,
        reply_markup=get_main_kb()
        )
