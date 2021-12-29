import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import UserModel, UserRolesEnum
from tests.helpers import object_as_dict


class TestAuth(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestConfig")

    def test_register_user(self):
        """
        - test if user is in db
        - check if role is correct
        """
        url = "/register"
        data = {
                    "email": "a@a.com",
                    "password": "test123",
                    "full_name": "test test",
                    "phone": "0123456789"
                }

        users = UserModel.query.all()
        assert len(users) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)
        assert resp.status_code == 201
        assert "token" in resp.json

        users = UserModel.query.all()
        assert len(users) == 1
        user = object_as_dict(users[0])
        user.pop("password")
        data.pop("password")
        user.pop("create_on")

        assert user == {
            "id": user["id"],
            "role": UserRolesEnum.user,
            **data,
        }
