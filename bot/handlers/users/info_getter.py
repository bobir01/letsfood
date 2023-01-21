import asyncio
import logging
from . import main_handler
from aiogram.types import Message, CallbackQuery, ForceReply, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.menu_keybord import make_numbers
from keyboards.default.main_keyboard import make_menu, address_markup
from keyboards.inline.food_inline_keyboard import make_food_markup
from keyboards.inline.lang_inline_keyboard import lang_inline, lang_call
from loader import dp, db, _, bot




@dp.message_handler(Text(contains="ℹ️"), state="*")
async def info_handler(message: Message, state: FSMContext = None):
    await message.answer(_("""📌Here you can find information about our restaurant📌    
📍Address: 1000, Tashkent, Yunusobod district, Mirzo Ulugbek street, 2
📞Phone number: +998 71 200 00 00
📧Email:bistro@akfauniversity.org
🕐Working hours: 10:00 - 22:00
📅Days off: Sunday
🚗Delivery: Yes
🍽️Cuisine: European, Uzbek
    """), reply_markup=make_menu())