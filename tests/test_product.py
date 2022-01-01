import json
import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import ProductModel
from services.s3 import S3Service
from tests.factories import UserFactory, CategoryFactory
from tests.helpers import encoded_photo, generate_token, mock_uuid, object_as_dict


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

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_photo", return_value="some-test.url")
    def test_create_product(self, s3_mock):
        """
        make request with login user's token and create product who:
        - exist in DB
        - OK response for created product
        - mock S3 bucket
        """
        url = "/products/create"
        user = UserFactory()
        category = CategoryFactory()
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

        extension = data.pop("image_extension")
        data.pop("product_image")
        created_product = object_as_dict(products[0])
        assert created_product == {
            "id": products[0].id,
            "product_description": products[0].product_description,
            "product_type_id": products[0].product_type_id,
            "user_id": user.id,
            "product_image": "some-test.url",
            **data
        }

        data.pop("product_description")
        data.pop("product_type_id")
        expected_response = {
            "product_image": "some-test.url",
            **data
        }

        actual_resp = resp.json
        assert resp.status_code == 201
        assert actual_resp == expected_response

        photo_name = f"{mock_uuid()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)
        s3_mock.assert_called_once_with(path, photo_name)

    def test_create_product_invalid_field_raises(self):
        url = "/products/create"
        user = UserFactory()
        category = CategoryFactory()
        data = {
            "product_code": "test",
            # "product_name": "Test",
            "product_quantity": 20,
            "product_delivery_price": 16,
            "product_description": "test test",
            "product_image": encoded_photo,
            "image_extension": "jpg",
            "product_type_id": 1,
        }
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})
        products = ProductModel.query.all()
        assert len(products) == 0

        # if data.__len__ != 8:
        #     resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 400
        assert resp.json == {}

        products = ProductModel.query.all()
        assert len(products) == 0
