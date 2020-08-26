""" Веб сервис взаимодействия с БД "Интернет провайдера" """
from flask import render_template, redirect
from app.utils import execute_query
from app.fill_table import fill_db
from app import app


@app.route('/')
def index():
    """ Список всех таблиц БД """
    return render_template('index.html', tables=app.config['TABLES'])


@app.route('/agents/')
def agents():
    """ Агенты """
    result = execute_query('SELECT * FROM Agents')
    return render_template('table.html', table=result, name="agents",
                           fields=app.config['TABLES'][0]['fields'])


@app.route('/applicants/')
def applicants():
    """ Соискатели """
    result = execute_query('SELECT * FROM Applicants')
    return render_template('table.html', table=result, name="applicants",
                           fields=app.config['TABLES'][1]['fields'])


@app.route('/deals/')
def deals():
    """ Сделки """
    result = execute_query('SELECT * FROM Deals')
    return render_template('table.html', table=result, name="deals",
                           fields=app.config['TABLES'][2]['fields'])


@app.route('/education/')
def education():
    """ Образование """
    result = execute_query('SELECT * FROM Education')
    return render_template('table.html', table=result, name="education",
                           fields=app.config['TABLES'][3]['fields'])


@app.route('/employers/')
def employers():
    """ Работодатели """
    result = execute_query('SELECT * FROM Employers')
    return render_template('table.html', table=result, name="employers",
                           fields=app.config['TABLES'][4]['fields'])


@app.route('/positions/')
def positions():
    """ Должности """
    result = execute_query('SELECT * FROM Positions')
    return render_template('table.html', table=result, name="positions",
                           fields=app.config['TABLES'][5]['fields'])


@app.route('/vacancies/')
def vacancies():
    """ Вакансии """
    result = execute_query('SELECT * FROM Vacancies')
    return render_template('table.html', table=result, name="vacancies",
                           fields=app.config['TABLES'][6]['fields'])


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')
