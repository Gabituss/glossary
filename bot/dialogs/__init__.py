from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from bot.dialogs.user import main_user_dialog, document_adding_dialog


async def setup(dp: Dispatcher):
    dp.include_router(main_user_dialog)
    dp.include_router(document_adding_dialog)

    setup_dialogs(dp)
