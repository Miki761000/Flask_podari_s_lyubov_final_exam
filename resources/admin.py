from flask_restful import Resource
from werkzeug.exceptions import NotFound

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
        user_obj = UserModel.query.filter_by(id=id_)
        user = user_obj.first()
        if not user:
            raise NotFound("This user doesn't exist.")
        user_obj.update({"role": "admin"})
        db.session.commit()
        return {"role": "admin"}
