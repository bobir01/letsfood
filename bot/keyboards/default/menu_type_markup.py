from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _


def make_menu_type_keyboard(lang=None):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(_("Full set")), KeyboardButton(_("Partial set"))],
            [KeyboardButton(_("Back ⬅️"))]
        ]
    )
    return markup
