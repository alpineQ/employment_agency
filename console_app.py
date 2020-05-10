""" Консольное приложение для работы с EmploymentAgencyDB """
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
print('Connection successful!')

print('"exit" для выхода')
request = ''
while request != 'exit':
    request = input('Запрос: ')
    cursor.execute(request)
    results = cursor.fetchall()
    print(results)

connection.close()
