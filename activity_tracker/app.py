from flask import Flask, render_template, g, request
import sqlite3

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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

@app.route('/add', methods=['GET', 'POST'])
def add():

    db = get_db()

    if request.method == 'POST':
        name = request.form['activity-name']
        time = float(request.form['time'])
        distance = float(request.form['distance'])
        calories = float(request.form['calories'])


        db.execute('insert into activities (name, time, distance, calories) values (?,?,?,?)',
        [name, time, distance, calories])
        db.commit()
    cur = db.execute('select name, time, distance, calories from activities')
    results = cur.fetchall()

    return render_template('add.html', results=results)

if __name__ == '__main__':
    app.run()
