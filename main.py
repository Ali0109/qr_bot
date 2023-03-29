from aiogram import executor
from aiogram.utils.executor import start_webhook

from app.handlers import register_handlers
from app.app import dp, bot
from app import logging
import settings

register_handlers(dp)


if settings.DEVELOPER_MODE:
    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)
else:
    # webhook settings
    WEBHOOK_HOST = 'https://admin.invitations.uz'
    WEBHOOK_PATH = '/'
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

    # webserver settings
    WEBAPP_HOST = '0.0.0.0'  # or ip
    WEBAPP_PORT = 8011


    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_HOST)
        # insert code here to run it after start


    async def on_shutdown(dp):
        logging.warning('Shutting down..')

        # insert code here to run it before shutdown

        # Remove webhook (not acceptable in some cases)
        await bot.delete_webhook()

        # Close DB connection (if used)
        await dp.storage.close()
        await dp.storage.wait_closed()

        logging.warning('Bye!')

    if __name__ == '__main__':
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
