from sqlalchemy import func

from db import db
from models.enums import UserRolesEnum


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class UserModel(BaseUserModel):
    __tablename__ = "users"

    role = db.Column(db.Enum(UserRolesEnum), default=UserRolesEnum.user)
    create_on = db.Column(db.DateTime, server_default=func.now())
