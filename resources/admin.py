from flask_restful import Resource

from db import db
from managers.auth import auth
from models import UserModel
from models.enums import UserRolesEnum
from utils.decorators import permission_required


class CreateAdmin(Resource):
    @staticmethod
    @auth.login_required
    @permission_required(UserRolesEnum.admin)
    def put(id_):
        UserModel.query.filter_by(id=id_).update({"role": UserRolesEnum.admin})
        db.session.commit()
        return {"role": "admin"}
