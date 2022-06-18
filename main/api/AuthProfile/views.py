from flask import Blueprint, request
from main.schemas.profile_schema import ProfileSchema
from main.schemas.user_schema import AuthSchema, UserAvatarSchema
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.service.profile_service import (
    get_profile_data_service,
    update_profile_data_service,
    update_avatar_service,
    get_user_favourites_service
)
from main.schemas.advert_schema import AdvertSchema

profile = Blueprint('profile', __name__)


@profile.route('/', methods=['GET'])
@jwt_required()
@marshal_with(AuthSchema)
def get_profile_data():
    try:
        identity = get_jwt_identity()
        return get_profile_data_service(user_id=identity)
    except Exception:
        raise


@profile.route('/', methods=['PUT'])
@jwt_required()
@use_kwargs(ProfileSchema)
@marshal_with(AuthSchema)
def update_profile_data(**kwargs):
    try:
        identity = get_jwt_identity()
        return update_profile_data_service(user_id=identity, **kwargs)
    except Exception as e:
        return {'message': f'Server Error: {str(e)}'}


@profile.route('/avatar', methods=['POST'])
@jwt_required()
@marshal_with(UserAvatarSchema)
def upload_profile_avatar():
    try:
        file = request.files['avatar']
        identity = get_jwt_identity()
        return update_avatar_service(user_id=identity, file=file)
    except Exception as e:
        return {'message': f'Server Error: {str(e)}'}


@profile.route('/favourites', methods=['GET'])
@jwt_required()
@marshal_with(AdvertSchema(many=True))
def user_favourites():
    identity = get_jwt_identity()
    return get_user_favourites_service(identity)
