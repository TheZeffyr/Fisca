from aiogram.filters.callback_data import CallbackData

class CurrenciesData(CallbackData, prefix="cur"):
    id: int

