from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.config['DEBUG'] = True

def connect_db():
    sql = sqlite3.connect('/Users/pilona/Documents/Repos/FlaskCourse/activity_tracker/tracker.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date']

        dt = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(dt, '%Y%m%d')

        db.execute('insert into log_date (entry_date) values (?)', [database_date])
        db.commit()

    cur = db.execute('select entry_date from log_date order by entry_date desc')
    results = cur.fetchall()

    pretty_results = []

    for i in results:
        single_date = {}
        d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        single_date['entry_date'] = datetime.strftime(d, '%B %d, %Y')

        pretty_results.append(single_date)

    return render_template('home.html', results=pretty_results)

@app.route('/view/<date>', methods=['GET', 'POST'])
def view(date):
    if request.method == 'POST':
        return ''

    db = get_db()

    cur = db.execute('select entry_date from log_date where entry_date = ?', [date])
    result = cur.fetchone()

    d = datetime.strptime(str(result['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(d, '%B %d, %Y')

    activity_cur = db.execute('select id, name from activities')

    activity_results = activity_cur.fetchall()

    return render_template('day.html', date = pretty_date, activity_results = activity_results)

@app.route('/add', methods=['GET', 'POST'])
def add():

    db = get_db()

    if request.method == 'POST':
        name = request.form['activity-name']
        time = float(request.form['time'])
        distance = float(request.form['distance'])
        calories = float(request.form['calories'])
        date = request.form['date']

        db.execute('insert into activities (name, time, distance, calories, date) values (?,?,?,?,?)',
        [name, time, distance, calories, date])
        db.commit()
    cur = db.execute('select name, time, distance, calories, date from activities')
    results = cur.fetchall()

    return render_template('add.html', results=results)

if __name__ == '__main__':
    app.run()
