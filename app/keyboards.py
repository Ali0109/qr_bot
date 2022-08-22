from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# Commands
command_menu = '/menu'
command_start = '/start'

# Remove btn
remove_btn = ReplyKeyboardRemove()


def start_func():
    start_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    start_btn = KeyboardButton(text="/start")
    return start_markup.add(start_btn)


def contact_func():
    contact_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    contact_btn = KeyboardButton(text="Поделиться номером", request_contact=True)
    return contact_markup.add(contact_btn)
