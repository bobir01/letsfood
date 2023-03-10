from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

lang_call = CallbackData("language", "lang")


def lang_callback(lang):
    return lang_call.new(lang=lang)


lang_inline = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="English ๐บ๐ธ",callback_data=lang_callback(lang="en"))],
        [InlineKeyboardButton(text="Pัััะบะธะน ๐ท๐บ", callback_data=lang_callback(lang="ru"))],
        [InlineKeyboardButton(text="O'zbekcha ๐บ๐ฟ", callback_data=lang_callback(lang='uz'))]
    ]
)
