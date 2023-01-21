from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

lang_call = CallbackData("language", "lang")


def lang_callback(lang):
    return lang_call.new(lang=lang)


lang_inline = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="English 🇺🇸",callback_data=lang_callback(lang="en"))],
        [InlineKeyboardButton(text="Pусский 🇷🇺", callback_data=lang_callback(lang="ru"))],
        [InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data=lang_callback(lang='uz'))]
    ]
)
