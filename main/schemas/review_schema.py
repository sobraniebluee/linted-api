from marshmallow import Schema, fields, validate
from config import Const
from .pagination_schema import PaginationSchema


class MemberReviewSchema(Schema):
    id = fields.Integer(dump_only=True)
    id_advert = fields.String(required=True)
    rating = fields.Integer(required=True, validate=[validate.OneOf([1, 2, 3, 4, 5])])
    description = fields.String(validate=[validate.Length(min=3,
                                                         max=Const.MAX_LENGTH_REVIEW,
                                                         error=f"Please,enter text which contains length in range 3-{Const.MAX_LENGTH_REVIEW}")])
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    message = fields.String(dump_only=True)


class AllMemberReviewsSchema(Schema):
    items = fields.Nested(MemberReviewSchema(many=True), dump_only=True)
    pagination = fields.Nested(PaginationSchema, dump_only=True)
