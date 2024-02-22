from aiogram import Dispatcher
from bot.handlers import user, errors, admin


async def setup(dp: Dispatcher):
    user.setup(dp)
    admin.setup(dp)
    errors.setup(dp)
