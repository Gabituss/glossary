from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.controllers import field, template, user
from bot.dialogs.states import UserMenuSG, AddDocumentSG


async def select_template(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await dialog_manager.start(AddDocumentSG.main, data={
        "template_id": int(item_id)
    })


async def select_input_field(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data.update(input_id=item_id)
    await dialog_manager.switch_to(AddDocumentSG.input)


async def handle_input_field(event: Any, widget: Any, dialog_manager: DialogManager, *_):
    value = dialog_manager.find("input").get_value()
    field_id = dialog_manager.dialog_data.get("field_id")
    input_id = dialog_manager.dialog_data.get("input_id")

    _field = await field.get(field_id)
    if not _field.check_string(value):
        await event.answer("Неправильный формат :(")
    else:
        dialog_manager.dialog_data["input"] = dialog_manager.dialog_data.get("input", {})
        dialog_manager.dialog_data["input"][input_id] = value
        await dialog_manager.switch_to(AddDocumentSG.main)
