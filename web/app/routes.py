""" Веб сервис взаимодействия с БД "Интернет провайдера" """
import logging
from flask import render_template, redirect, request
from app.fill_table import fill_db
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
def table_route():
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
def note_info(note_id):
    """ Информация о конкретной записи """
    table_name = request.path[1:request.path.find('/', 1)]
    cursor.execute(f"SELECT * FROM {app.config['TABLES'][table_name]['db']} "
                   f"WHERE {app.config['TABLES'][table_name]['key']} = (?)", note_id)
    table_data = cursor.fetchone()
    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{app.config['TABLES'][table_name]['db']}'")
    types = cursor.fetchall()
    return render_template('note.html', table_data=table_data, name=table_name,
                           types=types, zip=zip, tables=app.config['TABLES'])


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')


@app.route('/clear_db/', methods=['POST'])
def delete_all_data():
    """ Заполнение БД данными """
    cursor.execute("DROP DATABASE EmploymentAgencyDB")
    logging.info(cursor.fetchall())
    return redirect('/')
