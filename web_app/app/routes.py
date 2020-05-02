""" Flask сервер работы с EmploymentAgencyDB """
from flask import render_template
from . import app, cursor, table_info


@app.route('/index')
@app.route('/')
def index():
    """ Стартовая страница приложения """
    return render_template('index.html', urls=table_info)


@app.route('/<table_name>')
def table_page(table_name):
    """ Данные из таблицы соискателей """
    if table_name not in table_info:
        return 'Not found', 404
    sql_query = f"SELECT * FROM {table_info[table_name]['db']}"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('table_page.html', results=results)
