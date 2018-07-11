# wsgi.py
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello le wagon!"

@app.route('/api/v1/products')
def list_products():
    the_products = [
        { 'id': 1, 'name': 'Skello' },
        { 'id': 2, 'name': 'Socialive.tv' },
        { 'id': 3, 'name': 'foo.tv' },
        { 'id': 4, 'name': 'bar.audio' },
        ]
    return jsonify(the_products)

