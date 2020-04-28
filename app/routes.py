""" Flask сервер работы с EmploymentAgencyDB """
from flask import render_template, url_for
from app import app, cursor


@app.route('/index')
@app.route('/')
def index():
    """ Стартовая страница приложения """
    urls = {'Соискатели': url_for('aspirants'),
            'Должности': url_for('positions'),
            'Данные о соискателях': url_for('aspirants_data'),
            'Данные об образовании': url_for('education'),
            'Вакансии': url_for('vacancies'),
            'Работодатели': url_for('employers')}
    return render_template('index.html', urls=urls)


@app.route('/aspirants')
def aspirants():
    """ Данные из таблицы соискателей """
    sql_query = "SELECT * FROM dbo.Aspirants"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('aspirants.html', results=results)


@app.route('/positions')
def positions():
    """ Данные из таблицы должностей """
    sql_query = "SELECT * FROM dbo.Positions"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('positions.html', results=results)


@app.route('/aspirants_data')
def aspirants_data():
    """ Данные из таблицы "Данные о соискателях" """
    sql_query = "SELECT * FROM dbo.AspirantData"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('aspirants_data.html', results=results)


@app.route('/education')
def education():
    """ Данные из таблицы образования """
    sql_query = "SELECT * FROM dbo.EducationData"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('education.html', results=results)


@app.route('/employers')
def employers():
    """ Данные из таблицы работодателей """
    sql_query = "SELECT * FROM dbo.Employers"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('employers.html', results=results)


@app.route('/vacancies')
def vacancies():
    """ Данные из таблицы вакансий """
    sql_query = "SELECT * FROM dbo.Vacancies"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('vacancies.html', results=results)
