from aiogram.fsm.state import State, StatesGroup

class CreateTransactionState(StatesGroup):
    transaction_type = State()
    category_id = State()
    amount = State()
    date_time = State()
