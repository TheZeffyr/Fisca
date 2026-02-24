from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from api.saving import get_savings_by_user_tg_id
from keyboards.inline import get_savings_pg_kb

router = Router(name="saving_view_router")


@router.message(F.text == "Мои копилки")
@router.message(Command("piggy"))
async def create_piggy_interactive(message: Message, state: FSMContext):
    savings = await get_savings_by_user_tg_id(message.from_user.id)
    await message.answer(
        text="Ваши копилки:",
        reply_markup=get_savings_pg_kb(savings)
    )