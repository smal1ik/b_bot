from datetime import timedelta, datetime

from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram import types, F, Router, Bot, BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, FSInputFile
from aiogram.utils.deep_linking import create_start_link, decode_payload, encode_payload
from arq import ArqRedis

import app.utils.copy as cp
import app.keyboards.keyboard as kb
from app.database.requests import get_user, add_user, get_all_birthday_person, apply_change_birthday_person, \
    get_upcoming_birthdays, get_now_month_birthdays, get_person
from app.utils.google_sheet import get_from_table
from app.utils.utils import find_differences

router_main = Router()

@router_main.message(Command('update'))
async def answer_message(message: types.Message, state: FSMContext, bot: Bot):
    birthday_from_table = get_from_table()
    if birthday_from_table:
        birthday_from_db = await get_all_birthday_person()
        changes = find_differences(birthday_from_db, birthday_from_table)
        await apply_change_birthday_person(changes)
        await message.answer('Таблица успешно обновлена')
    else:
        await message.answer('Произошла ошибка, если ошибка продолжается, сообщите админу')

@router_main.message(Command('start'))
async def answer_message(message: types.Message, state: FSMContext, bot: Bot):
    user = await get_user(message.from_user.id)
    if not user:
        await add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(cp.start_msg)
    # await message.answer(cp.start_msg, reply_markup=kb.menu_btn)


@router_main.callback_query(F.data == 'back')
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(cp.start_msg)
    # await callback.message.answer(cp.start_msg, reply_markup=kb.menu_btn)


@router_main.callback_query(F.data == 'here')
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(cp.info_msg)
    # await callback.message.answer(cp.info_msg, reply_markup=kb.menu_btn)


@router_main.callback_query(F.data == 'offer')
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(cp.offer_msg)
    # await callback.message.answer(cp.offer_msg, reply_markup=kb.menu_btn)


@router_main.callback_query(F.data == 'who_today')
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    persons = await get_now_month_birthdays()
    btn = kb.generate_bnt_birthday(persons)
    await callback.message.answer(cp.birthday_msg, reply_markup=btn)


@router_main.callback_query(F.data.contains('info'))
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    _, tg_id = callback.data.split('_')
    person = await get_person(tg_id)
    # await callback.message.answer(cp.get_congratulation(person), reply_markup=kb.back_btn, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    await callback.message.answer(cp.get_congratulation(person), parse_mode=ParseMode.HTML, disable_web_page_preview=True)