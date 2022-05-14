from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from main.schemas.users import UsersSchema, AuthSchema
from main import app
from main.service.users_service import register_user_service, login_user_service
users = Blueprint('users', __name__)

URL = f"{app.config['ROOT_API_PATH']}/user"


@users.route(f'{URL}/register', methods=['POST'])
@use_kwargs(UsersSchema)
@marshal_with(AuthSchema)
def register_user(**kwargs):
    try:
        user = register_user_service(**kwargs)
        return user
    except Exception as e:
        raise e


@users.route(f'{URL}/login', methods=["POST"])
@use_kwargs(UsersSchema(only=('email', 'password', 'username')))
@marshal_with(AuthSchema)
def login_user(**kwargs):
    try:
        user = login_user_service(**kwargs)
        return jsonify(user)
    except Exception as e:
        raise e

