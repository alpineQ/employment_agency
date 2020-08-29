""" Функциональная часть веб-приложения """
from uuid import UUID
from datetime import datetime
from app import cursor


def update_note(table_name, data):
    """ Обновление записи в таблице """
    cursor.execute(f"SELECT DATA_TYPE, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_name}'")
    meta_info = cursor.fetchall()

    key_field = ''
    set_query = ''
    query_values = []
    for field, _ in zip(data, meta_info):
        if not field.endswith('*'):
            set_query += f"{field} = (?), "
        else:
            key_field = field
            set_query += f"{key_field[:-1]} = (?), "

        if meta_info[0] == 'uniqueidentifier':
            query_values.append(UUID(data[field]))
        elif meta_info[0] == 'datetime':
            if '.' in data[field]:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S.%f'))
            elif ':' in data[field]:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S'))
            else:
                query_values.append(datetime.strptime(data[field], '%Y-%m-%d'))
        elif data[field] == 'None':
            query_values.append(None)
        else:
            query_values.append(data[field])
    if key_field == '':
        return False

    set_query = set_query[:-2]
    sql_query = f"UPDATE {table_name} " \
                f"SET {set_query} " \
                f"WHERE {key_field[:-1]} = (?)"
    cursor.execute(sql_query, *query_values, UUID(data[key_field]))
    return True
