# wsgi.py
from flask import Flask, jsonify, abort, make_response
app = Flask(__name__)

THE_PRODUCTS = [
    {'id': 1, 'name': 'Skello'},
    {'id': 2, 'name': 'Socialive.tv'},
    {'id': 3, 'name': 'foo.tv'},
    {'id': 4, 'name': 'bar.audio'},
    {'id': 5, 'name': 'foobar'},
    ]

@app.route('/')
def hello():
    return "Hello le wagon!"

@app.route('/api/v1/products')
def list_products():
    return jsonify(THE_PRODUCTS)

@app.route('/api/v1/products/<int:id>', methods=['GET'])
def get_a_product(id):
    id_to_return = [x for x in THE_PRODUCTS if x['id'] == id]
    return jsonify(id_to_return[0]) if id_to_return != [] else abort(404)

@app.route('/api/v1/products/<int:id>', methods=['DELETE'])
def del_a_product(id):
    global THE_PRODUCTS
    if not get_a_product(id).status_code == 200:
        abort(404)
    THE_PRODUCTS = [x for x in THE_PRODUCTS if x['id'] != id]
    return make_response(("Product has been deleted!", 204))
