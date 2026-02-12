from aiogram.filters.callback_data import CallbackData


class PaginationData(CallbackData, prefix="pag"):
    page: int
    prefix: str