from flask import Flask, jsonify, request, url_for, redirect, session, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    return f'<h2>Hola, {name}, esta es la página principal</h2>'

@app.route('/json')
def json():
    return jsonify({'key': 'value', 'listkey': [1,2,3]})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>{name}, estás en la página de query, desde {location}</h1>'

@app.route('/form')
def form():
    return '''<form method="POST" action="/process">
    <input type="text" name="name">
    <input type="text" name="location">
    <input type="submit" value="enviar">
    </form>'''

@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return f'<h2>Hola, {name}, eres de {location}, el formulario se envió exitosamente.</h2>'


if __name__ == '__main__':
    app.run()
