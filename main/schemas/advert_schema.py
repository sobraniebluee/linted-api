from marshmallow import Schema, fields, validate, post_load, post_dump
from main.schemas.size_schema import SizeSchema
from main.schemas.category_schema import CategorySchema
from main.schemas.user_schema import UserSchema
from main.schemas.file_schema import FileSchema
from config import Const
from main.schemas.pagination_schema import PaginationSchema, ArgsPagination


class AdvertWatches(Schema):
    id = fields.Integer()
    id_user = fields.String()
    id_advert = fields.String()
    ip_user = fields.String()
    created_at = fields.String()


class AdvertLikesSchema(Schema):
    id = fields.Integer()
    id_user = fields.String()
    id_advert = fields.String()
    created_at = fields.String()


class AdvertImageSchema(Schema):
    is_preview = fields.Boolean(dump_only=True)
    image = fields.Nested(FileSchema(only=('id', 'path',)))


class AdvertConditionSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)
    description = fields.String(dump_only=True)


class AdvertInfoSchema(Schema):
    title = fields.String(dump_only=True)
    description = fields.String(dump_only=True)
    price = fields.Float(dump_only=True)
    condition = fields.Nested(AdvertConditionSchema(only=('title',)))
    size = fields.Nested(SizeSchema(only=('title',)))
    category = fields.Nested(CategorySchema(only=('id_category', 'title',)))


class AdvertSchema(Schema):
    id = fields.String(dump_only=True)
    rating = fields.Integer(dump_only=True)
    is_ban = fields.Boolean(dump_only=True)
    is_bought = fields.Boolean(dump_only=True)
    url = fields.String(dump_only=True)
    created_at = fields.Field(dump_only=True)
    info = fields.Nested(AdvertInfoSchema)
    images = fields.Nested(AdvertImageSchema(many=True))
    user = fields.Nested(UserSchema(only=('username', 'avatar', 'id')))
    likes = fields.Nested(AdvertLikesSchema(only=('id', 'id_user'), many=True), dump_only=True)
    watches = fields.Nested(AdvertWatches(only=('id',), many=True), dump_only=True)
    message = fields.String(dump_only=True)
    is_liked = fields.Boolean(dump_only=True)

    @post_dump
    def dump_data(self, data, **kwargs):
        if 'message' not in data:
            data['likes'] = int(len(data['likes']))
            data['watches'] = int(len(data['watches']))
            return data
        else:
            return data


class ArgsAdvertsSchema(ArgsPagination):
    categories_id = fields.List(fields.Field(), load_only=True)
    search_text = fields.String(load_only=True)
    sizes_id = fields.List(fields.Field(), load_only=True)
    sort = fields.String(load_only=True, validate=[validate.OneOf(['asc', 'desc', 'newest'])])
    price_from = fields.Float(load_only=True)
    price_to = fields.Float(load_only=True)
    conditions_id = fields.List(fields.Field(), load_only=True)
    page = fields.Field(load_only=True)
    limit = fields.Field(load_only=True)

    @post_load
    def parse_data(self, data, **kwargs):
        if 'categories_id' in data:
            data['categories_id'] = self.parse_to_list(data['categories_id'])
        if 'sizes_id' in data:
            data['sizes_id'] = self.parse_to_list(data['sizes_id'])
        if 'conditions_id' in data:
            data['conditions_id'] = self.parse_to_list(data['conditions_id'])
        return data

    @staticmethod
    def parse_to_list(params):
        try:
            parsed_list = list(map(lambda x: int(x), str(params[0]).split(',')))
        except ValueError:
            parsed_list = []
        return parsed_list


class AllAdvertsSchema(Schema):
    items = fields.Nested(AdvertSchema(many=True), dump_only=True)
    pagination = fields.Nested(PaginationSchema, dump_only=True)
    message = fields.String(dump_only=True)


class AdvertAddSchema(Schema):
    title = fields.String(required=True, validate=[
        validate.Length(min=4, max=64, error="Please,enter title in range 5 to 64 chars!")])
    description = fields.String(required=True, validate=[
        validate.Length(min=4, max=250, error="Please,enter title in range 5 to 64 chars!")])
    condition_id = fields.Integer(required=True, validate=[
        validate.OneOf([100, 200, 300, 400, 500], error="Please,enter valid condition!")
    ])
    price = fields.Float(required=True, validate=[validate.Range(min=0, max=100000, error="Price must be less than 100000 !")])
    category_id = fields.Integer(required=True)
    size_id = fields.Integer()
    images = fields.List(fields.String(required=True), validate=[
        validate.Length(max=Const.MAX_COUNT_FILES_FOR_ADVERT,
                        error="Max number of images is 20"),
        validate.Length(min=1, error="Please set one image!")
    ])


class AdvertEditSchema(Schema):
    title = fields.String(validate=[
        validate.Length(min=4, max=64, error="Please,enter title in range 5 to 64 chars!")])
    description = fields.String(validate=[
        validate.Length(min=4, max=250, error="Please,enter title in range 5 to 64 chars!")])
    condition_id = fields.Integer(validate=[
        validate.OneOf([100, 200, 300, 400, 500], error="Please,send valid data!")
    ])
    price = fields.Float(validate=[validate.Range(min=0, max=100000, error="Price must be less than 100000 !")])
    category_id = fields.Integer()
    size_id = fields.Integer()
    images = fields.List(fields.String(required=True), validate=[
        validate.Length(max=Const.MAX_COUNT_FILES_FOR_ADVERT,
                        error="Max number of images is 20"),
        validate.Length(min=1, error="Please set one image!")
    ])

