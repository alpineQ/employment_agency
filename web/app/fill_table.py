""" Скрипт заполнения БД """
from random import choice
from app import cursor, connection

# pylint: disable=invalid-name


AMOUNT_OF_EMPLOYERS = 50
VACANCY_PER_EMPLOYER = 10
AMOUNT_OF_POSITIONS = AMOUNT_OF_EMPLOYERS * VACANCY_PER_EMPLOYER
AMOUNT_OF_APPLICANTS = 500

EMPLOYER_NAMES = ['Facebook', 'Microsoft', 'JetBrains', 'Сбербанк', 'ГазПром', 'Пятерочка',
                  'HP', '1XСтавка', 'Adidas', 'Blizzard', 'Bethesda']
EMPLOYER_ENDINGS = [' & CO', ' Entertainment', ' ОАО', ' Company', ' Industries', '']

VACANCY_STATUS = ['Свободна', 'Занята']

POSITION = ['Дворник', 'Программист', 'Начальник отдела', 'Секретарь', 'Бухгалтер',
            'Охранник', 'Помощник регионального менеджера']
POSITION_ENDING = [' на полставки', '-грузчик', ' стажер', '', '', '', '', '']

NAME_MALE = ['Григорий', 'Андрей', 'Сергей', 'Михаил', 'Владимир']
NAME_FEMALE = ['Татьяна', 'Маргарита', 'Анастасия', 'Екатерина', 'Анна']
SECOND_NAME_MALE = [' Рогов', ' Минин', ' Смирнов', ' Ковпак', ' Новосёлов']
SECOND_NAME_FEMALE = [' Симонова', ' Андреева', ' Скоршева', ' Мальцева', ' Кобелева']
PATRONYMIC_MALE = [' Иванович', ' Андреевич', ' Юрьевич', ' Семенович', ' Дмитриевич']
PATRONYMIC_FEMALE = [' Андреевна', ' Семёновна', ' Сергеевна', ' Дмитриевна', ' Ивановна']

EDUCATION_DEGREE = ['Высшее', 'Среднее', 'Начальное', 'Базовое']
EDUCATION_SPHERE = ['экономики', 'программирования', 'администрирования', 'дизайна']


def fill_db():
    """ Заполнение всех таблиц БД """
    fill_employers()
    fill_positions()

    cursor.execute("SELECT PositionCode FROM dbo.Positions")
    position_codes = cursor.fetchall()
    cursor.execute("SELECT EmployerCode FROM dbo.Employers")
    employer_codes = cursor.fetchall()

    fill_vacancies(employer_codes)
    fill_applicants(position_codes)
    fill_education()

    cursor.execute("SELECT ApplicantCode FROM dbo.Applicants")
    applicant_codes = cursor.fetchall()
    cursor.execute("SELECT EducationCode FROM dbo.EducationData")
    education_codes = cursor.fetchall()

    fill_applicant_data(applicant_codes, education_codes)


def fill_employers():
    """ Заполнение таблицы "Работодатели" """
    print('Заполнение таблицы "Работодатели"...')
    sql_query = "INSERT INTO dbo.Employers (EmployerOrganization) VALUES (?);"
    for _ in range(AMOUNT_OF_EMPLOYERS):
        employer = choice(EMPLOYER_NAMES) + choice(EMPLOYER_ENDINGS)
        cursor.execute(sql_query, employer)
    connection.commit()


def fill_positions():
    """ Заполнение таблицы "Должности" """
    print('Заполнение таблицы "Должности"...')
    sql_query = "INSERT INTO dbo.Positions (PositionName) VALUES (?);"
    for _ in range(AMOUNT_OF_POSITIONS):
        position = choice(POSITION) + choice(POSITION_ENDING)
        cursor.execute(sql_query, position)
    connection.commit()


def fill_vacancies(employer_codes):
    """ Заполнение таблицы "Вакансии" """
    print('Заполнение таблицы "Вакансии"...')
    sql_query = "INSERT INTO dbo.Vacancies (EmployerCode, VacancyStatus) VALUES (?,?,?);"
    for employer_code in employer_codes:
        for _ in range(VACANCY_PER_EMPLOYER):
            cursor.execute(sql_query, employer_code[0], choice(VACANCY_STATUS))
    connection.commit()


def fill_applicants(position_codes):
    """ Заполнение таблицы "Соискатели" """
    print('Заполнение таблицы "Соискатели"...')
    sql_query = "INSERT INTO dbo.Applicants (ApplicantFullName, PositionCode) VALUES (?,?);"
    for _ in range(AMOUNT_OF_APPLICANTS):
        if choice(['male', 'female']) == 'male':
            applicant = choice(NAME_MALE) + choice(SECOND_NAME_MALE) + choice(PATRONYMIC_MALE)
        else:
            applicant = choice(NAME_FEMALE) + choice(SECOND_NAME_FEMALE) + choice(PATRONYMIC_FEMALE)
        position_code = choice(position_codes)
        cursor.execute(sql_query, applicant, position_code[0])
    connection.commit()


def fill_education():
    """ Заполнение таблицы "Образование" """
    print('Заполнение таблицы "Образование"...')
    sql_query = "INSERT INTO dbo.EducationData (Education) VALUES (?);"
    for _ in range(AMOUNT_OF_APPLICANTS):
        education = choice(EDUCATION_DEGREE) + ' образование в области ' + choice(EDUCATION_SPHERE)
        cursor.execute(sql_query, education)
    connection.commit()


def fill_applicant_data(applicant_codes, education_codes):
    """ Заполнение таблицы "Данные соискателей" """
    print('Заполнение таблицы "Данные Соискателей"...')
    sql_query = "INSERT INTO dbo.ApplicantData (ApplicantCode, EducationCode) VALUES (?,?);"
    for _ in range(AMOUNT_OF_APPLICANTS):
        applicant_code = choice(applicant_codes)
        education_code = choice(education_codes)
        cursor.execute(sql_query, applicant_code[0], education_code[0])

        applicant_codes.remove(applicant_code)
        education_codes.remove(education_code)
    connection.commit()