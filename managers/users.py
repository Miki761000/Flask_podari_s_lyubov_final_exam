from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models.users import UserModel


class UserManager:
    @staticmethod
    def register(data):
        data["password"] = generate_password_hash(data["password"], method="sha256")
        user = UserModel(**data)
        try:
            db.session.add(user)
            db.session.flush()
            return AuthManager.encode_token(user)
        except Exception as ex:
            if ex.orig.pgcode == UNIQUE_VIOLATION:
                raise BadRequest("Please, Login")
            else:
                raise InternalServerError(
                    "Server is unavailable. Please, try again later."
                )

    @staticmethod
    def login(data):
        try:
            user_data = UserModel.query.filter_by(email=data["email"]).first()
            if user_data and check_password_hash(user_data.password, data["password"]):
                return AuthManager.encode_token(user_data), user_data.id
            raise Exception
        except Exception:
            raise BadRequest("Invalid username or password")
