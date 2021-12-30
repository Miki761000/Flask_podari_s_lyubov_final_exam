import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import CategoryModel
from tests.factories import UserFactory
from tests.helpers import generate_token


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
        """
        make request with login user's token and create category who:
        - exist in DB
        - OK response for created product
        """
        url = "/category/create"
        user = UserFactory()
        data = {
                    "category_name": "test",
                }
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        categories = CategoryModel.query.all()
        assert len(categories) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        categories = CategoryModel.query.all()
        assert len(categories) == 1

        expected_response = {
            'category_name': 'test',
            'id': categories[0].id
        }
        actual_resp = resp.json
        assert resp.status_code == 201
        assert actual_resp == expected_response


