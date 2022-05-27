from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.schemas.user_schema import UserSchema, AuthSchema, JWTSchema, UserAdditionalInfo

from main.service.user_service import (
    register_user_service,
    login_user_service,
    refresh_token_service,
    logout_service,
    additional_info_service
)

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register_user(**kwargs):
    try:
        user = register_user_service(**kwargs)
        return user
    except Exception as e:
        raise e


@users.route('/login', methods=["POST"])
@use_kwargs(UserSchema(only=('email', 'password', 'username')))
@marshal_with(AuthSchema)
def login_user(**kwargs):
    try:
        user = login_user_service(**kwargs)
        return user
    except Exception as e:
        raise e


@users.route('/token/refresh', methods=["POST"])
@jwt_required(refresh=True)
@marshal_with(JWTSchema)
def refresh_token():
    try:
        identity = get_jwt_identity()
        tokens = refresh_token_service(identity=identity)
        return tokens
    except Exception as e:
        raise


@users.route('/logout', methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    try:
        identity = get_jwt_identity()
        response = logout_service(user_id=identity)
        return response
    except Exception:
        raise


@users.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    id_user = get_jwt_identity()
    return {'msg': id_user}


@users.route('/additional_info', methods=['POST'])
@use_kwargs(UserAdditionalInfo)
@marshal_with(UserAdditionalInfo)
@jwt_required()
def additional_info(**kwargs):
    try:
        identity = get_jwt_identity()
        return additional_info_service(identity=identity, **kwargs)
    except Exception:
        raise


