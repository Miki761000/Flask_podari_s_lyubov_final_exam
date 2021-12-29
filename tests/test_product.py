import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import ProductModel
from tests.factories import UserFactory
from tests.helpers import encoded_photo, generate_token


class TestProduct(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestConfig")

    def test_create_product(self):
        url = "/products/create"
        user = UserFactory()
        data = {
                    "product_code": "test",
                    "product_name": "Test",
                    "product_quantity": 20,
                    "product_delivery_price": 16,
                    "product_description": "test test",
                    "product_image": encoded_photo,
                    "image_extension": "jpg",
                    "product_type_id": 1
                }
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        products = ProductModel.query.all()
        assert len(products) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        products = ProductModel.query.all()
        assert len(products) == 1

        expected_response = {

        }

        assert resp.status_code == 201
        assert resp.json == expected_response


