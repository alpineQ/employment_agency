""" Веб сервис взаимодействия с БД "Интернет провайдера" """
from flask import render_template, redirect, request, url_for
# pylint: disable=c-extension-no-member
import pyodbc
from app.fill_table import fill_db
from app.utils import update_note, delete_note, add_note, delete_table, get_table
from app import app


@app.route('/')
def index():
    """ Список всех таблиц БД """
    cursor = app.config['cursor']
    for table in app.config['TABLES']:
        cursor.execute(f"SELECT COUNT(*) FROM {app.config['TABLES'][table]['db']}")
        app.config['TABLES'][table]['n_records'] = cursor.fetchone()[0]
    return render_template('index.html', tables=app.config['TABLES'],
                           username=app.config['USERNAME'])


@app.route('/agents/')
@app.route('/applicants/')
@app.route('/deals/')
@app.route('/education/')
@app.route('/employers/')
@app.route('/positions/')
@app.route('/vacancies/')
def table_view():
    """ Данные таблиц """
    table_name = request.path[1:-1]
    table_data, fields, types = get_table(table_name, app.config['TABLES'][table_name])
    return render_template('table.html', table_data=table_data, name=table_name, fields=fields,
                           username=app.config['USERNAME'], types=types, zip=zip,
                           tables=app.config['TABLES'])


@app.route('/agents/<note_id>/')
@app.route('/applicants/<note_id>/')
@app.route('/deals/<note_id>/')
@app.route('/education/<note_id>/')
@app.route('/employers/<note_id>/')
@app.route('/positions/<note_id>/')
@app.route('/vacancies/<note_id>/')
def note_view(note_id):
    """ Информация о конкретной записи """
    cursor = app.config['cursor']
    table_name = request.path[1:request.path.find('/', 1)]
    cursor.execute(f"SELECT * FROM {app.config['TABLES'][table_name]['db']} "
                   f"WHERE {app.config['TABLES'][table_name]['key']} = (?)", note_id)
    table_data = cursor.fetchone()
    cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH "
                   f"FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    meta_info = cursor.fetchall()
    return render_template('note.html', table_data=table_data, name=table_name, meta_info=meta_info,
                           zip=zip, tables=app.config['TABLES'], username=app.config['USERNAME'])


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')


@app.route('/clear_db/', methods=['POST'])
def delete_all_data():
    """ Заполнение БД данными """
    for table in app.config['TABLES']:
        delete_table(table)
    return redirect('/')


@app.route('/agents/update/', methods=['POST'])
@app.route('/applicants/update/', methods=['POST'])
@app.route('/deals/update/', methods=['POST'])
@app.route('/education/update/', methods=['POST'])
@app.route('/employers/update/', methods=['POST'])
@app.route('/positions/update/', methods=['POST'])
@app.route('/vacancies/update/', methods=['POST'])
def update_note_route():
    """ Обновление записи в таблице """
    table = request.path[1:request.path.find('/', 1)]
    table_name = app.config['TABLES'][table]['db']
    if not update_note(table_name, request.form, app.config['TABLES'][table]['key']):
        return 'Bad request', 400
    return redirect(f'/{table}/')


@app.route('/agents/delete/<note_id>/', methods=['POST'])
@app.route('/applicants/delete/<note_id>/', methods=['POST'])
@app.route('/deals/delete/<note_id>/', methods=['POST'])
@app.route('/education/delete/<note_id>/', methods=['POST'])
@app.route('/employers/delete/<note_id>/', methods=['POST'])
@app.route('/positions/delete/<note_id>/', methods=['POST'])
@app.route('/vacancies/delete/<note_id>/', methods=['POST'])
def delete_note_route(note_id):
    """ Удаление таблицы """
    table = request.path[1:request.path.find('/', 1)]
    delete_note(table, app.config['TABLES'][table]['key'], note_id)
    return redirect(f'/{table}/')


@app.route('/agents/delete/', methods=['POST'])
@app.route('/applicants/delete/', methods=['POST'])
@app.route('/deals/delete/', methods=['POST'])
@app.route('/education/delete/', methods=['POST'])
@app.route('/employers/delete/', methods=['POST'])
@app.route('/positions/delete/', methods=['POST'])
@app.route('/vacancies/delete/', methods=['POST'])
def delete_table_route():
    """ Удаление таблицы """
    table = request.path[1:request.path.find('/', 1)]
    delete_table(table)
    return redirect('/')


@app.route('/agents/add/')
@app.route('/applicants/add/')
@app.route('/deals/add/')
@app.route('/education/add/')
@app.route('/employers/add/')
@app.route('/positions/add/')
@app.route('/vacancies/add/')
def add_note_view():
    """ Страница добавления записи в таблице """
    cursor = app.config['cursor']
    table_name = request.path[1:request.path.find('/', 1)]
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    column_names = cursor.fetchall()
    cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH "
                   f"FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    meta_info = cursor.fetchall()
    return render_template('add_note.html', meta_info=meta_info, name=table_name, zip=zip,
                           username=app.config['USERNAME'], tables=app.config['TABLES'],
                           column_names=column_names)


@app.route('/agents/add/', methods=['POST'])
@app.route('/applicants/add/', methods=['POST'])
@app.route('/deals/add/', methods=['POST'])
@app.route('/education/add/', methods=['POST'])
@app.route('/employers/add/', methods=['POST'])
@app.route('/positions/add/', methods=['POST'])
@app.route('/vacancies/add/', methods=['POST'])
def add_note_route():
    """ Страница добавления записи в таблице """
    table_name = request.path[1:request.path.find('/', 1)]
    if not add_note(table_name, request.form):
        return 'Bad request', 400
    return redirect(f'/{table_name}/')


@app.route('/login/')
def login_view():
    """ Смена пользователя (фронтенд) """
    invalid = 'invisible' if not request.args.get('invalid') else ''
    return render_template('login.html', tables=app.config['TABLES'],
                           username=app.config['USERNAME'], invalid=invalid)


@app.route('/login/', methods=['POST'])
def login_route():
    """ Смена пользователя (бэкенд) """
    username = request.form['username']
    password = request.form['password']
    try:
        new_connection = pyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};'
            f"Server={app.config['SERVER']};"
            f"Database={app.config['DATABASE']};"
            f"uid={username};"
            f"PWD={password}"
        )
    except (pyodbc.InterfaceError, pyodbc.ProgrammingError):
        return redirect(url_for('login_view', invalid='True'))
    app.config['USERNAME'] = username
    app.config['PASSWORD'] = password
    app.config['connection'].close()
    app.config['connection'] = new_connection
    app.config['cursor'] = new_connection.cursor()
    return redirect('/')
