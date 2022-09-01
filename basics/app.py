from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secretsecretsecret'

def connect_db():
    sql = sqlite3.connect('/Users/pilona/Documents/Repos/FlaskCourse/basics/data.db')
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
    return '<h1>Hello, World!</h1>'

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return render_template('home.html', name=name, display=False, mylist=["uno", "dos", "tres", "cuatro"], results = results)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotInSession'
    return jsonify({'key': 'value', 'listkey': [1,2,3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>{name}, estás en la página de query, desde {location}</h1>'

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')

    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('INSERT INTO users (name, location) values (?, ?)', [name, location])
        db.commit()

        #return f'<h2>Hola, {name}, eres de {location}, el formulario se envió exitosamente.</h2>'
        return redirect(url_for('home', name=name, location=location))

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute("SELECT id, name, location from users")
    results = cur.fetchall()
    return f"id es {results[2]['id']}, locacion es {results[2]['location']}, nombre es {results[2]['name']}"

if __name__ == '__main__':
    app.run()
