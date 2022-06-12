from marshmallow import Schema, fields


class SizeSchema(Schema):

    id = fields.Integer(dump_only=True)
    id_category = fields.Integer(required=True, load_only=True)
    title = fields.String(required=True)
    message = fields.String(dump_only=True)
