from aiogram.filters.callback_data import CallbackData

class CategoryData(CallbackData, prefix="cat"):
    id: int

