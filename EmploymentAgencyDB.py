import pyodbc


server = 'MK-PROBOOK\SQLEXPRESS'
database = 'EmploymentAgencyDB'
username = 'MaxK'
password = '-*/-*/'
# cnxn = pypyodbc.connect('Driver={SQL Server};Server='+server+';Database='+database+';UID='+username+';PWD='+ password)
connection = pyodbc.connect('Driver={SQL Server};Server='+server+';Database='+database+';')
cursor = connection.cursor()

tsql = "SELECT PositionCode, Position FROM dbo.Positions"

cursor.execute(tsql)
results = cursor.fetchall()
print(results)

connection.close()
