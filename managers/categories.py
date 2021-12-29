from werkzeug.exceptions import NotFound

from db import db
from managers.auth import auth
from models import UserRolesEnum, ProductModel
from models.categories import CategoryModel
from utils.decorators import permission_required


class CategoryManager:
    @staticmethod
    def get_all_category():
        return CategoryModel.query.all()

    @staticmethod
    @auth.login_required
    def create(data, user_id):
        data["user_id"] = user_id
        category = CategoryModel(**data)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    @auth.login_required
    def update(data, id_):
        category_obj = CategoryModel.query.filter_by(id=id_)
        category = category_obj.first()
        if not category:
            raise NotFound("This category doesn't exist.")

        category_obj.update(data)
        db.session.commit()
        return category

    @staticmethod
    @auth.login_required
    @permission_required(UserRolesEnum.admin)
    def delete(id_):
        category_obj = CategoryModel.query.filter_by(id=id_)
        category = category_obj.first()
        if not category:
            raise NotFound("This category doesn't exist.")

        db.session.delete(category)
        db.session.commit()

    @staticmethod
    @auth.login_required
    def get_one_category(id_):
        products = (
            ProductModel.query.join(CategoryModel)
            .add_columns(
                ProductModel.id,
                ProductModel.product_code,
                ProductModel.product_name,
                ProductModel.product_quantity,
                ProductModel.product_image,
                ProductModel.product_delivery_price,
                ProductModel.product_description,
                ProductModel.product_type_id,
                CategoryModel.category_name,
            )
            .filter(ProductModel.product_type_id == CategoryModel.id)
            .filter_by(id=id_)
            .all()
        )
        return products
