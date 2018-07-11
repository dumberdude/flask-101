# wsgi.py
from flask import Flask, jsonify, abort, make_response, request
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

@app.route('/api/v1/products', methods=['POST'])
def create_a_product():
    if not request.is_json:
        return make_response(f"No JSON found", 400)
    THE_PRODUCTS.append(
        {
            'id': len(THE_PRODUCTS) + 1,
            'name': request.json['name'],
        })
    return make_response(jsonify({'id': len(THE_PRODUCTS)}), 201)

@app.route('/api/v1/products/<int:id>', methods=['PATCH'])
def update_a_product(id):
    if not request.is_json:
        return make_response(f"Content-Type not application/json", 422)
    if isinstance(request.json, str):
        return make_response(f"No JSON found", 422)
    if not request.json.get("name"):
        return make_response(f"No 'name' entry found in the JSON", 422)
    elif request.json['name'] == "":
        return make_response(f"The 'name' entry must not be empty", 422)
    if not get_a_product(id).json['id'] == id:
        return make_response(f"ID {id} not found", 400)
    for product in [x for x in THE_PRODUCTS if x['id'] == id]:
        product['name'] = request.json['name']
        break
    return make_response(get_a_product(id), 201)
