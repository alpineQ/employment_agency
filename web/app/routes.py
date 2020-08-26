""" Веб сервис взаимодействия с БД "Интернет провайдера" """
from flask import render_template, redirect
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
def agents():
    """ Агенты """
    cursor.execute('SELECT * FROM Agents')
    return render_template('table.html', table=cursor.fetchall(), name="agents",
                           fields=app.config['TABLES'][0]['fields'])


@app.route('/agents/<agent_id>/')
def agent_info(agent_id):
    """ Информация о конкретном агенте """
    cursor.execute('SELECT * FROM Agents WHERE AgentCode = (?)', agent_id)
    return render_template('table.html', table=cursor.fetchall(), name="agents",
                           fields=app.config['TABLES'][0]['fields'])


@app.route('/applicants/')
def applicants():
    """ Соискатели """
    cursor.execute('SELECT * FROM Applicants')
    return render_template('table.html', table=cursor.fetchall(), name="applicants",
                           fields=app.config['TABLES'][1]['fields'])


@app.route('/applicants/<applicant_id>/')
def applicant_info(applicant_id):
    """ Информация о конкретном соискателе """
    cursor.execute('SELECT * FROM Applicants WHERE ApplicantCode = (?)', applicant_id)
    return render_template('table.html', table=cursor.fetchall(), name="applicants",
                           fields=app.config['TABLES'][1]['fields'])


@app.route('/deals/')
def deals():
    """ Сделки """
    cursor.execute('SELECT * FROM Deals')
    return render_template('table.html', table=cursor.fetchall(), name="deals",
                           fields=app.config['TABLES'][2]['fields'])


@app.route('/deals/<deal_id>/')
def deal_info(deal_id):
    """ Информация о конкретной сделке """
    cursor.execute('SELECT * FROM Deals WHERE DealCode = (?)', deal_id)
    return render_template('table.html', table=cursor.fetchall(), name="deals",
                           fields=app.config['TABLES'][2]['fields'])


@app.route('/education/')
def education():
    """ Образование """
    cursor.execute('SELECT * FROM Education')
    return render_template('table.html', table=cursor.fetchall(), name="education",
                           fields=app.config['TABLES'][3]['fields'])


@app.route('/education/<education_id>/')
def education_info(education_id):
    """ Информация о конкретном образовании """
    cursor.execute('SELECT * FROM Education WHERE EducationCode = (?)', education_id)
    return render_template('table.html', table=cursor.fetchall(), name="education",
                           fields=app.config['TABLES'][3]['fields'])


@app.route('/employers/')
def employers():
    """ Работодатели """
    cursor.execute('SELECT * FROM Employers')
    return render_template('table.html', table=cursor.fetchall(), name="employers",
                           fields=app.config['TABLES'][4]['fields'])


@app.route('/employers/<employers_id>/')
def employers_info(employers_id):
    """ Информация о конкретном работодателе """
    cursor.execute('SELECT * FROM Employers WHERE EmployerCode = (?)', employers_id)
    return render_template('table.html', table=cursor.fetchall(), name="employers",
                           fields=app.config['TABLES'][4]['fields'])


@app.route('/positions/')
def positions():
    """ Должности """
    cursor.execute('SELECT * FROM Positions')
    return render_template('table.html', table=cursor.fetchall(), name="positions",
                           fields=app.config['TABLES'][5]['fields'])


@app.route('/positions/<positions_id>/')
def positions_info(positions_id):
    """ Информация о конкретной должности """
    cursor.execute('SELECT * FROM Positions WHERE PositionCode = (?)', positions_id)
    return render_template('table.html', table=cursor.fetchall(), name="positions",
                           fields=app.config['TABLES'][5]['fields'])


@app.route('/vacancies/')
def vacancies():
    """ Вакансии """
    cursor.execute('SELECT * FROM Vacancies')
    return render_template('table.html', table=cursor.fetchall(), name="vacancies",
                           fields=app.config['TABLES'][6]['fields'])


@app.route('/vacancies/<vacancy_id>/')
def vacancy_info(vacancy_id):
    """ Информация о конкретной вакансии """
    cursor.execute('SELECT * FROM Vacancies WHERE VacancyCode = (?)', vacancy_id)
    return render_template('table.html', table=cursor.fetchall(), name="vacancy",
                           fields=app.config['TABLES'][6]['fields'])


@app.route('/fill_db/', methods=['POST'])
def generate_data():
    """ Заполнение БД данными """
    fill_db()
    return redirect('/')
