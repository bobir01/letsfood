from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import dp, db, _


def contact_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(_("Share your contact 📞"), request_contact=True)],
            [KeyboardButton(_("Back ⬅️"))]],
        resize_keyboard=True
    )
