from marshmallow import Schema, fields
from .user_schema import UserSchema


class MemberSchema(Schema):
    rating = fields.Float(dump_only=True)
    user = fields.Nested(UserSchema(exclude=('balance',)), dump_only=True)
    followers = fields.Integer(dump_only=True)
    follows = fields.Integer(dump_only=True)
    count_reviews = fields.Integer(dump_only=True)
    message = fields.String(dump_only=True)
