""" Flask сервер работы с EmploymentAgencyDB """
import pyodbc
from flask import Flask

# pylint: disable=invalid-name
server = 'localhost'
database = 'EmploymentAgencyDB'
password = 'QwErTy123!'
username = 'SA'
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server='+server+';'
                            'Database='+database+';'
                            'uid='+username+';'
                            'PWD='+password)
cursor = connection.cursor()

app = Flask(__name__)
# pylint: disable=wrong-import-position
from . import routes
