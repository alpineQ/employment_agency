""" Веб сервис взаимодействия с БД "Интернет провайдера" """
import logging
from flask import render_template, redirect, request
from app.fill_table import fill_db
from app import app, cursor


@app.route('/')
def index():
    """ Список всех таблиц БД """
    for table in app.config['TABLES']:
        cursor.execute(f"SELECT COUNT(*) FROM {table['db']}")
        table['n_records'] = cursor.fetchone()[0]
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
    table_info = [table for table in app.config['TABLES'] if table['url'] == request.path][0]
    cursor.execute(f"SELECT * FROM {table_info['db']}")
    table_data = cursor.fetchall()
    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_info['db']}'")
    types = cursor.fetchall()
    return render_template('table.html', table=table_data, table_info=table_info,
                           types=types, zip=zip)


@app.route('/agents/<note_id>/')
@app.route('/applicants/<note_id>/')
@app.route('/deals/<note_id>/')
@app.route('/education/<note_id>/')
@app.route('/employers/<note_id>/')
@app.route('/positions/<note_id>/')
@app.route('/vacancies/<note_id>/')
def note_info(note_id):
    """ Информация о конкретной записи """
    table_name = request.path[:request.path.find('/', 1)+1]
    table_info = [table for table in app.config['TABLES'] if table['url'] == table_name][0]
    cursor.execute(f"SELECT * FROM {table_info['db']} WHERE {table_info['key']} = (?)", note_id)
    table_data = cursor.fetchall()
    cursor.execute(f"SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{table_info['db']}'")
    types = cursor.fetchall()
    return render_template('table.html', table=table_data, table_info=table_info,
                           types=types, zip=zip)


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
