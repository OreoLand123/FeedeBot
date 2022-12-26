from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdmin(StatesGroup):
    reason = State()
    reason_2 = State()
    register_number = State()
    register_number_2 = State()