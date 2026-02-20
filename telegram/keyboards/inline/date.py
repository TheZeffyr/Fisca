from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_dates_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вчера", callback_data="date:yesterday"),
            ],
            [
                InlineKeyboardButton(text="Сегодня", callback_data="date:today")
            ],
            [
                InlineKeyboardButton(text="Завтра", callback_data="date:tomorrow")
            ],
            [
                InlineKeyboardButton(
                    text="Ввести вручную",
                    callback_data="date:custom"
                )
            ]
        ]
    )