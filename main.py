from aiogram import executor

from app.handlers import register_handlers
from app.app import dp

register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
