import json
import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import ProductModel
from services.s3 import S3Service
from tests.factories import UserFactory, CategoryFactory, AdminFactory
from tests.helpers import encoded_photo, generate_token, object_as_dict, mock_uuid


@patch("uuid.uuid4", mock_uuid)
@patch.object(S3Service, "upload_photo", return_value="some-test.url")
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

    def test_create_product(self, s3_mock):
        """
        make request with login user's token and create product who:
        - exist in DB
        - OK response for created product
        - mock S3 bucket
        """
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()
        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        products = ProductModel.query.all()
        assert len(products) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        products = ProductModel.query.all()
        assert len(products) == 1

        extension = data.pop("image_extension")
        data.pop("product_image")
        created_product = object_as_dict(products[0])
        assert created_product == {
            "id": products[0].id,
            "product_description": products[0].product_description,
            "product_type_id": products[0].product_type_id,
            "user_id": user.id,
            "product_image": "some-test.url",
            **data,
        }

        data.pop("product_description")
        data.pop("product_type_id")
        expected_response = {"product_image": "some-test.url", **data}

        actual_resp = resp.json
        assert resp.status_code == 201
        assert actual_resp == expected_response

        photo_name = f"{mock_uuid()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)
        s3_mock.assert_called_once_with(path, photo_name)

    def test_create_product_invalid_field_raises(self, s3_mock):
        """
        make request with login user's token and create product who:
        - invalid input fields
        - do not exist in DB
        - 400 response for created product
        """
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        products = ProductModel.query.all()
        assert len(products) == 0

        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(
                url, data=json.dumps(copy_data), headers=self.headers
            )

            assert resp.status_code == 400
            # assert resp.json == {'message': {key: ['Missing data for required field.']}}

        products = ProductModel.query.all()
        assert len(products) == 0

    def test_create_product_invalid_min_field_length(self, s3_mock):
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }
        products = ProductModel.query.all()
        assert len(products) == 0

        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(
                url, data=json.dumps(copy_data), headers=self.headers
            )
            assert resp.status_code == 400

        products = ProductModel.query.all()
        assert len(products) == 0

    def test_create_product_invalid_max_field_length(self, s3_mock):
        long_text = "x" * 150
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": long_text,
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }
        products = ProductModel.query.all()
        assert len(products) == 0

        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(
                url, data=json.dumps(copy_data), headers=self.headers
            )
            assert resp.status_code == 400

        products = ProductModel.query.all()
        assert len(products) == 0

    def test_edit_product(self, s3_mock):
        """
        make request with login user's token and edit product who:
        - exist in DB
        - OK response for edited product
        """
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        self.client.post(url, data=json.dumps(data), headers=self.headers)
        data.pop("image_extension")

        products = ProductModel.query.all()
        assert len(products) == 1

        url = f"/products/{products[-1].id}"

        product = {
            "product_code": "test",
            "product_name": "New Name",
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": products[-1].product_type_id,
        }

        resp = self.client.put(url, data=json.dumps(product), headers=self.headers)
        product["product_image"] = "test test"
        products = ProductModel.query.all()
        assert len(products) == 1

        expected_response = {
            "product_code": "test",
            "product_name": "New Name",
            "product_image": "some-test.url",
            "product_quantity": products[-1].product_quantity,
            "product_delivery_price": products[-1].product_delivery_price,
        }
        actual_resp = resp.json
        assert resp.status_code == 200
        assert actual_resp == expected_response

    def test_edit_product_invalid_field_raises(self, s3_mock):
        """
        make request with login user's token and edit product who:
        - exist in DB
        - 400 response for edited product
        """
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        self.client.post(url, data=json.dumps(data), headers=self.headers)
        data.pop("image_extension")

        products = ProductModel.query.all()
        assert len(products) == 1

        url = f"/products/{products[-1].id}"

        product = {
            # "product_code": "test",
            "product_name": "New Name",
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": products[-1].product_type_id,
        }

        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.put(
                url, data=json.dumps(copy_data), headers=self.headers
            )

            assert resp.status_code == 400

    def test_edit_product_quantity_increase(self, s3_mock):
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 14,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        self.client.post(url, data=json.dumps(data), headers=self.headers)
        data.pop("image_extension")

        products = ProductModel.query.all()
        assert len(products) == 1

        url = f"/products/edit-quantity/{products[-1].id}"

        product = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 10,
            "product_delivery_price": 10,
        }

        resp = self.client.put(url, data=json.dumps(product), headers=self.headers)
        products = ProductModel.query.all()
        assert len(products) == 1

        expected_response = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 30,
            "product_delivery_price": 12,
            "product_image": "some-test.url",
        }
        actual_resp = resp.json
        assert resp.status_code == 200
        assert actual_resp == expected_response

    def test_edit_product_quantity_decrease(self, s3_mock):
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 14,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        self.client.post(url, data=json.dumps(data), headers=self.headers)
        data.pop("image_extension")

        products = ProductModel.query.all()
        assert len(products) == 1

        url = f"/products/edit-quantity/{products[-1].id}"

        product = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": -10,
            "product_delivery_price": 14,
        }

        resp = self.client.put(url, data=json.dumps(product), headers=self.headers)
        products = ProductModel.query.all()
        assert len(products) == 1

        expected_response = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 10,
            "product_delivery_price": 14,
            "product_image": "some-test.url",
        }
        actual_resp = resp.json
        assert resp.status_code == 200
        assert actual_resp == expected_response

    def test_delete_product(self, s3_mock):
        url = "/products"
        user = AdminFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        self.client.post(url, data=json.dumps(data), headers=self.headers)
        data.pop("image_extension")

        products = ProductModel.query.all()
        assert len(products) == 1

        url = f"/products/{products[-1].id}"

        self.client.delete(url, headers=self.headers).status_code == 204
        products = ProductModel.query.all()

        assert len(products) == 0

    def test_delete_product_user_raises(self, s3_mock):
        url = "/products"
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        category = CategoryFactory()

        data = {
            "product_code": "test",
            "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": category.id,
        }

        self.client.post(url, data=json.dumps(data), headers=self.headers)
        data.pop("image_extension")

        products = ProductModel.query.all()
        assert len(products) == 1

        url = f"/products/{products[-1].id}"

        self.client.delete(url, headers=self.headers).status_code == 404
        products = ProductModel.query.all()

        assert len(products) == 1
