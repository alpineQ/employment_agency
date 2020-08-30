""" Скрипт заполнения БД """
from random import choice, randint, randrange
from string import digits, ascii_lowercase
from datetime import date, timedelta
import logging
from app import app

AMOUNT_OF_AGENTS = randint(20, 50)
AMOUNT_OF_APPLICANTS = randint(400, 500)
AMOUNT_OF_DEALS = randint(200, 400)
AMOUNT_OF_EMPLOYERS = randint(50, 100)
VACANCY_PER_EMPLOYER = randint(5, 10)
AMOUNT_OF_POSITIONS = AMOUNT_OF_EMPLOYERS * VACANCY_PER_EMPLOYER

EMPLOYER_NAMES = ['Facebook', 'Microsoft', 'JetBrains', 'Сбербанк', 'ГазПром', 'Пятерочка',
                  'HP', '1XСтавка', 'Adidas', 'Blizzard', 'Bethesda']
EMPLOYER_ENDINGS = [' & CO', ' Entertainment', ' ОАО', ' Company', ' Industries', '']

VACANCY_STATUS = ['Свободна', 'Занята']

POSITION = ['Дворник', 'Программист', 'Начальник отдела', 'Секретарь', 'Бухгалтер',
            'Охранник', 'Помощник регионального менеджера', 'Инженер', 'Повар',
            'Строитель', 'HR']
INDUSTRIES = ['IT', 'Туризм', 'Искусство', 'Строительство', 'HR', 'Шоу бизнес']

NAME_MALE = ['Григорий', 'Андрей', 'Сергей', 'Михаил', 'Владимир', 'Максим', 'Игорь', 'Егор']
NAME_FEMALE = ['Татьяна', 'Маргарита', 'Анастасия', 'Екатерина', 'Анна', 'Евгения', 'Елена']
SECOND_NAME_MALE = ['Вихров', 'Минин', 'Смирнов', 'Шувалов', 'Рязанцев', 'Балабанов', 'Клюквин']
SECOND_NAME_FEMALE = ['Симонова', 'Андреева', 'Скоршева', 'Мальцева', 'Гришечкина', 'Синицина']
PATRONYMIC_MALE = ['Иванович', 'Андреевич', 'Юрьевич', 'Семенович', 'Дмитриевич']
PATRONYMIC_FEMALE = ['Андреевна', 'Семёновна', 'Сергеевна', 'Дмитриевна', 'Ивановна']

EDUCATION_DEGREE = ['Высшее', 'Среднее', 'Начальное', 'Базовое']
EDUCATION_FIELD = ['Экономика', 'Информационная безопасность', 'Менеджмент', 'Дизайн']


def fill_db():
    """ Заполнение всех таблиц БД """
    cursor = app.config['cursor']
    fill_employers()
    fill_positions()
    fill_agents()
    fill_education()

    cursor.execute("SELECT EmployerCode FROM Employers")
    employer_codes = cursor.fetchall()
    fill_vacancies(employer_codes)

    cursor.execute("SELECT PositionCode FROM Positions")
    position_codes = cursor.fetchall()
    cursor.execute("SELECT EducationCode FROM Education")
    education_codes = cursor.fetchall()
    fill_applicants(position_codes, education_codes)

    cursor.execute("SELECT ApplicantCode FROM Applicants")
    applicant_codes = cursor.fetchall()
    cursor.execute("SELECT VacancyCode FROM Vacancies")
    vacancy_codes = cursor.fetchall()
    cursor.execute("SELECT AgentCode FROM Agents")
    agent_codes = cursor.fetchall()
    fill_deals(applicant_codes, vacancy_codes, agent_codes)


def fill_employers():
    """ Заполнение таблицы "Работодатели" """
    cursor = app.config['cursor']
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Работодатели"...')
    sql_query = "INSERT INTO Employers " \
                "(EmployerOrganization, Email, PhoneNumber) " \
                "VALUES (?,?,?);"
    for _ in range(AMOUNT_OF_EMPLOYERS):
        employer = choice(EMPLOYER_NAMES) + choice(EMPLOYER_ENDINGS)
        cursor.execute(sql_query, employer, generate_email(), generate_phone_number())
    app.config['connection'].commit()


def fill_positions():
    """ Заполнение таблицы "Должности" """
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Должности"...')
    sql_query = "INSERT INTO Positions (PositionName, Industry) VALUES (?,?);"
    for _ in range(AMOUNT_OF_POSITIONS):
        cursor.execute(sql_query, choice(POSITION), choice(INDUSTRIES))
    app.config['connection'].commit()


def fill_vacancies(employer_codes):
    """ Заполнение таблицы "Вакансии" """
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Вакансии"...')
    sql_query = "INSERT INTO Vacancies " \
                "(EmployerCode, VacancyStatus, Industry, PlacementDate, " \
                "RequiredEducation, Salary) " \
                "VALUES (?,?,?,?,?,?);"
    for employer_code in employer_codes:
        for _ in range(randint(5, 10)):
            degree = choice(EDUCATION_DEGREE)
            industry = choice(EDUCATION_FIELD)
            education = f'{degree} образование в области {industry}'
            salary = randint(10, 300)*1000
            cursor.execute(sql_query, employer_code[0], choice(VACANCY_STATUS), choice(INDUSTRIES),
                           generate_date(date(2000, 1, 1), date(2020, 1, 1)), education, salary)
    app.config['connection'].commit()


def fill_education():
    """ Заполнение таблицы "Образование" """
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Образование"...')
    sql_query = "INSERT INTO Education (EducationDegree, EducationField) " \
                "VALUES (?,?);"
    for _ in range(AMOUNT_OF_APPLICANTS):
        cursor.execute(sql_query, choice(EDUCATION_DEGREE), choice(EDUCATION_FIELD))
    app.config['connection'].commit()


def fill_applicants(position_codes, education_codes):
    """ Заполнение таблицы "Соискатели" """
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Соискатели"...')
    sql_query = "INSERT INTO Applicants " \
                "(Name, SecondName, Patronymic, Sex, Email, Birthday, " \
                "PhoneNumber, PositionCode, EducationCode, JobExperience) " \
                "VALUES (?,?,?,?,?,?,?,?,?,?);"
    for _ in range(AMOUNT_OF_APPLICANTS):
        if choice([True, False]):
            name = choice(NAME_MALE)
            second_name = choice(SECOND_NAME_MALE)
            patronymic = choice(PATRONYMIC_MALE)
            sex = 'М'
        else:
            name = choice(NAME_FEMALE)
            second_name = choice(SECOND_NAME_FEMALE)
            patronymic = choice(PATRONYMIC_FEMALE)
            sex = 'Ж'
        position_code = choice(position_codes)
        education_code = choice(education_codes)
        cursor.execute(sql_query, name, second_name, patronymic, sex, generate_email(),
                       generate_date(date(1970, 1, 1), date(2000, 1, 1)), generate_phone_number(),
                       position_code[0], education_code[0], randint(0, 10))
    app.config['connection'].commit()


def fill_agents():
    """ Заполнение таблицы "Агенты" """
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Агенты"...')
    sql_query = "INSERT INTO Agents " \
                "(Name, SecondName, Patronymic, Sex, Email, PhoneNumber) " \
                "VALUES (?,?,?,?,?,?);"
    for _ in range(AMOUNT_OF_AGENTS):
        if choice([True, False]):
            name = choice(NAME_MALE)
            second_name = choice(SECOND_NAME_MALE)
            patronymic = choice(PATRONYMIC_MALE)
            sex = 'М'
        else:
            name = choice(NAME_FEMALE)
            second_name = choice(SECOND_NAME_FEMALE)
            patronymic = choice(PATRONYMIC_FEMALE)
            sex = 'Ж'
        cursor.execute(sql_query, name, second_name, patronymic, sex,
                       generate_email(), generate_phone_number())
    app.config['connection'].commit()


def fill_deals(applicant_codes, vacancy_codes, agent_codes):
    """ Заполнение таблицы "Сделки" """
    cursor = app.config['cursor']
    logging.info('Заполнение таблицы "Сделки"...')
    sql_query = "INSERT INTO Deals " \
                "(ApplicantCode, VacancyCode, AgentCode, WasPaid, IssueDate, " \
                "PaymentDate, CommissionFee) " \
                "VALUES (?,?,?,?,?,?,?);"
    for _ in range(AMOUNT_OF_DEALS):
        issue_date = generate_date(date(2000, 1, 1), date(2020, 1, 1))
        was_paid = choice([True, False])
        payment_date = generate_date(issue_date, date(2020, 1, 1)) if was_paid else None

        cursor.execute(sql_query, choice(applicant_codes)[0], choice(vacancy_codes)[0],
                       choice(agent_codes)[0], 1 if was_paid else 0, issue_date, payment_date,
                       randint(2, 10)*1000)
    app.config['connection'].commit()


def generate_phone_number():
    """ Генерация номера телефона """
    return f'+7({randint(900, 999)}){randint(100, 999)}-{randint(10, 99)}-{randint(10, 99)}'


def generate_email():
    """ Генерация адреса элктронной почты """
    extensions = ['com', 'net', 'org', 'gov']
    domains = ['gmail', 'yahoo', 'comcast', 'rambler', 'mail', 'hotmail', 'outlook', 'yandex']

    ext = choice(extensions)
    domain = choice(domains)
    username = ''.join(choice(ascii_lowercase + digits) for _ in range(randint(6, 12)))

    return f'{username}@{domain}.{ext}'


def generate_date(start_date, end_date):
    """ Генерация случайной даты """
    return start_date + timedelta(days=randrange((end_date - start_date).days))
