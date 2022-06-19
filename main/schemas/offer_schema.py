from marshmallow import Schema, fields, validate
from config import Const


class RequestOfferSchema(Schema):
    id_advert = fields.String(required=True)
    price = fields.Float(required=True, validate=[validate.Range(0, Const.MAX_PRICE)])


class SendOfferSchema(Schema):
    id_advert = fields.String(required=True)
    id_buyer = fields.String(required=True)
    price = fields.Float(required=True, validate=[validate.Range(0, Const.MAX_PRICE)])


class OfferSchema(Schema):
    id = fields.Integer(dump_only=True)
    id_advert = fields.String(dump_only=True)
    id_buyer = fields.String(dump_only=True)
    price = fields.Float(dump_only=True)
    is_accepted = fields.Boolean(dump_only=True)
    created_at = fields.String(dump_only=True)
    update_at = fields.String(dump_only=True)
    message = fields.String(dump_only=True)