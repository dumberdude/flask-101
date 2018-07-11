# tests/test_views.py
from flask_testing import TestCase
from wsgi import app

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
