from math import ceil

from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


from .currencies_data import CurrenciesData
from .pagination_data import PaginationData

def get_currencies_pg_kb(
        currencies: list[dict[str,str]],
        item_per_page: int = 5,
        page: int = 0
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    count_correncies = len(currencies)
    count_pages = ceil(count_correncies / item_per_page)
    
    start_index = page*item_per_page
    end_index = start_index+item_per_page
    nav_buttons = []
    for currency in currencies[start_index:end_index]:
        builder.button(
            text=f"{currency["name"]} ({currency["currency_code"]})",
            callback_data=CurrenciesData(id=int(currency["id"])).pack()
        )
    if page<count_pages-1:
        nav_buttons.append(InlineKeyboardButton(
            text="Вперед",
            callback_data=PaginationData(page=page+1, prefix="cur").pack()
        ))
    nav_buttons.append(InlineKeyboardButton(
            text=f"{page+1}/{count_pages}",
            callback_data="current_page"
        ))
    if page>0:
        nav_buttons.append(InlineKeyboardButton(
            text="Назад",
            callback_data=PaginationData(page=page-1, prefix="cur").pack()
        ))
    builder.row(*nav_buttons)
    builder.adjust(1)
    return builder.as_markup()