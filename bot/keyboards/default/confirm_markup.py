from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _


def get_confrim_markup():
    car = _("Confirm order 🚖")
    back = _("Back ⬅️")
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(car)],
            [KeyboardButton(back)]
        ]
    )
    return markup
