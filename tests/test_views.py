# tests/test_views.py
from flask_testing import TestCase
from wsgi import app
import json

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_products_json(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 3) # 3 is not a mistake here.

    def test_get_a_product(self):
        response = self.client.get("/api/v1/products/2")
        self.assertEqual(response.status_code, 200)
        the_product = response.json
        self.assertEqual(len(the_product), 2)
        self.assertEqual(the_product['id'], 2)
        self.assertIsInstance(the_product['name'], str)
        response = self.client.get("/api/v1/products/-1")
        self.assertEqual(response.status_code, 404)

    def test_delete_a_product(self):
        response = self.client.delete("/api/v1/products/1")
        self.assertEqual(response.status_code, 204)
        response = self.client.delete("/api/v1/products/-1")
        self.assertEqual(response.status_code, 404)

    def test_create_a_product(self):
        data = json.dumps({'name': 'TEST'})
        response = self.client.post("/api/v1/products",
                                    headers={'content-type':
                                             'application/json'},
                                    data=data)
        self.assertEqual(response.status_code, 201)

    def test_update_a_product(self):
        for d in [{'name': ''}, {'test': 'a test'}, '']:
            print(f'd = {d}')
            bad_req = \
                self.client.patch("/api/v1/products/2",
                                  headers={'content-type':
                                           'application/json'},
                                  data=json.dumps(d))
            self.assertEqual(bad_req.status_code, 422)
        name_before = \
            self.client.get("/api/v1/products/2").json['name']
        response = \
            self.client.patch("/api/v1/products/2",
                              headers={'content-type':
                                       'application/json'},
                              data=json.dumps({'name': 'NewTEST'}))
        self.assertEqual(response.status_code, 201)
        name_after = \
            self.client.get("/api/v1/products/2").json['name']
        self.assertEqual(response.status_code, 201)

