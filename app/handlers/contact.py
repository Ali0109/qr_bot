import re

import qrcode
import requests
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.app import dp, bot
from app.handlers.base import BaseHelper
from app.handlers.start import StartHelper
from settings import DOMAIN, ENTRYPOINT


@dp.message_handler(content_types=["text", "contact"])
async def contact_handler(message: types.Message):
    helper = ContactHelper(message=message)

    if message.contact:
        phone = await helper.get_correct_phone(message.contact.phone_number)
    else:
        phone = await helper.get_correct_phone(message.text)

    is_valid = await helper.check_phone(phone)
    if is_valid:

        response_ticket_numbers = await helper.get_response_ticket_numbers(phone)
        keyboard = await helper.get_start_keyboard()

        tickets = response_ticket_numbers.json()

        if tickets:
            for ticket in tickets:
                ticket_number = ticket["number"]
                qr = await helper.generate_qr(ticket_number)

                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=qr,
                    caption=ticket_number,
                )

            success_text = await helper.get_success_text()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=success_text,
                reply_markup=keyboard,
            )
        else:

            user_not_found_text = await helper.get_user_not_found_text()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=user_not_found_text,
                reply_markup=keyboard,
            )
    else:

        error_phone_text = await helper.get_error_phone_text()
        keyboard = await StartHelper(message).get_contact_keyboard()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=error_phone_text,
            reply_markup=keyboard
        )

    return True


class ContactHelper(BaseHelper):

    async def get_correct_phone(self, phone: str) -> str:
        correct_phone = "".join(re.split("\D+", phone))
        return correct_phone

    async def check_phone(self, phone: str) -> bool:
        if len(phone) == 12 or phone[0:3] == "998":
            return True
        else:
            return False

    async def get_error_phone_text(self):
        text = "Введите правильный номер.\nПример: 998 97 111 11 11"
        return text

    async def get_response_ticket_numbers(self, phone):
        path = "ticket/numbers"
        data = {"phone": phone}
        response = requests.get(url=f"{DOMAIN}/{ENTRYPOINT}/{path}", data=data)
        return response

    async def get_start_keyboard(self):
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(KeyboardButton(text="/start"))
        return markup

    async def get_user_not_found_text(self):
        return "Этот номер не зарегистрирован в системе"

    async def get_success_text(self):
        text = "Поздравляем, это все ваши доступные и активные QR-Code пригласительные, " \
               "сохраните их и предъявите для входа на мероприятие"
        return text

    async def generate_qr(self, ticket_number):
        url = f"{DOMAIN}/api/ticket/deactivate/{ticket_number}/"
        qr = qrcode.make(url)
        path = f"media/{ticket_number}.png"
        qr.save(path)
        img = open(path, "rb")
        return img
