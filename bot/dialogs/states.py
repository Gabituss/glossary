from aiogram.filters.state import StatesGroup, State


class UserMenuSG(StatesGroup):
    main = State()
    add_doc = State()
    add_template = State()
    my_docs = State()


class AddDocumentSG(StatesGroup):
    main = State()
    input = State()