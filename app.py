from flask import Flask, jsonify, request, url_for, redirect, session, render_template
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secretsecretsecret'

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name, display=False, mylist=["uno", "dos", "tres", "cuatro"])

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

        #return f'<h2>Hola, {name}, eres de {location}, el formulario se envió exitosamente.</h2>'
        return redirect(url_for('home', name=name, location=location))

if __name__ == '__main__':
    app.run()
