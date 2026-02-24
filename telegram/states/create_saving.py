from aiogram.fsm.state import State, StatesGroup

class CreateSavingState(StatesGroup):
    user_tg_id = State()
    name = State()
    final_amount = State()
    deadline = State()
