from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares.lang_midlware import i18n
from middlewares.throttling import ThrottlingMiddleware
from data import config
from utils.db_api.postgresql import Database
from middlewares.lang_midlware import db_m
def setup_middleware(dp):
    print("middleware set")
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(i18n)


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
setup_middleware(dp)
db = Database()
_ = i18n.gettext
