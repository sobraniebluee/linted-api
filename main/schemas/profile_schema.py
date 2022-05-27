from marshmallow import Schema, fields, validate


class ProfileSchema(Schema):
    username = fields.String(required=False, validate=[
        validate.Length(min=8, max=64, error="Please,enter username in the range 3 - 63 symbols")
    ])
    email = fields.String(required=False, validate=[
        validate.Length(max=64), validate.Email(error="Please,enter your real email")
    ])
    phone_number = fields.String(required=False, validate=[
        validate.Regexp(r'^[0-9\-\+]{9,15}$', error="Please,enter valid phone number")
    ])
    first_name = fields.String(required=False, validate=[
        validate.Length(min=3, max=64, error="Please,enter name in the range 3 - 63 symbols")
    ])
    second_name = fields.String(required=False, validate=[
        validate.Length(min=3, max=64, error="Please,enter surname in the range 3 - 63 symbols")
    ])
    sex = fields.String(required=False, validate=[
        validate.Length(min=3, error="Please,enter valid data!")
    ])