from datetime import date, timedelta, datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from strings.messages import SELECT_TRANSACTION_TYPE, INPUT_AMOUNT, SELECT_CATEGORY, SELECT_DATETIME, INPUT_DATETIME, TRANSACTION_CREATED
from strings.errors import INVALID_DATE_FORMAT
from keyboards.inline import get_transaction_type_kb, get_categories_pg_kb, CategoryData, get_dates_kb, get_savings_pg_kb, SavingData
from states import CreateTransactionState
from api.category import get_categories_by_filters
from api.transaction import create_transaction
from api.saving import get_savings_by_user_tg_id

router = Router(name="add_transaction_router")

@router.message(F.text == "Добавить транзакцию")
@router.message(Command("add"))
async def add_transaction_interactive(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CreateTransactionState.transaction_type)
    await message.answer(
        text=SELECT_TRANSACTION_TYPE,
        reply_markup=get_transaction_type_kb()
    )

@router.callback_query(
    CreateTransactionState.transaction_type,
    F.data.in_({"income", "expense", "deposit", "withdrawal"})
)
async def process_transaction_type(
    callback: CallbackQuery,
    state: FSMContext
):
    if not callback.message:
        return
    
    transaction_type = callback.data
    await state.update_data(transaction_type=transaction_type)
    if transaction_type in ["deposit", "withdrawal"]:
        await state.set_state(CreateTransactionState.saving_id)
        await callback.answer()
        savings = await get_savings_by_user_tg_id(callback.from_user.id)
        await callback.message.answer(
            text="Выберите копилку:",
            reply_markup=get_savings_pg_kb(savings)
        )
    else:
        await state.set_state(CreateTransactionState.amount)
        await callback.answer()
        await callback.message.answer(
            text=INPUT_AMOUNT
        )

@router.callback_query(SavingData.filter(), CreateTransactionState.saving_id)
async def process_saving(callback: CallbackQuery, callback_data: SavingData, state: FSMContext):
    if not callback.message:
        return
    saving_id = callback_data.id
    await state.update_data(saving_id=saving_id)
    await state.set_state(CreateTransactionState.amount)
    await callback.message.answer(INPUT_AMOUNT)

@router.message(CreateTransactionState.amount)
async def process_amount(
    message: Message,
    state: FSMContext
):
    if not message.text:
        return
    amount = abs(float(message.text.replace(',', '.')))
    await state.update_data(amount=amount)
    user_tg_id = message.from_user.id
    transaction_type = await state.get_value("transaction_type")
    if not transaction_type:
        return
    categories = await get_categories_by_filters(
        user_tg_id=user_tg_id,
        transaction_type=transaction_type
    )
    if transaction_type in ["deposit", "withdrawal"]:
        await state.set_state(CreateTransactionState.date_time)
        await message.answer(
            text=SELECT_DATETIME,
            reply_markup=get_dates_kb()
        )
    else:
        await state.set_state(CreateTransactionState.category_id)
        await message.answer(
            text=SELECT_CATEGORY,
            reply_markup=get_categories_pg_kb(categories)
        )

@router.callback_query(
    CategoryData.filter(),
    CreateTransactionState.category_id
)
async def process_category(
    callback: CallbackQuery,
    callback_data: CategoryData,
    state: FSMContext
):
    if not callback.message:
        return
    
    await state.update_data(category_id=callback_data.id)
    await state.set_state(CreateTransactionState.date_time)

    await callback.message.answer(
        text=SELECT_DATETIME,
        reply_markup=get_dates_kb()
    )

@router.callback_query(
    F.data.startswith("date:"),
    CreateTransactionState.date_time
)
async def process_datetime(
    callback: CallbackQuery,
    state: FSMContext
):
    if not callback.data or not callback.message:
        return
    
    action = callback.data.split(":")[1]
    today = date.today()
    if action == "custom":
        await callback.message.answer(
            text=INPUT_DATETIME,
        )
        await callback.answer()
        return
    elif action == "today":
        date_time = today
    elif action == "yesterday":
        date_time = today - timedelta(days=1)
    elif action == "tomorrow":
        date_time = today + timedelta(days=1)
    else:
        await callback.answer()
        return
    
    await state.update_data(date_time=date_time)
    await complete_create_transaction(callback.from_user.id, state)
    await callback.message.answer(
        text=TRANSACTION_CREATED
    )

@router.message(CreateTransactionState.date_time)
async def process_custom_datetime(
    message: Message,
    state: FSMContext
):
    if not message.text:
        return
    try:
        date_time = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
        await state.update_data(date_time=date_time)
        await complete_create_transaction(message.from_user.id, state)
        await message.answer(
            text=TRANSACTION_CREATED
        )
    except ValueError:
        await message.answer(INVALID_DATE_FORMAT)


async def complete_create_transaction(
    user_tg_id: int,
    state: FSMContext
):
    data = await state.get_data()
    try:
        await create_transaction(
            user_tg_id=user_tg_id,
            transaction_type=data['transaction_type'],
            category_id=data['category_id'],
            amount=data['amount'],
            date_time=data['date_time'],
            saving_id=data["saving_id"]
        )
    except Exception as e:
        return
    finally:
        await state.clear()