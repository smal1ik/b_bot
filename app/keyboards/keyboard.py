from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import BirthdayPerson

# menu = types.ReplyKeyboardMarkup(keyboard=[
#     [types.KeyboardButton(text="Зачем я здесь?")],
#     [types.KeyboardButton(text="У кого сегодня праздник?")],
#     [types.KeyboardButton(text="У меня есть предложение")],
# ])

menu_btn = InlineKeyboardBuilder()
menu_btn.row(
    types.InlineKeyboardButton(
        text="Зачем я здесь?",
        callback_data="here")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="У кого скоро праздник?",
        callback_data="who_today")
)
menu_btn.row(
    types.InlineKeyboardButton(
        text="У меня есть предложение",
        callback_data="offer")
)
menu_btn = menu_btn.as_markup()

back_btn = InlineKeyboardBuilder()
back_btn.row(
    types.InlineKeyboardButton(
        text="В начало",
        callback_data="back")
)
back_btn = back_btn.as_markup()

def generate_bnt_birthday(persons: list):
    btn = InlineKeyboardBuilder()
    for person in persons:
        btn.row(
            types.InlineKeyboardButton(
                text=person.full_name,
                callback_data=f"info_{person.tg_id}")
        )
    btn.row(
        types.InlineKeyboardButton(
            text="В начало",
            callback_data="back")
    )
    return btn.as_markup()
