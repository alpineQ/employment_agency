""" Flask сервер работы с EmploymentAgencyDB """
from app import app, connection


app.run(host='0.0.0.0', port=80)
connection.close()
