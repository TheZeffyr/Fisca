from aiogram.filters.callback_data import CallbackData

class SavingData(CallbackData, prefix="piggy"):
    id: int

