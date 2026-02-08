from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from strings.buttons import MAIN_MENU_TEXT

def get_main_kb() -> ReplyKeyboardMarkup:
    """
    Creates the main menu keyboard for the user.
    
    Uses the button texts from the MAIN_MENU constant, which should contain
    a list of lines with texts for buttons.

    Returns:
        ReplyKeyboardMarkup: Ready-made keyboard with main menu buttons
    """
    builder = ReplyKeyboardBuilder()
    for text in MAIN_MENU_TEXT:
        builder.button(text=text)

    builder.adjust(2,3)
    return builder.as_markup()
