from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.service.offer_service import reqeust_offer_service, accept_offer_service, send_offer_service
from flask_apispec import use_kwargs, marshal_with
from main.schemas.offer_schema import RequestOfferSchema, OfferSchema, SendOfferSchema
from main.middleware.error import Error
offers = Blueprint('offers', __name__)


@offers.route('request_offer', methods=['POST'])
@jwt_required()
@use_kwargs(RequestOfferSchema)
@marshal_with(OfferSchema)
def request_offer(**kwargs):
    try:
        identity = get_jwt_identity()
        return reqeust_offer_service(identity, **kwargs)
    except Exception as e:
        return Error.server_error(msg=e)


@offers.route('accept_offer/<int:id_offer>', methods=['PUT', 'DELETE'])
@jwt_required()
@marshal_with(OfferSchema)
def cancel_offer(id_offer):
    identity = get_jwt_identity()
    is_accept = False if request.method == 'DELETE' else True
    return accept_offer_service(id_offer, is_accept, identity)


@offers.route('send_offer', methods=['POST'])
@jwt_required()
@use_kwargs(SendOfferSchema)
@marshal_with(OfferSchema)
def send_offer(**kwargs):
    identity = get_jwt_identity()
    return send_offer_service(identity, **kwargs)
