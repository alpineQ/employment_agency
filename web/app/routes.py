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
    result = execute_query('SELECT * FROM dbo.Agents')
    return str(result)


@app.route('/applicants/')
def applicants():
    """ Соискатели """
    result = execute_query('SELECT * FROM dbo.Applicants')
    return str(result)


@app.route('/deals/')
def deals():
    """ Сделки """
    result = execute_query('SELECT * FROM dbo.Deals')
    return render_template('table.html', table=result, fields=['Service ID', 'Name', 'Price'])


@app.route('/education/')
def education():
    """ Образование """
    result = execute_query('SELECT * FROM dbo.Education')
    return str(result)


@app.route('/employers/')
def employers():
    """ Работодатели """
    fields = ['Employer ID',
              'Organization',
              'Address',
              'Phone number',
              'Email',
              'License']
    result = execute_query('SELECT * FROM dbo.Employers')
    return render_template('table.html', table=result, fields=fields)


@app.route('/positions/')
def positions():
    """ Должности """
    result = execute_query('SELECT * FROM dbo.Positions')
    return str(result)


@app.route('/vacancies/')
def vacancies():
    """ Вакансии """
    result = execute_query('SELECT * FROM dbo.Vacancies')
    return str(result)


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')
