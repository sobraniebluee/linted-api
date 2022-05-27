from marshmallow import Schema, fields


class JWTSchema(Schema):
    access_token = fields.String(dump_only=True)
    refresh_token = fields.String(dump_only=True)
    message = fields.Field(dump_only=True)
