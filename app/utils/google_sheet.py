from datetime import datetime

from gspread import Client, Spreadsheet, Worksheet, service_account
from decouple import config

def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account(filename='./app/utils/bbot-453904-68bcf372066f.json')
    # return service_account(filename='bbot-453904-68bcf372066f.json')

def get_table_by_id(client: Client, table_url) -> list:
    """Получение таблицы из Google Sheets по ID таблицы."""
    spreadsheet = client.open_by_key(table_url)
    table = spreadsheet.worksheet('Лист1')
    return table.get_all_records()

def get_from_table():
    try:
        client = client_init_json()
        table = get_table_by_id(client, config('GSHEET_TABLE_ID'))
        for person in table:
            person['ДР'] = datetime.strptime(person['ДР'], "%d.%m.%Y").date()
        return table
    except:
        return []