from marshmallow import Schema, fields, validate
from main.schemas.token_schema import JWTSchema


class UserAvatarSchema(Schema):
    id_user = fields.Field(required=False, load_only=True)
    full_avatar_path = fields.String(dump_only=True)
    mini_avatar_path = fields.String(dump_only=True)
    name = fields.String(load_only=True)
    message = fields.String(dump_only=True)


class UserAdditionalInfo(Schema):
    id_user = fields.Field(required=False, load_only=True)
    is_fill = fields.Boolean(dump_only=True)
    phone_number = fields.String(required=True, validate=[
        validate.Regexp(r'^[0-9\-\+]{9,15}$', error="Please,enter valid phone number")
    ])
    first_name = fields.String(required=True, validate=[
        validate.Length(min=3, max=64, error="Please,enter name in the range 3 - 63 symbols")
    ])
    second_name = fields.String(required=True, validate=[
        validate.Length(min=3, max=64, error="Please,enter surname in the range 3 - 63 symbols")
    ])
    sex = fields.String(required=True, validate=[
        validate.OneOf(['female', 'male'])
    ])
    created_at = fields.DateTime(dump_only=False)
    updated_at = fields.DateTime(dump_only=False)
    message = fields.Field(dump_only=True)


class UserSchema(Schema):
    id = fields.Field(dump_only=True)
    username = fields.String(required=False, validate=[
        validate.Length(min=8, max=64, error="Please,enter username in the range 3 - 63 symbols")
    ])
    email = fields.String(required=False, validate=[
        validate.Length(max=64), validate.Email(error="Please,enter your real email")
    ])
    password = fields.String(required=True, validate=[
        validate.Length(min=8, max=64, error="Please,enter password in the range 3 - 64 symbols")
    ], load_only=True)
    balance = fields.Float(dump_only=True)
    verified = fields.Boolean(dump_only=True)
    additional_info = fields.Nested(UserAdditionalInfo, dump_only=True)
    avatar = fields.Nested(UserAvatarSchema, dump_only=True)
    message = fields.Field(dump_only=True)


class AuthSchema(Schema):
    data = fields.Nested(UserSchema, dump_only=True)
    jwt = fields.Nested(JWTSchema, dump_only=True)
    message = fields.Field(dump_only=True)



