import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import CategoryModel
from tests.factories import UserFactory, CategoryFactory, AdminFactory
from tests.helpers import generate_token


class TestCategory(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestConfig")

    def test_create_category(self):
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

        expected_response = {"category_name": "test", "id": categories[0].id}
        actual_resp = resp.json
        assert resp.status_code == 201
        assert actual_resp == expected_response

    def test_create_category_invalid_field_raises(self):
        url = "/category/create"
        user = UserFactory()
        data = {
            # "category_name": "",
        }
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        categories = CategoryModel.query.all()
        assert len(categories) == 0

        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

            assert resp.status_code == 400
            assert resp.json == {"message": {key: ["Missing data for required field."]}}

        categories = CategoryModel.query.all()
        assert len(categories) == 0

    def test_create_category_invalid_field_length(self):
        long_text = "x" * 150
        url = "/category/create"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        data = {"category_name": long_text}
        categories = CategoryModel.query.all()
        assert len(categories) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 400
        assert resp.json == {
            "message": "Invalid fields {'category_name': ['Length must be between 1 and "
            "100.']}"
        }

        categories = CategoryModel.query.all()
        assert len(categories) == 0

    def test_edit_category(self):
        """
        make request with login user's token and create category who:
        - exist in DB
        - OK response for edited category
        """
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()
        categories = CategoryModel.query.all()
        assert len(categories) == 1
        data = CategoryModel.query.filter_by(id=category.id)
        url = f"/category/edit/{category.id}"

        data = {
            "category_name": "test",
        }

        resp = self.client.put(url, data=json.dumps(data), headers=self.headers)
        categories = CategoryModel.query.all()
        assert len(categories) == 1

        expected_response = {
            "category_name": "test",
            "id": category.id,
        }
        actual_resp = resp.json
        assert resp.status_code == 200
        assert actual_resp == expected_response

    def test_edit_category_raises(self):
        """
        make request with login user's token and create category who:
        - exist in DB
        - raises error response for edited product
        """
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()
        categories = CategoryModel.query.all()
        assert len(categories) == 1
        data = CategoryModel.query.filter_by(id=category.id)
        url = f"/category/edit/{category.id}"

        data = {
            # "category_name": "test",
        }

        resp = self.client.put(url, data=json.dumps(data), headers=self.headers)
        categories = CategoryModel.query.all()
        assert len(categories) == 1

        expected_response = {
            "category_name": "test",
            "id": category.id,
        }
        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
            assert resp.status_code == 400
            assert resp.json == {"message": {key: ["Missing data for required field."]}}

    def test_delete_category(self):
        user = AdminFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()
        categories = CategoryModel.query.all()
        assert len(categories) == 1
        data = CategoryModel.query.filter_by(id=category.id)
        url = f"/category/delete/{category.id}"

        self.client.delete(url, headers=self.headers).status_code == 204

        categories = CategoryModel.query.all()
        assert len(categories) == 0

    def test_delete_category_user_raises(self):
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()
        categories = CategoryModel.query.all()
        assert len(categories) == 1
        data = CategoryModel.query.filter_by(id=category.id)
        url = f"/category/delete/{category.id}"
        self.client.delete(url, headers=self.headers).status_code == 404

        categories = CategoryModel.query.all()
        assert len(categories) == 1

