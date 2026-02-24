import logging
from datetime import datetime
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from api.saving import create_saving
from states import CreateSavingState

router = Router(name="saving_router")
logger = logging.getLogger(__name__)


@router.message(Command("create_piggy"))
async def create_piggy_interactive(message: Message, state: FSMContext):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.set_state(CreateSavingState.name)
    await message.answer("Введите имя для копилки:")

@router.message(CreateSavingState.name)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(CreateSavingState.final_amount)
    await message.answer("Введите сумму, которую хотите накопить:")

@router.message(CreateSavingState.final_amount)
async def process_final_amount(message: Message, state: FSMContext):
    if not message.text:
        return
    final_amount = float(message.text)
    await state.update_data(final_amount=final_amount)
    await state.set_state(CreateSavingState.deadline)
    await message.answer("Введите дату до который вы хотите накопить")

@router.message(CreateSavingState.deadline)
async def process_deadline(message: Message, state: FSMContext):
    if not message.text:
        return
    try:
        deadline = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
        await state.update_data(deadline=deadline)
        await complete_create_saving(state)
        await message.answer("Копилка успешно создана\\!")
    except Exception as e:
        print(e)
        return


async def complete_create_saving(
    state: FSMContext
):
    data = await state.get_data()
    try:
        await create_saving(
            user_tg_id=data["user_tg_id"],
            name=data["name"],
            final_amount=data["final_amount"],
            deadline=data["deadline"]
        )
    except Exception as e:
        print(e)
    finally:
        await state.clear()
