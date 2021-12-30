from random import randint

import factory
from sqlalchemy import func

from db import db
from models import UserRolesEnum, UserModel, CategoryModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class UserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n + 1)
    full_name = factory.Faker("name")
    email = factory.Faker("email")
    phone = str(randint(100000000, 900000000))
    password = factory.Faker("password")
    role = UserRolesEnum.user
    create_on = func.now()


class CategoryFactory(BaseFactory):
    class Meta:
        model = CategoryModel

    id = factory.Sequence(lambda n: n + 1)
    category_name = factory.Faker("name")

