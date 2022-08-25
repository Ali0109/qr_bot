import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from .keyboards import *
from .text import *
from .app import bot
from .api import *


# --- Start ---
async def start(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Здравствуйте, нажмите кнопку "Поделиться контактом" или впишите ваш номер телефона\n'
        "Пример: 998 97 111 11 11",
        reply_markup=contact_func(),
    )


# --- Contact ---
async def contact(message: types.Message):
    if message.contact:
        phone = ''.join(re.split('\D+', message.contact.phone_number))
    else:
        phone = ''.join(re.split('\D+', message.text))
        if len(phone) != 12 or phone[0:3] != "998":
            await bot.send_message(
                message.from_user.id,
                "Неверный номер,\n"
                "Неверно набран номер \nПример: 998 97 111 11 11",
                reply_markup=contact_func()
            )
            return False

    contact_data = contact_api(phone)
    if contact_data['status'] == 200:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=open(f"{contact_data['path']}{contact_data['image']}", "rb"),
            reply_markup=start_func(),
        )
        await bot.send_message(
            message.from_user.id,
            "Поздравляем, это ваш QR-Code, сохраните его и предъявите для входа на мероприятие",
            reply_markup=start_func(),
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "Этот номер не зарегистрирован в системе",
            reply_markup=start_func(),
        )


# --- Register handlers ---
def register_handlers(dp: Dispatcher):
    # Start
    dp.register_message_handler(start, commands=['start'], state=None)
    # Contact
    dp.register_message_handler(contact, content_types=['text', 'contact'])

    # Finish
    # dp.register_message_handler(start, commands=['finish'], state=menu)
