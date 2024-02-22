from loguru import logger

from bot.models import Template, Field, User
from bot.controllers import template, field, user

from aiogram_dialog import DialogManager


async def get_templates(**kwargs) -> dict:
    templates = await template.get_all()
    return {
        "templates": templates
    }


async def get_template_fields(dialog_manager: DialogManager, **kwargs) -> dict:
    template_id = dialog_manager.start_data.get("template_id")
    _template = await template.get(template_id)
    fields = list(map(int, str(_template.template_fields).split()))

    _fields = []
    filled_cnt = 0
    for i, field_id in enumerate(fields):
        _field = await field.get(field_id)
        _input = dialog_manager.dialog_data.get("input", {}).get(f"{field_id} {i}", "N/A")
        filled_cnt += _input != "N/A"
        _fields.append({
            "field_name": _field.field_name,
            "field_id": _field.field_id,
            "input": _input,
            "order": i,
            "status": ("✅" if _input != "N/A" else "⏳")
        })

    return {
        "template_id": template_id,
        "template_name": _template.template_name,
        "fields": _fields,
        "finished": filled_cnt == len(fields)
    }


async def input_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    field_id = int(dialog_manager.dialog_data["input_id"].split()[0])
    dialog_manager.dialog_data.update(field_id=field_id)
    return {
        "input_id": dialog_manager.dialog_data["input_id"],
        "field": await field.get(field_id)
    }
