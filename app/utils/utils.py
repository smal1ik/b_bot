from app.utils.google_sheet import get_from_table
from datetime import datetime


def get_actual_month_birthday(table: list):
    today_month = datetime.today().month
    for person in table:
        # print(person.get('ДР'))
        date = datetime.strptime(person.get('ДР'), "%d.%m.%Y")
        if date.month == today_month:
            print(person)


def find_differences(db_data: list[dict], api_data: list[dict]) -> dict:
    new_records = []
    updated_records = []
    deleted_records = []

    db_dict = {person['ТГ']: person for person in db_data}
    api_dict = {person['ТГ']: person for person in api_data}

    # Проверяем, что в таблице есть новые или измененные записи
    for tg_id, person in api_dict.items():
        if tg_id not in db_dict:
            new_records.append(person)
        else:
            db_person = db_dict[tg_id]
            if (db_person['Имя'] != person['Имя'] or
                    db_person['ДР'] != person['ДР'] or
                    db_person['Ссылка на сбор'] != person['Ссылка на сбор']):
                updated_records.append(person)

    # Проверяем, какие записи удалены из таблицы
    for tg_id, person in db_dict.items():
        if not api_dict.get(tg_id):
            deleted_records.append(person)

    return {
        'new_records': new_records,
        'update_records': updated_records,
        'delete_records': deleted_records
    }


def get_month_name_ru(month_num):
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    return months[month_num - 1]