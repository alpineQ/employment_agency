""" Flask сервер работы с EmploymentAgencyDB """
from app import app, connection


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    connection.close()
