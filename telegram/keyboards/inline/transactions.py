from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_transaction_type_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Доход", callback_data="income")
    builder.button(text="Трата", callback_data="expense")
    builder.button(text="В копилку", callback_data="deposit")
    builder.button(text="Из копилки", callback_data="withdrawal")
    builder.adjust(1)
    return builder.as_markup()