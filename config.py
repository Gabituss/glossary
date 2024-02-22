import configparser
import os
from dataclasses import dataclass


@dataclass
class Bot:
    token: str
    admin_id: int


@dataclass
class Logging:
    logfile: str


@dataclass
class Database:
    user: str
    password: str
    host: str
    port: int
    db: str


config_parser = configparser.ConfigParser()
config_parser.read("bot.ini")

tg_bot = config_parser["tg_bot"]
logging = config_parser["logging"]
bot_config = Bot(
    token=tg_bot.get("token"),
    admin_id=tg_bot.get("admin_id")
)
logging_config = Logging(
    logfile=logging.get("logfile")
)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
database_config = Database(**config_parser["db"])
