from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.categories import CategoryManager
from schemas.request.categories import CategoryCreateRequestSchema
from schemas.response.categories import (
    CategoryResponseSchema,
    CategoryDetailedResponseSchema,
)
from utils.decorators import validate_schema


class CategoriesGetAllResource(Resource):
    def get(self):
        categories = CategoryManager.get_all_category()
        return CategoryResponseSchema().dump(categories, many=True)


class CategoriesDetailResource(Resource):
    @auth.login_required
    def get(self, id_):
        products = CategoryManager.get_one_category(id_)
        return CategoryDetailedResponseSchema().dump(products, many=True)


class CategoriesCreateResource(Resource):
    @auth.login_required
    @validate_schema(CategoryCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        data = request.get_json()
        category = CategoryManager.create(data, current_user.id)
        return CategoryResponseSchema().dump(category)


class CategoriesEditResource(Resource):
    @auth.login_required
    @validate_schema(CategoryCreateRequestSchema)
    def put(self, id_):
        data = request.get_json()
        updated_category = CategoryManager.update(data, id_)
        return CategoryResponseSchema().dump(updated_category)


class CategoriesDeleteResource(Resource):
    @auth.login_required
    def delete(self, id_):
        CategoryManager.delete(id_)
        return {"message": "You successfully delete item"}, 204
