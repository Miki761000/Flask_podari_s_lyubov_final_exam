from marshmallow import fields, validate

from schemas.bases import BaseProductSchema


class ProductCreateRequestSchema(BaseProductSchema):
    product_quantity = fields.Integer(required=True)
    product_delivery_price = fields.Integer(required=True)
    product_description = fields.String(required=True, validate=validate.Length(min=1))
    product_image = fields.String(required=True)
    image_extension = fields.String(required=True)
    product_type_id = fields.Integer(required=True)


class ProductEditRequestSchema(BaseProductSchema):
    product_description = fields.String(required=True, validate=validate.Length(min=1))
    product_image = fields.String(required=True)
    image_extension = fields.String(required=True)
    product_type_id = fields.Integer(required=True)


class ProductChangeQuantityRequestSchema(BaseProductSchema):
    product_quantity = fields.Integer(required=True)
    product_delivery_price = fields.Integer(required=True)
