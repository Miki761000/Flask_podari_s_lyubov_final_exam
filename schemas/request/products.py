from marshmallow import fields, validate

from schemas.bases import BaseProductSchema


class ProductCreateRequestSchema(BaseProductSchema):
    product_quantity = fields.Integer(required=True)
    product_delivery_price = fields.Integer(required=True)
    product_description = fields.String(required=True, validate=validate.Length(min=1))
    product_image = fields.String(required=True, validate=validate.Length(min=1))
    image_extension = fields.String(required=True, validate=validate.Length(min=1))
    product_type_id = fields.Integer(required=True, validate=validate.Length(min=1))


class ProductEditRequestSchema(BaseProductSchema):
    product_description = fields.String(required=True, validate=validate.Length(min=1))
    product_image = fields.String(required=True, validate=validate.Length(min=1))
    image_extension = fields.String(required=True, validate=validate.Length(min=1))
    product_type_id = fields.Integer(required=True, validate=validate.Length(min=1))


class ProductChangeQuantityRequestSchema(BaseProductSchema):
    pass
