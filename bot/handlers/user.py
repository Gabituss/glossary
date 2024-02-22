from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from bot.controllers import user
from bot.dialogs.states import UserMenuSG

from aiogram_dialog import DialogManager, ShowMode, StartMode


async def command_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserMenuSG.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)
    await user.create_user(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username
    )


async def command_me(message: Message):
    user_id = message.from_user.id
    try:
        _user = await user.get(user_id)
        await message.answer(f"You are joined {_user.join_date}")
    except ValueError:
        await message.answer("You are not registered!")


def setup(dp: Dispatcher):
    dp.message.register(command_start, Command("start"))
    dp.message.register(command_me, Command("me"))
