""" Скрипт заполнения БД """
from random import choice
import logging
from app import cursor, connection


AMOUNT_OF_EMPLOYERS = 50
VACANCY_PER_EMPLOYER = 10
AMOUNT_OF_POSITIONS = AMOUNT_OF_EMPLOYERS * VACANCY_PER_EMPLOYER
AMOUNT_OF_APPLICANTS = 500
AMOUNT_OF_AGENTS = 50

EMPLOYER_NAMES = ['Facebook', 'Microsoft', 'JetBrains', 'Сбербанк', 'ГазПром', 'Пятерочка',
                  'HP', '1XСтавка', 'Adidas', 'Blizzard', 'Bethesda']
EMPLOYER_ENDINGS = [' & CO', ' Entertainment', ' ОАО', ' Company', ' Industries', '']

VACANCY_STATUS = ['Свободна', 'Занята']

POSITION = ['Дворник', 'Программист', 'Начальник отдела', 'Секретарь', 'Бухгалтер',
            'Охранник', 'Помощник регионального менеджера']

NAME_MALE = ['Григорий', 'Андрей', 'Сергей', 'Михаил', 'Владимир']
NAME_FEMALE = ['Татьяна', 'Маргарита', 'Анастасия', 'Екатерина', 'Анна']
SECOND_NAME_MALE = ['Вихров', 'Минин', 'Смирнов', 'Шувалов', 'Рязанцев', 'Балабанов', 'Клюквин']
SECOND_NAME_FEMALE = ['Симонова', 'Андреева', 'Скоршева', 'Мальцева', 'Гришечкина', 'Синицина']
PATRONYMIC_MALE = ['Иванович', 'Андреевич', 'Юрьевич', 'Семенович', 'Дмитриевич']
PATRONYMIC_FEMALE = ['Андреевна', 'Семёновна', 'Сергеевна', 'Дмитриевна', 'Ивановна']

EDUCATION_DEGREE = ['Высшее', 'Среднее', 'Начальное', 'Базовое']
EDUCATION_SPHERE = ['экономики', 'программирования', 'администрирования', 'дизайна']


def fill_db():
    """ Заполнение всех таблиц БД """
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
    logging.info('Заполнение таблицы "Работодатели"...')
    sql_query = "INSERT INTO Employers (EmployerOrganization) VALUES (?);"
    for _ in range(AMOUNT_OF_EMPLOYERS):
        employer = choice(EMPLOYER_NAMES) + choice(EMPLOYER_ENDINGS)
        cursor.execute(sql_query, employer)
    connection.commit()


def fill_positions():
    """ Заполнение таблицы "Должности" """
    logging.info('Заполнение таблицы "Должности"...')
    sql_query = "INSERT INTO Positions (PositionName) VALUES (?);"
    for _ in range(AMOUNT_OF_POSITIONS):
        position = choice(POSITION)
        cursor.execute(sql_query, position)
    connection.commit()


def fill_vacancies(employer_codes):
    """ Заполнение таблицы "Вакансии" """
    logging.info('Заполнение таблицы "Вакансии"...')
    sql_query = "INSERT INTO Vacancies (EmployerCode, VacancyStatus) VALUES (?,?);"
    for employer_code in employer_codes:
        for _ in range(VACANCY_PER_EMPLOYER):
            cursor.execute(sql_query, employer_code[0], choice(VACANCY_STATUS))
    connection.commit()


def fill_education():
    """ Заполнение таблицы "Образование" """
    logging.info('Заполнение таблицы "Образование"...')
    sql_query = "INSERT INTO Education (Education) VALUES (?);"
    for _ in range(AMOUNT_OF_APPLICANTS):
        education = choice(EDUCATION_DEGREE) + ' образование в области ' + choice(EDUCATION_SPHERE)
        cursor.execute(sql_query, education)
    connection.commit()


def fill_applicants(position_codes, education_codes):
    """ Заполнение таблицы "Соискатели" """
    logging.info('Заполнение таблицы "Соискатели"...')
    sql_query = "INSERT INTO Applicants " \
                "(Name, SecondName, Patronymic, Sex, PositionCode, EducationCode)" \
                " VALUES (?,?,?,?,?,?);"
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
        cursor.execute(sql_query, name, second_name, patronymic, sex,
                       position_code[0], education_code[0])
    connection.commit()


def fill_agents():
    """ Заполнение таблицы "Агенты" """
    logging.info('Заполнение таблицы "Агенты"...')
    sql_query = "INSERT INTO Agents " \
                "(Name, SecondName, Patronymic, Sex) " \
                "VALUES (?,?,?,?);"
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
        cursor.execute(sql_query, name, second_name, patronymic, sex)
    connection.commit()


def fill_deals(applicant_codes, vacancy_codes, agent_codes):
    """ Заполнение таблицы "Сделки" """
    logging.info('Заполнение таблицы "Сделки"...')
    sql_query = "INSERT INTO Deals " \
                "(ApplicantCode, VacancyCode, AgentCode) " \
                "VALUES (?,?,?);"
    applicant_code = iter(applicant_codes)
    vacancy_code = iter(vacancy_codes)
    for _ in range(AMOUNT_OF_APPLICANTS):
        cursor.execute(sql_query, next(applicant_code)[0],
                       next(vacancy_code)[0], choice(agent_codes)[0])
    connection.commit()
