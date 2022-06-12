from marshmallow import Schema, fields, validate


class FileSchema(Schema):
    id = fields.String(dump_only=True)
    id_user = fields.String(dump_only=True)
    path = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
