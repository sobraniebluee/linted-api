from marshmallow import Schema, fields, post_load, pre_load
from .user_schema import UserSchema
from main.schemas.pagination_schema import PaginationSchema, ArgsPagination


class MemberSchema(Schema):
    rating = fields.Float(dump_only=True)
    user = fields.Nested(UserSchema(exclude=('balance',)), dump_only=True)
    followers = fields.Integer(dump_only=True)
    follows = fields.Integer(dump_only=True)
    count_reviews = fields.Integer(dump_only=True)
    message = fields.String(dump_only=True)


class QueryMemberSchema(ArgsPagination):
    search_text = fields.String()
    page = fields.Field()

    @post_load
    def load_data(self, data, **kwargs):
        if 'search_text' not in data:
            data['search_text'] = ''
        return data


class ResponseSearchMembersSchema(Schema):
    items = fields.Nested(UserSchema(only=('id', 'username', 'avatar'), many=True), dump_only=True)
    message = fields.String(dump_only=True)
    pagination = fields.Nested(PaginationSchema, dump_only=True)


class AllMemberSubs(Schema):
    items = fields.Nested(UserSchema(only=('username', 'id', 'avatar'), many=True), dump_only=True)
    pagination = fields.Nested(PaginationSchema, dump_only=True)
    message = fields.String(dump_only=True)
