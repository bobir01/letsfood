import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(user_id=message.from_user.id)

    await message.answer("Xush kelibsiz!")

    count = await db.count_users()
    msg = f"{user[1]} added to db.\nIn db {count} users"
    await bot.send_message(chat_id=ADMINS[0], text=msg)
