from marshmallow import Schema, fields, post_dump, post_load


class ArgsPagination(Schema):
    page = fields.Integer(load_only=True)
    limit = fields.Integer(load_only=True)

    @post_load
    def data(self, data, **kwargs):
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
        return data


class PaginationSchema(Schema):
    current_page = fields.Integer(dump_only=True)
    total_pages = fields.Integer(dump_only=True)
    total_entries = fields.Integer(dump_only=True)
    per_page = fields.Integer(dump_only=True)

    @post_dump
    def data(self, data, **kwargs):
        if 'current_page' in data:
            data['current_page'] = data['current_page'] + 1
        return data
