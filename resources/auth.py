from flask import request
from flask_cors import cross_origin
from flask_restful import Resource

from managers.auth import AuthManager
from managers.users import UserManager
from schemas.request.users import RequestLoginUserSchema
from utils.decorators import validate_schema


class Register(Resource):
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201


class Login(Resource):
    @validate_schema(RequestLoginUserSchema)
    @cross_origin()
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token, "role": "user"}
