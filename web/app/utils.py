""" Веб сервис взаимодействия с БД "Интернет провайдера" """
from app import cursor


def execute_query(query: str):
    """ Исполнение любого запроса(query) к БД """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
