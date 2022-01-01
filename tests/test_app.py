import json

from flask_testing import TestCase

from config import create_app
from db import db


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
            ("/category/create", "POST"),
            ("/category/edit/<int:id_>", "PUT"),
            ("/category/detail/2", "GET"),
            ("/category/delete/1", "DELETE"),
            ("/products/create", "POST"),
            ("/products/edit/3", "PUT"),
            ("/products/delete/18 ", "DELETE"),
            ("/products/detail/3", "GET"),
            ("/products/edit-quantity/3", "PUT"),
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
        pass
        # for method, url in [
        #     ("DELETE", "/category/delete/1"),
        #     ("DELETE", "/products/delete/1"),
        # ]:
        #     complainer = ComplainerFactory()
        #     token = generate_token(complainer)
        #     headers = {"Authorization": f"Bearer {token}"}
        #     if method == "POST":
        #         resp = self.client.post(url, data=json.dumps({}), headers=headers)
        #     elif method == "DELETE":
        #         resp = self.client.delete(url, headers=headers)
        #     expected_message = {'message': 'You do not have the rights to access this resource'}
        #     self.assert_403(resp, expected_message)
