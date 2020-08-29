""" Веб сервис взаимодействия с БД "Интернет провайдера" """
from flask import render_template, redirect, request
from app.fill_table import fill_db
from app.utils import update_note, delete_note, add_note, delete_table
from app import app, cursor


@app.route('/')
def index():
    """ Список всех таблиц БД """
    for table in app.config['TABLES']:
        cursor.execute(f"SELECT COUNT(*) FROM {app.config['TABLES'][table]['db']}")
        app.config['TABLES'][table]['n_records'] = cursor.fetchone()[0]
    return render_template('index.html', tables=app.config['TABLES'])


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
    cursor.execute(f"SELECT * FROM {app.config['TABLES'][table_name]['db']}")
    table_data = cursor.fetchall()
    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    types = cursor.fetchall()
    return render_template('table.html', table_data=table_data, name=table_name,
                           types=types, zip=zip, tables=app.config['TABLES'])


@app.route('/agents/<note_id>/')
@app.route('/applicants/<note_id>/')
@app.route('/deals/<note_id>/')
@app.route('/education/<note_id>/')
@app.route('/employers/<note_id>/')
@app.route('/positions/<note_id>/')
@app.route('/vacancies/<note_id>/')
def note_view(note_id):
    """ Информация о конкретной записи """
    table_name = request.path[1:request.path.find('/', 1)]
    cursor.execute(f"SELECT * FROM {app.config['TABLES'][table_name]['db']} "
                   f"WHERE {app.config['TABLES'][table_name]['key']} = (?)", note_id)
    table_data = cursor.fetchone()
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    column_names = cursor.fetchall()
    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    types = cursor.fetchall()
    return render_template('note.html', table_data=table_data, name=table_name, types=types,
                           zip=zip, tables=app.config['TABLES'], column_names=column_names)


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')


@app.route('/clear_db/', methods=['POST'])
def delete_all_data():
    """ Заполнение БД данными """
    cursor.execute("DROP DATABASE EmploymentAgencyDB")
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
    delete_note(table, app.config['TABLES'][table]['key'], note_id, app.config['TABLES'])
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
    delete_table(table, app.config['TABLES'])
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
    table_name = request.path[1:request.path.find('/', 1)]
    cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    column_names = cursor.fetchall()
    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    types = cursor.fetchall()
    return render_template('add_note.html', types=types, name=table_name,
                           zip=zip, tables=app.config['TABLES'], column_names=column_names)


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
