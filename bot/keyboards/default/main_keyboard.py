from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _




def make_menu(lang=None):
    if lang:
        menu = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(_("Order 🛍", locale=lang))],
                [KeyboardButton(_("Info ℹ️", locale=lang))],
                [KeyboardButton(_("Settings⚙️", locale=lang))],
            ],
            resize_keyboard=True
        )
        return menu
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(_("Order 🛍"))],
            [KeyboardButton(_("Info ℹ️"))],
            [KeyboardButton(_("Settings⚙️"))],
        ],
        resize_keyboard=True
    )
    return menu


def address_markup(confrim=False):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(_("Share your location📍"), request_location=True)],
            [KeyboardButton(_("Back ⬅️"))]
        ]
    )
    if confrim:
        markup.add(KeyboardButton(_("Confirm address✅")), KeyboardButton(_("Comment to address (optional)")))

        return markup

    return markup
