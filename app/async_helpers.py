from .app import bot
from . import keyboards, helpers


async def check_uz_phone_number(message, phone):
    if len(phone) != 12 or phone[0:3] != "998":
        await bot.send_message(
            message.from_user.id,
            "Неверный номер,\n"
            "Неверно набран номер \nПример: 998 97 111 11 11",
            reply_markup=keyboards.contact_func()
        )
        return False
    else:
        return True


async def response_from_data(message, contact_data):
    if contact_data.status_code == 200:
        qr = helpers.generate_qr_code(contact_data.json()["number"])
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=qr,
            reply_markup=keyboards.start_func(),
        )
        await bot.send_message(
            message.from_user.id,
            "Поздравляем, это ваш QR-Code, сохраните его и предъявите для входа на мероприятие",
            reply_markup=keyboards.start_func(),
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "Этот номер не зарегистрирован в системе",
            reply_markup=keyboards.start_func(),
        )
