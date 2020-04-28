import pyodbc
from flask import Flask


server = 'MK-PROBOOK\SQLEXPRESS'
database = 'EmploymentAgencyDB'
connection = pyodbc.connect('Driver={SQL Server};Server='+server+';Database='+database+';')
cursor = connection.cursor()

app = Flask(__name__)
from . import routes
