from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandObject, Command

from aiogram_dialog import DialogManager

from bot.controllers import field, template, user
from loguru import logger


async def get_fields(message: Message, dialog_manager: DialogManager):
    fields = await field.get_all()
    for _field in fields:
        await message.answer(f"[{_field.field_id}] {_field.field_name} {_field.field_re}")


async def get_templates(message: Message, dialog_manager: DialogManager):
    templates = await template.get_all()
    for _template in templates:
        await message.answer(str(_template))


async def add_field(message: Message, command: CommandObject, dialog_manager: DialogManager):
    if command.args is None:
        logger.error("add_field command: values not provided")
        await message.answer("Не введены данные!")
        return

    try:
        field_name, expression = command.args.split(" | ", maxsplit=2)
    except ValueError:
        logger.error("add_field command: not enough values")
        await message.answer("Не все поля введены!")
        return

    await field.create_field(
        field_name=field_name,
        field_re=expression
    )
    await message.answer("Поле добавлено")


async def add_template(message: Message, command: CommandObject, dialog_manager: DialogManager):
    if command.args is None:
        logger.error("add_template command: values not provided")
        await message.answer("Не введены данные!")
        return

    try:
        template_name, fields = command.args.split(" | ")
        fields = fields.split()
        if len(fields) == 0:
            raise ValueError
    except ValueError:
        logger.error("add_template command: not enough values")
        await message.answer("Не все поля введены!")
        return

    for field_id in fields:
        field_id = int(field_id)
        if not await field.field_exists(field_id):
            logger.error(f"add_template command: field [{field_id}] does not exists")
            await message.answer(f"Поля с id={field_id} не существует!")
            return

    await template.create_template(
        template_name=template_name,
        template_fields=" ".join(fields)
    )
    await message.answer("OK")


async def delete_field(message: Message, command: CommandObject, dialog_manager: DialogManager):
    field_id = int(command.args)

    await field.delete_field(field_id)
    await message.answer("Поле удалено")


async def update_field(message: Message, command: CommandObject, dialog_manager: DialogManager):
    field_id = int(command.args.split()[0])
    new_re = command.args.split(maxsplit=1)[1]

    await field.update_field(field_id, field_re=new_re)


async def delete_template(message: Message, command: CommandObject, dialog_manager: DialogManager):
    template_id = int(command.args)

    await template.delete_template(template_id)
    await message.answer("Шаблон удален")


async def check(message: Message, command: CommandObject, dialog_manager: DialogManager):
    field_id, text = command.args.split(" ", maxsplit=1)
    field_id = int(field_id)

    _field = await field.get(field_id)
    result = _field.check_string(text)

    if result:
        await message.answer("OK")
    else:
        await message.answer("BAD")


def setup(dp: Dispatcher):
    dp.message.register(add_field, Command("add_field"))
    dp.message.register(update_field, Command("update_field"))
    dp.message.register(delete_field, Command("delete_field"))
    dp.message.register(get_fields, Command("get_fields"))
    dp.message.register(check, Command("check"))

    dp.message.register(add_template, Command("add_template"))
    dp.message.register(delete_template, Command("delete_template"))
    dp.message.register(get_templates, Command("get_templates"))
