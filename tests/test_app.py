import json

from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import UserFactory
from tests.helpers import generate_token


class TestApplication(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        return create_app("config.TestConfig")

    def test_authentication_missing_token_raise(self):
        url_method = [
            ("/category/", "POST"),
            ("/category/1", "PUT"),
            ("/category/1", "GET"),
            ("/category/1", "DELETE"),
            ("/products/", "POST"),
            ("/products/13", "PUT"),
            ("/products/13 ", "DELETE"),
            ("/products/12", "GET"),
            ("/products/edit-quantity/12", "PUT"),
        ]

        for url, method in url_method:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            else:
                resp = self.client.delete(url)

        assert resp.status_code == 401
        assert resp.json == {"message": "Invalid token"}

    def test_permission_required_admin_rights_raise(self):
        for method, url in [
            ("DELETE", "/category/5"),
            ("DELETE", "/products/12"),
        ]:
            complainer = UserFactory()
            token = generate_token(complainer)
            headers = {"Authorization": f"Bearer {token}"}

            resp = self.client.delete(url, headers=headers)
            expected_message = {
                "message": "You do not have the rights to access this resource"
            }
            assert resp.status_code == 403
            assert resp.json == expected_message
