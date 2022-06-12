from marshmallow import Schema, fields, validate
from main.schemas.size_schema import SizeSchema
from main.schemas.category_schema import CategorySchema
from main.schemas.user_schema import UserSchema
from main.schemas.file_schema import FileSchema
from config import Config


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
    watches = fields.Integer(dump_only=True)
    likes = fields.Integer(dump_only=True)
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
    message = fields.String(dump_only=True)
    likes = fields.Method('count_likes', dump_only=True)
    watches = fields.Method('count_watches', dump_only=True)

    def count_likes(self, obj):
        return int(len(obj.likes))

    def count_watches(self, obj):
        return int(len(obj.watches))

class AdvertAddSchema(Schema):
    title = fields.String(required=True, validate=[
        validate.Length(min=4, max=64, error="Please,enter title in range 5 to 64 chars!")])
    description = fields.String(required=True, validate=[
        validate.Length(min=4, max=250, error="Please,enter title in range 5 to 64 chars!")])
    condition_id = fields.Integer(required=True, validate=[
        validate.OneOf([100, 200, 300, 400, 500], error="Please,send valid data!")
    ])
    price = fields.Float(required=True, validate=[validate.Range(min=0, max=100000, error="Price must be less than 100000 !")])
    category_id = fields.Integer(required=True)
    size_id = fields.Integer()
    images = fields.List(fields.String(required=True), validate=[
        validate.Length(max=Config.MAX_COUNT_FILES_FOR_ADVERT,
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
        validate.Length(max=Config.MAX_COUNT_FILES_FOR_ADVERT,
                        error="Max number of images is 20"),
        validate.Length(min=1, error="Please set one image!")
    ])

