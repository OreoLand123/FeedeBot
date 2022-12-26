from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN_BOT = "5393916177:AAGCXzGAxzpeeZm5r4tholcpyBxUskY4P2Y"
storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)