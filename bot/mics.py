import asyncio
from loguru import logger

from config import bot_config, REDIS_HOST
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis, DefaultKeyBuilder, RedisEventIsolation

loop = asyncio.get_event_loop()

logger.error(f"Redis running on {REDIS_HOST}")
storage = RedisStorage(
    Redis(host=REDIS_HOST, port=6379),
    key_builder=DefaultKeyBuilder(with_destiny=True)
)
storage = MemoryStorage()
bot = Bot(token=bot_config.token)
dp = Dispatcher(bot=bot, loop=loop, storage=storage,
                events_isolation=RedisEventIsolation(redis=Redis(host=REDIS_HOST, port=6379)))


async def setup():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
