import logging

from bot.dialogs.states import UserMenuSG

from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(UserMenuSG.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog %s", event.exception)
    await dialog_manager.start(UserMenuSG.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


def setup(dp: Dispatcher):
    dp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    dp.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))
