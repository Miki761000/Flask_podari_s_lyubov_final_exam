from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import Unauthorized

# This should be here. Auth doesnt work without this
from models.users import UserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=20000),
            "type": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("JWT_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config("JWT_KEY"), algorithms=["HS256"])
            return info["sub"], info["type"]
        except Exception as ex:
            raise ex


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        user_id, type_user = AuthManager.decode_token(token)
        return eval(f"{type_user}.query.filter_by(id={user_id}).first()")
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
