from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot.app import bot, dp
from bot.handlers.base import BaseHelper


@dp.message_handler(
    lambda message: message.text == "/start",
)
async def start_handler(message: types.Message):

    helper = StartHelper(message=message)

    hello_text = await helper.get_hello_text()
    keyboard = await helper.get_contact_keyboard()

    await bot.send_message(
        chat_id=message.from_user.id,
        text=hello_text,
        reply_markup=keyboard,
    )
    return True


class StartHelper(BaseHelper):

    async def get_share_contact_text(self):
        return "Поделиться контактом"

    async def get_hello_text(self):
        share_contact_text = await self.get_share_contact_text()

        text = f"Здравствуйте, нажмите кнопку {share_contact_text} или впишите ваш номер телефона\n" \
               "Пример: 998 97 111 11 11"

        return text

    async def get_contact_keyboard(self):
        share_contact_text = await self.get_share_contact_text()

        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(KeyboardButton(text=share_contact_text, request_contact=True))

        return markup
