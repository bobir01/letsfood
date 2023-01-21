import logging

from aiogram import executor

from data.config import *
from loader import dp, db_m, db, _, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8000


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    await db_m.create() # for language db pool
    await db.create()
    await db.create_table_users()
    await db.create_table_basket()


    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


async def on_shutdown(dp):
    logging.warning('Shutting down..')


    await bot.delete_webhook()


    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    if IS_WEBHOOK is False:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    else:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host='localhost',
            port=3232
        )
