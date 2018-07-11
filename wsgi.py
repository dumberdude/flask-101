# wsgi.py
from flask import Flask, jsonify, abort
app = Flask(__name__)

THE_PRODUCTS = [
    {'id': 1, 'name': 'Skello'},
    {'id': 2, 'name': 'Socialive.tv'},
    {'id': 3, 'name': 'foo.tv'},
    {'id': 4, 'name': 'bar.audio'},
    ]

@app.route('/')
def hello():
    return "Hello le wagon!"

@app.route('/api/v1/products')
def list_products():
    return jsonify(THE_PRODUCTS)

@app.route('/api/v1/products/<int:id>')
def get_a_product(id):
    id_to_return = [x for x in THE_PRODUCTS if x['id'] == id]
    return jsonify(id_to_return[0]) if id_to_return != [] else abort(404)
