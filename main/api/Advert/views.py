from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with
from main.schemas.advert_schema import AdvertAddSchema, AdvertConditionSchema, AdvertSchema, AdvertEditSchema
from main.service.advert.advert_service import (
    get_advert_condition_service,
    add_new_advert_data_service,
    get_advert_by_url_service,
    edit_advert_service,
    delete_advert_service,
    get_adverts_service
)
from main.service.advert.like_service import unlike_advert_service, like_advert_service

adverts = Blueprint('adverts', __name__)


@adverts.route('', methods=["GET"])
@marshal_with(AdvertSchema(many=True))
def get_adverts():
    return get_adverts_service()


@adverts.route('<url_advert>', methods=["GET"])
@jwt_required(optional=True)
@marshal_with(AdvertSchema)
def get_advert(url_advert):
    identity = {'jwt': get_jwt_identity(), 'ip': request.remote_addr}
    return get_advert_by_url_service(identity, url_advert=url_advert)


@adverts.route('<url_advert>', methods=["PUT"])
@use_kwargs(AdvertEditSchema)
@marshal_with(AdvertSchema)
@jwt_required()
def edit_advert(url_advert, **kwargs):
    images = kwargs.get('images')
    kwargs.pop('images')
    identity = get_jwt_identity()
    return edit_advert_service(url_advert=url_advert, id_user=identity, images=images, **kwargs)


@adverts.route('', methods=["POST"])
@use_kwargs(AdvertAddSchema)
@marshal_with(AdvertSchema)
@jwt_required()
def add_new_advert(**kwargs):
    identity = get_jwt_identity()
    return add_new_advert_data_service(id_user=identity, **kwargs)


@adverts.route('<url_advert>', methods=["DELETE"])
@jwt_required()
def delete_advert(url_advert):
    identity = get_jwt_identity()
    return delete_advert_service(id_user=identity, url_advert=url_advert)


@adverts.route('like/<url_advert>', methods=["POST"])
@jwt_required()
def like_advert(url_advert):
    identity = get_jwt_identity()
    return like_advert_service(id_user=identity, url_advert=url_advert)


@adverts.route('like/<url_advert>', methods=["DELETE"])
@jwt_required()
def unlike_advert(url_advert):
    identity = get_jwt_identity()
    return unlike_advert_service(id_user=identity, url_advert=url_advert)


@adverts.route('condition', methods=['GET'])
@jwt_required()
@marshal_with(AdvertConditionSchema(many=True))
def get_adverts_condition():
    return get_advert_condition_service()
