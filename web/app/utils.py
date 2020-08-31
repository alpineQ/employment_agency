""" Функциональная часть веб-приложения """
from uuid import UUID
from datetime import datetime
from app import app


def get_table(table_name, table_info, constraint_field=None,
              constraint_value=None, constraint_type=None):
    """ Получение данных табицы """
    cursor = app.config['cursor']
    if table_name == 'agents':
        sql_query = "EXEC AgentsInfo"
        types = ['uniqueidentifier', 'nvarchar', 'char', 'varchar', 'nchar']
        fields = ['ID', 'ФИО', 'Номер телефона', 'Email', 'Пол']
    elif table_name == 'applicants':
        sql_query = "SELECT * FROM ApplicantsEducationPosition"
        types = ['uniqueidentifier', 'nvarchar', 'datetime', 'datetime',
                 'nchar', 'nvarchar', 'char', 'nvarchar', 'varchar',
                 'nvarchar', 'nvarchar']
        fields = ['ID', 'ФИО', 'Дата обращения', 'Дата рождения',
                  'Пол', 'Адрес', 'Номер телефона', 'Опыт работы', 'Email',
                  'Степень образования', 'Должность']
    else:
        cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                       f"WHERE TABLE_NAME = '{table_info['db']}'")
        meta_info = cursor.fetchall()
        types = [info[0] for info in meta_info]
        sql_query = f"SELECT * FROM {table_info['db']}"
        fields = table_info['fields']
    # if constraint_field and constraint_value:
    #     sql_query += f" WHERE {constraint_field} = (?)"
    #     logging.info(sql_query)
    #     cursor.execute(sql_query, constraint_value)
    cursor.execute(sql_query)
    return cursor.fetchall(), fields, types


def add_note(table_name, data):
    """ Добавление записи в таблицу """
    cursor = app.config['cursor']
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

    sql_query = f"INSERT INTO {table_name} " \
                f"({set_query}) " \
                f"VALUES ({values_query})"
    cursor.execute(sql_query, *query_values)
    app.config['connection'].commit()
    return True


def update_note(table_name, data, key_field):
    """ Обновление записи в таблице """
    cursor = app.config['cursor']
    if data.get(key_field, '') == '':
        return False

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
    app.config['connection'].commit()
    return True


def delete_note(table_name, key_field, key):
    """ Рекурсивное удаление записи """
    cursor = app.config['cursor']
    tables = app.config['TABLES']
    if tables[table_name].get('dependencies', []):
        for dependency in tables[table_name]['dependencies']:
            cursor.execute(f"SELECT {tables[dependency]['key']} "
                           f"FROM {tables[dependency]['db']} "
                           f"WHERE {key_field} = (?)", UUID(key))
            dependency_keys = cursor.fetchall()
            for dependency_key in dependency_keys:
                delete_note(dependency, tables[dependency]['key'], dependency_key[0])
    cursor.execute(f'DELETE FROM {table_name} WHERE {key_field} = (?);', UUID(key))
    app.config['connection'].commit()


def delete_table(table_name):
    """ Рекурсивное удаление таблицы """
    cursor = app.config['cursor']
    tables = app.config['TABLES']
    if tables[table_name].get('dependencies', []):
        for dependency in tables[table_name]['dependencies']:
            delete_table(dependency)
    cursor.execute(f"TRUNCATE TABLE {tables[table_name]['db']}")
    app.config['connection'].commit()
