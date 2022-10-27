from aiogram.dispatcher.filters.state import StatesGroup, State


class AdvStates(StatesGroup):
    title = State()
    desc = State()
    image = State()
    price = State()
    phone = State()
    confirm = State()