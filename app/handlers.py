import re

from aiogram import types, Dispatcher

from . import keyboards, api, async_helpers
from .app import bot


# --- Start ---
async def start(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Здравствуйте, нажмите кнопку "Поделиться контактом" или впишите ваш номер телефона\n'
        "Пример: 998 97 111 11 11",
        reply_markup=keyboards.contact_func(),
    )


# --- Contact ---
async def contact(message: types.Message):
    if message.contact:
        phone = ''.join(re.split('\D+', message.contact.phone_number))
    else:
        phone = ''.join(re.split('\D+', message.text))
        await async_helpers.check_uz_phone_number(message, phone)

    contact_data = api.contact_api(phone)
    await async_helpers.response_from_data(message, contact_data)


# --- Register handlers ---
def register_handlers(dp: Dispatcher):
    # Start
    dp.register_message_handler(start, commands=['start'], state=None)
    # Contact
    dp.register_message_handler(contact, content_types=['text', 'contact'])

    # Finish
    # dp.register_message_handler(start, commands=['finish'], state=menu)
