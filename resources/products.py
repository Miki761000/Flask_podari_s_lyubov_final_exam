from flask import request, jsonify
from flask_restful import Resource

from managers.auth import auth
from managers.products import ProductManager
from schemas.request.products import (
    ProductCreateRequestSchema,
    ProductChangeQuantityRequestSchema, ProductEditRequestSchema,
)
from schemas.response.products import (
    ProductResponseSchema,
    ProductDetailedResponseSchema,
)
from utils.decorators import validate_schema
from utils.paginator import get_paginated_list


class ProductsGetAllResource(Resource):
    def get(self):
        products = ProductManager.get_all_products()
        return jsonify(
            get_paginated_list(
                ProductResponseSchema().dump(products, many=True),
                "/products",
                start=request.args.get("start", 1),
                limit=request.args.get("limit", 4),
            )
        )


class ProductsCreateResource(Resource):
    @auth.login_required
    @validate_schema(ProductCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        data = request.get_json()
        product = ProductManager.create(data, current_user.id)
        return ProductResponseSchema().dump(product)


class ProductsEditResource(Resource):
    @auth.login_required
    @validate_schema(ProductEditRequestSchema)
    def put(self, id_):
        data = request.get_json()
        updated_product = ProductManager.update(data, id_)
        return ProductResponseSchema().dump(updated_product)


class ProductsDetailResource(Resource):
    @auth.login_required
    def get(self, id_):
        product = ProductManager.get_one_product(id_)
        return ProductDetailedResponseSchema().dump(product)


class ProductsDeleteResource(Resource):
    @auth.login_required
    def delete(self, id_):
        ProductManager.delete(id_)
        return {"message": "You successfully delete item"}, 204


class AddDecreaseQuantity(Resource):
    @auth.login_required
    @validate_schema(ProductChangeQuantityRequestSchema)
    def put(self, id_):
        data = request.get_json()
        updated_product = ProductManager.update_quantity(data, id_)
        return ProductResponseSchema().dump(updated_product)
