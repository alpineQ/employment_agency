""" Функциональная часть веб-приложения """
import logging
from uuid import UUID
from datetime import datetime
from app import cursor


def update_note(table_name, data, key_field):
    """ Обновление записи в таблице """
    logging.info('1')
    if data.get(key_field, '') == '':
        return False
    logging.info('2')

    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_name}'")
    types = cursor.fetchall()

    set_query = ''
    query_values = []
    for field, field_type in zip(data, types):
        set_query += f"{field} = (?), "
        if data[field] == 'None' or data[field] == '':
            query_values.append(None)
        elif field_type == 'uniqueidentifier':
            query_values.append(UUID(data[field]))
        elif field_type == 'datetime':
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
    """ Рекурсивное удаление записи """
    if tables[table_name].get('dependencies', []):
        for dependency in tables[table_name]['dependencies']:
            cursor.execute(f"SELECT {tables[dependency]['key']} "
                           f"FROM {tables[dependency]['db']} "
                           f"WHERE {key_field} = (?)", UUID(key))
            dependency_keys = cursor.fetchall()
            for dependency_key in dependency_keys:
                delete_note(dependency, tables[dependency]['key'], dependency_key[0], tables)
    cursor.execute(f'DELETE FROM {table_name} WHERE {key_field} = (?);', UUID(key))


def delete_table(table_name, tables):
    """ Рекурсивное удаление таблицы """
    if tables[table_name].get('dependencies', []):
        for dependency in tables[table_name]['dependencies']:
            delete_table(dependency, tables)
    cursor.execute(f"TRUNCATE TABLE {tables[table_name]['db']}")


def add_note(table_name, data):
    """ Добавление записи в таблицу """
    cursor.execute(f"SELECT DATA_TYPE, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_name}'")
    meta_info = cursor.fetchall()

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

    logging.info(table_name, set_query, values_query)
    sql_query = f"INSERT INTO {table_name} " \
                f"({set_query}) " \
                f"VALUES ({values_query})"
    cursor.execute(sql_query, *query_values)
    return True
