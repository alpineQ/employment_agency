""" Консольное приложение для работы с EmploymentAgencyDB """
# pylint: disable=c-extension-no-member
import pyodbc


if __name__ == '__main__':
    SERVER = 'localhost'
    DATABASE = 'EmploymentAgencyDB'
    username = input("Имя пользователя: ")
    password = input("Пароль: ")

    connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                'Server=' + SERVER + ';'
                                'Database=' + DATABASE + ';'
                                'uid=' + username + ';'
                                'PWD=' + password)
    cursor = connection.cursor()
    print('Connection successful!')

    print('"exit" для выхода')
    while request := '' != 'exit':
        request = input('Запрос: ')
        cursor.execute(request)
        results = cursor.fetchall()
        print(results)

    connection.close()
