""" Flask сервер работы с EmploymentAgencyDB """
from flask import Flask
import pyodbc
from .config import Config


# pylint: disable=invalid-name
app = Flask(__name__)
app.config.from_object(Config)
table_info = app.config['TABLE_INFO']

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=' + app.config['SERVER'] + ';'
                            'Database=' + app.config['DATABASE'] + ';'
                            'uid=' + app.config['USERNAME'] + ';'
                            'PWD=' + app.config['PASSWORD'])
cursor = connection.cursor()

# pylint: disable=wrong-import-position
from . import routes
