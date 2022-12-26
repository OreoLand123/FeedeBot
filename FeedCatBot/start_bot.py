from aiogram import *
from create_bot import dp
from handlers import register_handler


register_handler(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)