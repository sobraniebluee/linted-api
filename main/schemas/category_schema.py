from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id_category = fields.Integer(required=True)
    id_root = fields.Integer(required=True)
    is_root = fields.Boolean(required=True)
    title = fields.String(required=True)
    url = fields.Field()

