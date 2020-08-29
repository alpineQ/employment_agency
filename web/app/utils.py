""" Функциональная часть веб-приложения """
import logging
from uuid import UUID
from datetime import datetime
from app import cursor


def update_note(table_name, data, key_field):
    """ Обновление записи в таблице """
    if data[key_field] == '':
        return False

    cursor.execute(f"SELECT DATA_TYPE, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_name}'")
    meta_info = cursor.fetchall()

    set_query = ''
    query_values = []
    for field, info in zip(data, meta_info):
        set_query += f"{field} = (?), "
        if data[field] == 'None':
            query_values.append(None)
        elif info[0] == 'uniqueidentifier':
            query_values.append(UUID(data[field]))
        elif info[0] == 'datetime':
            if '.' in data[field]:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S.%f'))
            elif ':' in data[field]:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S'))
            else:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d'))
        else:
            query_values.append(data[field])

    set_query = set_query[:-2]
    sql_query = f"UPDATE {table_name} " \
                f"SET {set_query} " \
                f"WHERE {key_field} = (?)"
    cursor.execute(sql_query, *query_values, UUID(data[key_field]))
    return True


def delete_note(table_name, key_field, key, tables):
    """DELETE FROM child
FROM cTable AS child
INNER JOIN table AS parent ON child.ParentId = parent.ParentId
WHERE <condition>;

DELETE FROM parent
FROM table AS parent
WHERE <condition>;"""
    # if tables[table_name].get('dependencies', '') != '':
    #     for dependency in tables[table_name]['dependencies']:
    #         delete_dependency(dependency, )
    cursor.execute(f'DELETE FROM {table_name} WHERE {key_field} = (?);', UUID(key))


def delete_dependency(table_name, key_field, key, tables):
    """ Удаление внешнего ключа записи """
    pass


def add_note(table_name, data):
    """ Добавление записи в таблицу """
    logging.info('2')
    logging.info('inhere0')

    cursor.execute(f"SELECT DATA_TYPE, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_name}'")
    meta_info = cursor.fetchall()
    logging.info('inhere')

    set_query = ''
    values_query = ''
    query_values = []
    for field, info in zip(data, meta_info[1:]):
        set_query += f"{field}, "
        values_query += '?,'
        if data[field] == 'None' or data[field] == '':
            query_values.append(None)
        elif info[0] == 'uniqueidentifier':
            query_values.append(UUID(data[field]))
        elif info[0] == 'datetime':
            if '.' in data[field]:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S.%f'))
            elif ':' in data[field]:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S'))
            else:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d'))
        else:
            query_values.append(data[field])
    set_query = set_query[:-2]
    values_query = values_query[:-1]

    logging.info('here')
    sql_query = f"INSERT INTO {table_name} " \
                f"({set_query}) " \
                f"VALUES ({values_query})"
    cursor.execute(sql_query, *query_values)
    logging.info('here1')
    return True
