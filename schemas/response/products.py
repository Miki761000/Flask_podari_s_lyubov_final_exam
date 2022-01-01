from marshmallow import fields

from schemas.bases import BaseProductSchema


class ProductResponseSchema(BaseProductSchema):
    product_quantity = fields.Integer(required=True)
    product_delivery_price = fields.Integer(required=True)
    product_image = fields.String(required=True)
    category_name = fields.String(required=True)


class ProductDetailedResponseSchema(BaseProductSchema):
    id = fields.Integer(required=True)
    product_quantity = fields.Integer(required=True)
    product_delivery_price = fields.Integer(required=True)
    product_description = fields.String(required=True)
    product_image = fields.String(required=True)
    product_type_id = fields.Integer(required=True)
    category_name = fields.String(required=True)
