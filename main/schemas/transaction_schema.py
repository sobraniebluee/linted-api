from marshmallow import Schema, fields
from main.schemas.advert_schema import AdvertSchema


class CreateTransactionSchema(Schema):
    id_advert = fields.String(required=True)


class TransactionSchema(Schema):
    id = fields.Integer(dump_only=True)
    id_buyer = fields.String(dump_only=True)
    id_seller = fields.String(dump_only=True)
    id_advert = fields.String(dump_only=True)
    price = fields.Float(dump_only=True)
    is_finish = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    advert = fields.Nested(AdvertSchema, dump_only=True)
    message = fields.String(dump_only=True)