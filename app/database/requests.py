from app.database.models import User, async_session, BirthdayPerson
from sqlalchemy import select, BigInteger, update, delete, func, or_

from datetime import datetime, date, timedelta

async def add_user(tg_id: BigInteger, first_name: str, username: str):
    """
    Функция добавляет пользователя в БД
    """
    async with async_session() as session:
        if not first_name:
            first_name = 'None'
        if not username:
            username = 'None'
        session.add(User(tg_id=tg_id, first_name=first_name, username=username))
        await session.commit()

async def get_user(tg_id: BigInteger):
    """
    Получаем пользователя по tg_id
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result


async def get_all_user():
    """
    Получаем всех пользователей
    """
    async with async_session() as session:
        result = await session.scalars(select(User.tg_id))
        return result.fetchall()

async def get_person(tg_id: BigInteger):
    """
    Получаем именинника по tg_id
    """
    async with async_session() as session:
        tg_id = int(tg_id)
        result = await session.scalar(select(BirthdayPerson).where(BirthdayPerson.tg_id == tg_id))
        return result

async def get_all_birthday_person() -> list:
    async with async_session() as session:
        result = await session.scalars(select(BirthdayPerson))
        result = result.fetchall()
        result = [{
            'Имя': person.full_name,
            'ТГ': person.tg_id,
            'ДР': person.birthday_day,
            'Ссылка на сбор': person.link,
        } for person in result]
        return result

async def apply_change_birthday_person(changes: dict):
    new_records = changes['new_records']
    update_records = changes['update_records']
    delete_records = changes['delete_records']

    if new_records:
        new_records = [BirthdayPerson(tg_id=person['ТГ'], full_name=person['Имя'], birthday_day=person['ДР'],
                                      link=person['Ссылка на сбор']) for person in new_records]
        async with async_session() as session:
            session.add_all(new_records)
            await session.commit()

    if update_records:
        async with async_session() as session:
            for person in update_records:
                await session.execute(update(BirthdayPerson).where(BirthdayPerson.tg_id == person['ТГ']).values(
                    full_name=person['Имя'], birthday_day=person['ДР'], link=person['Ссылка на сбор'])
                )
            await session.commit()

    if delete_records:
        delete_records = [person['ТГ'] for person in delete_records]
        async with async_session() as session:
            await session.execute(delete(BirthdayPerson).where(BirthdayPerson.tg_id.in_(delete_records)))
            await session.commit()

async def get_upcoming_birthdays(days: int):
    # Список людей у которых др через n дней от настоящей даты
    async with async_session() as session:
        result = await session.scalars(select(BirthdayPerson).where(
            func.extract('month', BirthdayPerson.birthday_day) == func.extract('month', func.now() + timedelta(days=days)),
            func.extract('day', BirthdayPerson.birthday_day) == func.extract('day', func.now() + timedelta(days=days))
        ))
        return result.fetchall()

async def get_now_month_birthdays():
    today = datetime.today()

    next_month = today.month + 1 if today.month < 12 else 1
    next_month_year = today.year if today.month < 12 else today.year + 1
    start_of_next_month = datetime(next_month_year, next_month, 1)
    half_of_next_month = start_of_next_month + timedelta(days=14)

    async with async_session() as session:
        result = await session.scalars(select(BirthdayPerson).filter(
            (
                    (func.extract('month', BirthdayPerson.birthday_day) == today.month) &
                    (func.extract('day', BirthdayPerson.birthday_day) >= today.day)
            # В этом месяце, после сегодняшнего дня
            ) |
            (
                    (func.extract('month', BirthdayPerson.birthday_day) == next_month) &
                    (func.extract('day', BirthdayPerson.birthday_day) <= half_of_next_month.day)
            # В следующем месяце, до середины месяца
            )
        ).order_by(
                # Сортируем сначала по месяцу, потом по дню
                func.extract('month', BirthdayPerson.birthday_day),
                func.extract('day', BirthdayPerson.birthday_day)
            ))
        return result.fetchall()


