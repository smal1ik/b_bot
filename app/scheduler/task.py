import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from arq import cron
from arq.connections import RedisSettings, ArqRedis
from decouple import config as env_config

from app.database.requests import get_upcoming_birthdays, get_all_user, get_now_month_birthdays
import app.utils.copy as cp
import app.keyboards.keyboard as kb


async def startup(ctx):
    ctx['bot'] = Bot(token=env_config('BOT_TOKEN'))


async def shutdown(ctx):
    await ctx['bot'].session.close()


async def every_day_check_birthday(ctx):
    days = [14, 7, 2, 0]
    tg_ids = await get_all_user()
    for day in days:
        persons = await get_upcoming_birthdays(day)
        for person in persons:
            for tg_id in tg_ids:
                try:
                    if day == 0 and tg_id == person.tg_id:
                        await ctx['bot'].send_message(tg_id, text=cp.birthday_person_msg)
                    else:
                        await ctx['bot'].send_message(tg_id, text=cp.get_congratulation_n_days(person, day), parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                    await asyncio.sleep(0.05)
                except:
                    continue
            await asyncio.sleep(30)


async def every_month_check_birthday(ctx):
    tg_ids = await get_all_user()
    persons = await get_now_month_birthdays()
    btn = kb.generate_bnt_birthday(persons)
    for tg_id in tg_ids:
        try:
            await ctx['bot'].send_message(tg_id, text=cp.every_month_msg, parse_mode=ParseMode.HTML,
                                          disable_web_page_preview=True, reply_markup=btn)
            await asyncio.sleep(0.05)
        except:
            continue


class workersettings:
    max_tries = 3
    redis_settings = RedisSettings(host=env_config('HOST'), port=6379, password=env_config('REDIS_PASSWORD'), database=0, username='default')
    on_startup = startup
    on_shutdown = shutdown
    allow_abort_jobs = True
    cron_jobs = [
        cron(every_day_check_birthday, minute=30, hour=8),
        cron(every_month_check_birthday, minute=0, hour=8, day=1)
    ]