""" Функциональная часть веб-приложения """
from uuid import UUID
from datetime import datetime
from app import app


def get_table(table_name, search_field=None,
              search_value=None, sort_by=None,
              sort_descending=False):
    """ Получение данных табицы """
    # SELECT @ SQLStatement = 'SELECT AgentCode, SecondName + '' '' + Name + '' '' + Patronymic
    # AS FIO, PhoneNumber, Email, Sex FROM ' +
    cursor = app.config['cursor']
    if table_name == 'applicants':
        sql_query = "SELECT * FROM ApplicantsEducationPosition"
        if sort_by is not None:
            sort = 'DESC' if sort_descending else 'ASC'
            sql_query += f" ORDER BY {sort_by} {sort}"
        types = ['uniqueidentifier', 'nvarchar', 'datetime', 'datetime',
                 'nchar', 'nvarchar', 'char', 'nvarchar', 'varchar',
                 'nvarchar', 'nvarchar']
        fields = ['ID', 'ФИО', 'Дата обращения', 'Дата рождения',
                  'Пол', 'Адрес', 'Номер телефона', 'Опыт работы', 'Email',
                  'Степень образования', 'Должность']
        column_names = ['ID', 'FIO', 'ApplicationDate', 'Birthday', 'Sex', 'RegistrationAddress',
                        'PhoneNumber', 'JobExperience', 'Email', 'EducationDegree', 'PositionName']
    else:
        cursor.execute(f"SELECT DATA_TYPE, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                       f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
        meta_info = cursor.fetchall()
        types = [info[0] for info in meta_info]
        column_names = [info[1] for info in meta_info]
        fields = app.config['TABLES'][table_name]['fields']

        sql_query = f"EXEC SortedInfo @TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'"
        if sort_by is not None:
            sort = 'DESC' if sort_descending else 'ASC'
            sql_query += f", @SORTBY = '{sort_by}', @ASCENDING = '{sort}'"
        if search_field and search_value:
            sql_query += f", @SEARCH_FIELD = '{search_field}', @SEARCH_VALUE = '{search_value}'"
    cursor.execute(sql_query)
    return cursor.fetchall(), fields, types, column_names


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
