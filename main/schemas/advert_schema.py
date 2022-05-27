from marshmallow import Schema, fields, validate


class AdvertAddSchema(Schema):
    title = fields.String(required=True, validate=[
        validate.Length(min=5, max=64, error="Please,enter title in range 5 to 64 chars!")])
    description = fields.String(required=True, validate=[
        validate.Length(min=5, max=250, error="Please,enter title in range 5 to 64 chars!")])
    condition = fields.Integer(required=True, validate=[
        validate.OneOf([100, 200, 300, 400, 500], error="Please,send valid data!")
    ])
    price = fields.Float(required=True, validate=[validate.Range(min=0, max=100000, error="Price must be less than 100000 !")])
    category = fields.Integer(required=True)