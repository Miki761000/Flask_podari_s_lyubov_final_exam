from werkzeug.exceptions import NotFound

from db import db
from managers.auth import auth
from models import ProductModel, UserRolesEnum, CategoryModel
from services.s3 import S3Service
from utils.calculations import calculate_quantity_and_price
from utils.decorators import permission_required, positive_number
from utils.photo_upload import photo_upload

s3 = S3Service()


class ProductManager:
    @staticmethod
    def get_all_products():
        products = (
            ProductModel.query.join(CategoryModel)
            .add_columns(
                ProductModel.product_code,
                ProductModel.product_name,
                ProductModel.product_quantity,
                ProductModel.product_image,
                ProductModel.product_type_id,
                CategoryModel.category_name,
            )
            .filter(ProductModel.product_type_id == CategoryModel.id)
            .order_by(ProductModel.product_code)
        )

        return products

    @staticmethod
    @auth.login_required
    def get_one_product(id_):
        product = (
            ProductModel.query.filter_by(id=id_)
            .join(CategoryModel)
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
            .first()
        )
        return product

    @staticmethod
    @auth.login_required
    def create(data, user_id):
        data = photo_upload(data)

        positive_number(data["product_quantity"])
        positive_number(data["product_delivery_price"])
        data["user_id"] = user_id
        product = ProductModel(**data)
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    @auth.login_required
    def update(data, id_):
        data = photo_upload(data)

        product_obj = ProductModel.query.filter_by(id=id_)
        product = product_obj.first()
        if not product:
            raise NotFound("This product doesn't exist.")

        product_obj.update(data)
        db.session.commit()
        return product

    @staticmethod
    @auth.login_required
    def update_quantity(data, id_):
        product_obj = ProductModel.query.filter_by(id=id_)
        product = product_obj.first()
        if not product:
            raise NotFound("This product doesn't exist.")

        calculate_quantity_and_price(data, product)
        product_obj.update(data)
        db.session.commit()
        return product

    @staticmethod
    @auth.login_required
    @permission_required(UserRolesEnum.admin)
    def delete(id_):
        product_obj = ProductModel.query.filter_by(id=id_)
        product = product_obj.first()
        if not product:
            raise NotFound("This product doesn't exist.")

        db.session.delete(product)
        db.session.commit()

