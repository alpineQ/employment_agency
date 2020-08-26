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
    fields = [
        'Code',
        'Name'
        'Second name',
        'Patronymic',
        'Phone number',
        'Email',
        'Sex'
    ]
    result = execute_query('SELECT * FROM Agents')
    return render_template('table.html', table=result, fields=fields)


@app.route('/applicants/')
def applicants():
    """ Соискатели """
    fields = [
        'Code',
        'Name',
        'Second name',
        'Patronymic',
        'Application Date',
        'Qualification',
        'Birthday',
        'Sex',
        'Address',
        'Phone number',
        'Job experience',
        'Email',
        'Education code',
        'Position code'
    ]
    result = execute_query('SELECT * FROM Applicants')
    return render_template('table.html', table=result, fields=fields)


@app.route('/deals/')
def deals():
    """ Сделки """
    fields = [
        'Code',
        'Applicant code',
        'Vacancy code',
        'Issue date',
        'Commission fee',
        'Was paid?',
        'Payment date',
        'Agent code'
    ]
    result = execute_query('SELECT * FROM Deals')
    return render_template('table.html', table=result, fields=fields)


@app.route('/education/')
def education():
    """ Образование """
    fields = ['Code',
              'Education',
              'Note',
              'Institution']
    result = execute_query('SELECT * FROM Education')
    return render_template('table.html', table=result, fields=fields)


@app.route('/employers/')
def employers():
    """ Работодатели """
    fields = ['Employer ID',
              'Organization',
              'Address',
              'Phone number',
              'Email',
              'License']
    result = execute_query('SELECT * FROM Employers')
    return render_template('table.html', table=result, fields=fields)


@app.route('/positions/')
def positions():
    """ Должности """
    fields = ['Code',
              'Position',
              'Industry']
    result = execute_query('SELECT * FROM Positions')
    return render_template('table.html', table=result, fields=fields)


@app.route('/vacancies/')
def vacancies():
    """ Вакансии """
    fields = ['Code',
              'Date',
              'Salary',
              'Schedule',
              'VacancyStatus',
              'Industry',
              'RequiredEducation',
              'Qualification',
              'EmployerCode']
    result = execute_query('SELECT * FROM Vacancies')
    return render_template('table.html', table=result, fields=fields)


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')
