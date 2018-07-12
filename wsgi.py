# wsgi.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass # Heroku does not use .env

from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
# models requires the 'db' object
from models import Product
# schemas requires the 'ma' object
from schemas import product_schema, products_schema

@app.route('/')
def hello():
    return "Hello le wagon!"

@app.route('/api/v1/products')
def list_products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/api/v1/products/<int:id>', methods=['GET'])
def get_a_product(id):
    product = db.session.query(Product).get(id)
    return product_schema.jsonify(product) if product else abort(404)

@app.route('/api/v1/products/<int:id>', methods=['DELETE'])
def del_a_product(id):
    product = db.session.query(Product).get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return make_response(("Product has been deleted!", 204))
    else:
        abort(404)

@app.route('/api/v1/products', methods=['POST'])
def create_a_product():
    if not request.is_json:
        return make_response(f"No JSON found", 400)
    product = Product()
    product.name = request.json['name']
    db.session.add(product)
    db.session.commit()
    return make_response(("Product has been added", 201))

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
    product = db.session.query(Product).get(id)
    if not product:
        return make_response(f"ID {id} not found", 400)
    product.name = request.json['name']
    db.session.commit()
    return make_response(get_a_product(id), 201)
