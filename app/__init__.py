""" Flask сервер работы с EmploymentAgencyDB """
import pyodbc
from flask import Flask

# pylint: disable=invalid-name
server = '.\\SQLEXPRESS'
database = 'EmploymentAgencyDB'
connection = pyodbc.connect('Driver={SQL Server};Server='+server+';Database='+database+';')
cursor = connection.cursor()

app = Flask(__name__)
# pylint: disable=wrong-import-position
from . import routes
