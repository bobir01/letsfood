from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _


def getbacket():
    return ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(_("Back ⬅️"))],
        [KeyboardButton(_("Basket 🛒"))]
    ],
    resize_keyboard=True
)
