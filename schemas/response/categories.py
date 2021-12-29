from marshmallow import fields

from schemas.bases import BaseCategorySchema


class CategoryResponseSchema(BaseCategorySchema):
    id = fields.Integer(required=True)


class CategoryDetailedResponseSchema(BaseCategorySchema):
    id = fields.Integer(required=True)
    product_code = fields.String(required=True)
    product_name = fields.String(required=True)
    product_quantity = fields.Integer(required=True)
    product_delivery_price = fields.Float(required=True)
    product_description = fields.String(required=True)
    product_image = fields.String(required=True)
    product_type_id = fields.Integer(required=True)
    category_name = fields.String(required=True)
