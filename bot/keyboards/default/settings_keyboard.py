from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _


def make_settings(lang=None):
    if lang:
        settings = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(_("Change name ✏️", locale=lang))],
                [KeyboardButton(_("Change phone 📱", locale=lang))],
                [KeyboardButton(_("Change language 🇺🇿", locale=lang))],
                [KeyboardButton(_("Back ⬅️", locale=lang))],
            ],
            resize_keyboard=True
        )
        return settings

    settings = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(_("Change name ✏️"))],
            [KeyboardButton(_("Change phone 📱"))],
            [KeyboardButton(_("Change language 🇺🇿",))],
            [KeyboardButton(_("Back ⬅️"))],
        ],
        resize_keyboard=True
    )
    return settings