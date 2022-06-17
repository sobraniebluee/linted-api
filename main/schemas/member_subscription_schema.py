from marshmallow import Schema, fields


class RequestSubscription(Schema):
    id_leader = fields.String(required=True)
