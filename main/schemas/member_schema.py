from marshmallow import Schema, fields, post_load, pre_load
from .user_schema import UserSchema


class MemberSchema(Schema):
    rating = fields.Float(dump_only=True)
    user = fields.Nested(UserSchema(exclude=('balance',)), dump_only=True)
    followers = fields.Integer(dump_only=True)
    follows = fields.Integer(dump_only=True)
    count_reviews = fields.Integer(dump_only=True)
    message = fields.String(dump_only=True)


class QueryMemberSchema(Schema):
    search_text = fields.String()
    page = fields.Field()

    @post_load
    def load_data(self, data, **kwargs):
        if 'page' in data:
            try:
                data['page'] = int(data['page'])
            except Exception:
                data['page'] = 0
            if data['page'] < 1:
                data['page'] = 1
            if data['page']:
                data['page'] = data['page'] - 1
        else:
            data['page'] = 0
        if 'search_text' not in data:
            data['search_text'] = ''
        return data


class SearchPagination(Schema):
    current_page = fields.Integer(dump_only=True)
    total_pages = fields.Integer(dump_only=True)
    total_entries = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)


class ResponseSearchMembersSchema(Schema):
    users = fields.Nested(UserSchema(only=('id', 'username', 'avatar'), many=True), dump_only=True)
    message = fields.String(dump_only=True)
    pagination = fields.Nested(SearchPagination, dump_only=True)
