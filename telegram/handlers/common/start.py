import logging

from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters.command import CommandStart

from strings.messages import START_TEXT
from keyboards.reply import get_main_kb


router = Router(name="start_router")
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    logger.info("User %s started bot", message.from_user.id)
    await message.answer(
        text=START_TEXT,
        reply_markup=get_main_kb()
        )
