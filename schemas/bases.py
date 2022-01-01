from marshmallow import Schema, validate, fields


class BaseCategorySchema(Schema):
    category_name = fields.String(
        required=True, validate=validate.Length(min=1, max=100)
    )


class BaseProductSchema(Schema):
    product_code = fields.String(required=True, validate=validate.Length(min=1))
    product_name = fields.String(required=True, validate=validate.Length(min=1))
