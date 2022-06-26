from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.schemas.user_schema import UserSchema, ResponseAuthSchema, JWTSchema, RegisterSchema,UserAdditionalInfo
from main.service.user_service import (
    register_user_service,
    login_user_service,
    refresh_token_service,
    logout_service,
    additional_info_service
)
from main import docs
users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
@use_kwargs(RegisterSchema)
@marshal_with(ResponseAuthSchema)
def register_user(**kwargs):
    ip_user = request.remote_addr
    return register_user_service(ip_user=ip_user, **kwargs)


@users.route('/login', methods=["POST"])
@use_kwargs(UserSchema(only=('email', 'password', 'username')))
@marshal_with(ResponseAuthSchema)
def login_user(**kwargs):
    return login_user_service(**kwargs)


@users.route('/token/refresh', methods=["POST"])
@jwt_required(refresh=True)
@marshal_with(JWTSchema)
def refresh_token():
    identity = get_jwt_identity()
    return refresh_token_service(identity=identity)


@users.route('/logout', methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    identity = get_jwt_identity()
    return logout_service(user_id=identity)


@users.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    id_user = get_jwt_identity()
    return {'msg': id_user}


@users.route('/additional_info', methods=['POST'])
@jwt_required()
@use_kwargs(UserAdditionalInfo)
@marshal_with(UserAdditionalInfo)
def additional_info(**kwargs):
    identity = get_jwt_identity()
    return additional_info_service(identity=identity, **kwargs)


docs.register(register_user, blueprint='users')
docs.register(login_user, blueprint='users')
docs.register(logout, blueprint='users')
docs.register(refresh_token, blueprint='users')
docs.register(additional_info, blueprint='users')


