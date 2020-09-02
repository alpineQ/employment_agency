""" Функциональная часть веб-приложения """
from uuid import UUID
from datetime import datetime
from app import app


def get_table(table_name, search_field=None,
              search_value=None, sort_by=None,
              sort_descending=False):
    """ Получение данных табицы """
    cursor = app.config['cursor']
    db_name = app.config['TABLES'][table_name]['db']
    if table_name == 'applicants':
        fields = ['ID', 'ФИО', 'Дата обращения', 'Дата рождения',
                  'Пол', 'Адрес', 'Номер телефона', 'Опыт работы', 'Email',
                  'Степень образования', 'Должность']
        db_name = 'ApplicantsEducationPosition'
    else:
        fields = app.config['TABLES'][table_name]['fields']
    sql_query = f"EXEC SortedInfo @TABLE_NAME = {db_name}"

    if sort_by is not None:
        sort = 'DESC' if sort_descending else 'ASC'
        sql_query += f", @SORTBY = '{sort_by}', @ASCENDING = '{sort}'"
    if search_field and search_value:
        meta_info = cursor.execute(
            f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
            f"WHERE TABLE_NAME = '{db_name}'"
        ).fetchall()
        column_names = [info[0] for info in meta_info]
        types = [info[1] for info in meta_info]
        if types[column_names.index(search_field)] in ['nvarchar', 'nchar']:
            sql_query += f", @SEARCH_FIELD = '{search_field}', " \
                         f"@SEARCH_VALUE = N'{search_value}', " \
                         f"@SEARCH_N_TYPE = 1"
        else:
            sql_query += f", @SEARCH_FIELD = '{search_field}', " \
                         f"@SEARCH_VALUE = '{search_value}', " \
                         f"@SEARCH_N_TYPE = 0"

    cursor.execute(sql_query)
    column_names = [info[0] for info in cursor.description]
    types = [info[1] for info in cursor.description]
    return cursor.fetchall(), fields, types, column_names


def add_note(table_name, data):
    """ Добавление записи в таблицу """
    cursor = app.config['cursor']
    meta_info = cursor.execute(
        f"SELECT DATA_TYPE, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
        f"WHERE TABLE_NAME = '{table_name}'"
    ).fetchall()

    set_query = ''
    values_query = ''
    query_values = []
    for field, info in zip(data, meta_info[1:]):
        set_query += f"{field}, "
        values_query += '?,'
        query_values.append(make_sql_object(data[field], info[0]))
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

    types = cursor.execute(
        f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
        f"WHERE TABLE_NAME = '{table_name}'"
    ).fetchall()

    set_query = ''
    query_values = []
    for field, field_type in zip(data, types):
        set_query += f"{field} = (?), "
        query_values.append(make_sql_object(data[field], field_type))

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
            dependency_keys = cursor.execute(
                f"SELECT {tables[dependency]['key']} "
                f"FROM {tables[dependency]['db']} "
                f"WHERE {key_field} = (?)", UUID(key)
            ).fetchall()
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


def make_sql_object(field_value, field_type):
    """ Создание объекта для передачи в cursor.execute """
    if field_value in ['None', '']:
        return None
    if field_type == 'uniqueidentifier':
        return UUID(field_value)
    if field_type == 'datetime':
        return datetime.strptime(field_value, '%Y-%m-%d').date()
    return field_value
