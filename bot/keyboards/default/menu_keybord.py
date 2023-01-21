from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _



def make_numbers():
    menu = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    buttons = []
    for i in range(1, 10):
        if i % 3 == 0:
            buttons.append(KeyboardButton(text=str(i)))
            menu.add(*buttons)
            buttons.clear()
            continue
        buttons.append(KeyboardButton(text=str(i)))
    menu.add(KeyboardButton(_("Back ⬅️")))
    return menu
