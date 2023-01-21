from typing import Tuple, Any, Optional

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from data.config import LOCALES_DIR, I18N_DOMAIN
from utils.db_api.postgresql import Database

db_m = Database()


async def get_lang(user_id):
    return await db_m.get_lang(user_id)


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        lang = await get_lang(user.id)

        return lang or user.locale  # get_lang(user.id) # or user.locale


i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
