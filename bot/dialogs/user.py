from magic_filter import F

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import *
from aiogram_dialog.widgets.text import *
from aiogram_dialog.widgets.input import *

from bot.models import Template, Field, User

from bot.dialogs import getters, handlers
from bot.dialogs.states import UserMenuSG, AddDocumentSG

main_user_dialog = Dialog(
    Window(
        Const("Главное меню"),
        SwitchTo(Const("Добавить новую запись"), id="add_doc", state=UserMenuSG.add_doc),
        SwitchTo(Const("Мои записи"), id="my_docs", state=UserMenuSG.my_docs),
        state=UserMenuSG.main
    ),
    Window(
        Const("Меню добавления записи"),
        SwitchTo(Const("Добавить шаблон"), id="add", state=UserMenuSG.add_template),
        ScrollingGroup(
            Select(
                text=Format("{item.template_name}"),
                id="templates_select",
                items="templates",
                on_click=handlers.user.select_template,
                item_id_getter=lambda template: template.template_id,
            ),
            width=2,
            height=10,
            hide_on_single_page=True,
            id="templates_scroller"
        ),
        SwitchTo(Const("Назад"), id="back", state=UserMenuSG.main),
        state=UserMenuSG.add_doc,
        getter=getters.get_templates,
    ),
    Window(
        Const("Добавление🥵"),
        SwitchTo(Const("Назад"), id="back", state=UserMenuSG.add_doc),
        state=UserMenuSG.add_template
    ),
    Window(
        Const("Ваши сохраненные записи"),
        SwitchTo(Const("Назад"), id="back", state=UserMenuSG.main),
        state=UserMenuSG.my_docs
    )
)

document_adding_dialog = Dialog(
    Window(
        Jinja(
            "<b>Выбран шаблон \"{{ template_name }}\" [{{ template_id }}]</b>\n"
            "{% for index in range(fields | length) %}\n"
            "<a>{{fields[index].field_name}} - <b>{{fields[index].input}}</b></a>\n"
            "{% endfor %}\n"
        ),
        ScrollingGroup(
            Select(
                Format("{item[field_name]} {item[status]}"),
                id="field_writer",
                items="fields",
                on_click=handlers.user.select_input_field,
                item_id_getter=lambda field: f"{field['field_id']} {field['order']}"
            ),
            id="fields_scrolling_group",
            height=6,
            width=2,
        ),
        Cancel(Const("Добавить", when=F["finished"])),
        Cancel(Const("Назад")),
        parse_mode="HTML",
        getter=getters.get_template_fields,
        state=AddDocumentSG.main,
    ),
    Window(
        Format("Ввод для {field.field_name}"),
        TextInput(id="input", on_success=handlers.user.handle_input_field),
        SwitchTo(Const("Назад"), id="back", state=AddDocumentSG.main),
        getter=getters.input_data_getter,
        state=AddDocumentSG.input
    )
)
