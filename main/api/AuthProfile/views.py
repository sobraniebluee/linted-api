from flask import Blueprint, request
from main.schemas.profile_schema import ProfileSchema
from main.schemas.user_schema import AuthSchema, UserAvatarSchema
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.service.profile_service import (
    get_profile_data_service,
    update_profile_data_service,
    update_avatar_service
)

profile = Blueprint('profile', __name__)


@profile.route('/', methods=['GET'])
@marshal_with(AuthSchema)
@jwt_required()
def get_profile_data():
    try:
        identity = get_jwt_identity()
        return get_profile_data_service(user_id=identity)
    except Exception:
        raise


@profile.route('/', methods=['PUT'])
@use_kwargs(ProfileSchema)
@marshal_with(AuthSchema)
@jwt_required()
def update_profile_data(**kwargs):
    try:
        identity = get_jwt_identity()
        return update_profile_data_service(user_id=identity, **kwargs)
    except Exception as e:
        return {'message': f'Server Error: {str(e)}'}


@profile.route('/avatar', methods=['POST'])
@marshal_with(UserAvatarSchema)
@jwt_required()
def upload_profile_avatar():
    try:
        file = request.files['avatar']
        identity = get_jwt_identity()
        return update_avatar_service(user_id=identity, file=file)
    except Exception as e:
        return {'message': f'Server Error: {str(e)}'}

