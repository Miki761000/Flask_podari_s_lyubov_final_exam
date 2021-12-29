from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models.users import UserModel


class UserManager:
    @staticmethod
    def register(data):
        """
        Hashes the plain password
        :param comx lainer_data: dict
        :return: complainer
        """
        data["password"] = generate_password_hash(data["password"], method="sha256")
        user = UserModel(**data)
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as ex:
            if ex.orig.pgcode == UNIQUE_VIOLATION:
                raise BadRequest("Please, Login")
            else:
                InternalServerError("Server is unavailable.Please, try again later.")

    @staticmethod
    def login(data):
        """
        Checks the email and password (hashes the plain password)
        :param data: dict -> email, password
        :return: token
        """
        try:
            user_data = UserModel.query.filter_by(email=data["email"]).first()
            if user_data and check_password_hash(user_data.password, data["password"]):
                return AuthManager.encode_token(user_data), user_data.id
            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")
