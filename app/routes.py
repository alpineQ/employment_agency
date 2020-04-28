from flask import render_template
from . import app, cursor


@app.route('/positions')
def positions():
    sql_query = "SELECT PositionCode, Position FROM dbo.Positions"

    cursor.execute(sql_query)
    results = cursor.fetchall()
    return render_template('positions.html', results=results)

