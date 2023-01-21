from environs import Env
from pathlib import Path

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
IS_WEBHOOK = env.bool("IS_WEBHOOK")
WEBHOOK_HOST = env.str("WEBHOOK_HOST")
WEBHOOK_PATH = '' #env.str("WEBHOOK_PATH", '')
WEBHOOK_URL = WEBHOOK_HOST+WEBHOOK_PATH

I18N_DOMAIN = 'bistro'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'
GROUP_ID = '-1001793359105'



DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
