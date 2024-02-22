from tortoise import Tortoise, run_async
from config import database_config as database, POSTGRES_HOST

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://postgres:postgres@{POSTGRES_HOST}:5432/{database.db}"
    },
    "apps": {
        "models": {
            "models": ["bot.models"],
            "default_connection": "default",
        },
    },
}


async def setup():
    await Tortoise.init(TORTOISE_ORM, _create_db=True)
    await Tortoise.generate_schemas()
