from marshmallow import Schema, fields, validate


class UsersSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=False, validate=[
        validate.Length(min=3, max=64)
    ])
    email = fields.String(required=False, validate=[
        validate.Length(max=64), validate.Email(error="Please,fill the try email")
    ])
    password = fields.String(required=True, validate=[
        validate.Length(min=8, max=64)
    ], load_only=True)
    created_at = fields.String(dump_only=True)
    message = fields.Field(dump_only=True)


class AuthSchema(Schema):
    data = fields.Nested(UsersSchema, dump_only=True)
    access_token = fields.String(dump_only=True)
    message = fields.Field(dump_only=True)

