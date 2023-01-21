import logging
import os
import sys

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "bot is alive")
            # trying to compile all translations
            os.system('pybabel compile -d locales -D bistro')
            await dp.bot.send_message(admin, 'All translations successfully complied')
            logging.info('All translations successfully complied')

        except Exception as err:
            logging.exception(err)
