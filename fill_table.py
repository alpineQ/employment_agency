""" Скрипт заполнения БД """
from random import choice
import pyodbc

SERVER = 'localhost'
DATABASE = 'EmploymentAgencyDB'
USERNAME = input("Имя пользователя: ")
PASSWORD = input("Пароль: ")

# pylint: disable=invalid-name
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=' + SERVER + ';'
                            'Database=' + DATABASE + ';'
                            'uid=' + USERNAME + ';'
                            'PWD=' + PASSWORD)
cursor = connection.cursor()


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


print('Заполнение таблицы "Работодатели"...')
SQL_QUERY = f"INSERT INTO dbo.Employers (EmployerOrganization) VALUES (?);"
for i in range(AMOUNT_OF_EMPLOYERS):
    employer = choice(EMPLOYER_NAMES) + choice(EMPLOYER_ENDINGS)
    cursor.execute(SQL_QUERY, employer)
connection.commit()


print('Заполнение таблицы "Должности"...')
SQL_QUERY = f"INSERT INTO dbo.Positions (Position) VALUES (?);"
for i in range(AMOUNT_OF_POSITIONS):
    position = choice(POSITION) + choice(POSITION_ENDING)
    cursor.execute(SQL_QUERY, position)
connection.commit()


# pylint: disable=invalid-name
cursor.execute("SELECT PositionCode FROM dbo.Positions")
position_codes = cursor.fetchall()

cursor.execute("SELECT EmployerCode FROM dbo.Employers")
employer_codes = cursor.fetchall()


print('Заполнение таблицы "Вакансии"...')
SQL_QUERY = f"INSERT INTO dbo.Vacancies (EmployerCode, PositionCode, VacancyStatus) VALUES (?,?,?);"
position_code = iter(position_codes)
for employer_code in employer_codes:
    for i in range(VACANCY_PER_EMPLOYER):
        cursor.execute(SQL_QUERY, employer_code[0], next(position_code)[0], choice(VACANCY_STATUS))
connection.commit()


print('Заполнение таблицы "Соискатели"...')
SQL_QUERY = f"INSERT INTO dbo.Applicants (ApplicantFullName, PositionCode) VALUES (?,?);"
for i in range(AMOUNT_OF_APPLICANTS):
    if choice(['male', 'female']) == 'male':
        applicant = choice(NAME_MALE) + choice(SECOND_NAME_MALE) + choice(PATRONYMIC_MALE)
    else:
        applicant = choice(NAME_FEMALE) + choice(SECOND_NAME_FEMALE) + choice(PATRONYMIC_FEMALE)
    position_code = choice(position_codes)
    cursor.execute(SQL_QUERY, applicant, position_code[0])
connection.commit()


print('Заполнение таблицы "Образование"...')
SQL_QUERY = f"INSERT INTO dbo.EducationData (Education) VALUES (?);"
for i in range(AMOUNT_OF_APPLICANTS):
    education = choice(EDUCATION_DEGREE) + ' образование в области ' + choice(EDUCATION_SPHERE)
    cursor.execute(SQL_QUERY, education)
connection.commit()


cursor.execute("SELECT ApplicantCode FROM dbo.Applicants")
applicant_codes = cursor.fetchall()

cursor.execute("SELECT EducationCode FROM dbo.EducationData")
education_codes = cursor.fetchall()


print('Заполнение таблицы "Данные Соискателей"...')
SQL_QUERY = f"INSERT INTO dbo.ApplicantData (ApplicantCode, EducationCode) VALUES (?,?);"
for i in range(AMOUNT_OF_APPLICANTS):
    applicant_code = choice(applicant_codes)
    education_code = choice(education_codes)
    cursor.execute(SQL_QUERY, applicant_code[0], education_code[0])

    applicant_codes.remove(applicant_code)
    education_codes.remove(education_code)
connection.commit()


connection.close()
print('Успех!')
