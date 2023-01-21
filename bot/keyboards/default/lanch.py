from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _



def make_event_keyboard(lang=None):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(_("Lunch🍲")), KeyboardButton(_("Dinner🍽"))],
            [KeyboardButton(_("Back ⬅️"))]
        ]
    )
    return markup
