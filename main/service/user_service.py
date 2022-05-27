from main.models.User.user_model import User, UserAdditionalInfo, UserAvatar, UserTokens, func
from main.utils import get_ip_addr, _error_response
from main.service.token_service import jwt_tokens
from config import ConfigAWS


# Register Auth

# Response code [200,405,400,500]
# Response schema error: 400
# {
#   message: {
#       fieldName: [ errorText ]
#    }
# }


def register_user_service(**kwargs):
    email = kwargs.get('email', None)
    username = kwargs.get('username', None)
    password = kwargs.get('password')
    is_exists_email = User.query.filter(User.email == email).first()
    is_exists_username = User.query.filter(User.username == f'@{username}').first()

    if not username or not email:
        return '', 405
    if is_exists_email:
        return {"message": _error_response('email', 'Sorry,this email already used')}, 400
    if is_exists_username:
        return {"message": _error_response('username', 'Sorry,this username already used')}, 400
    try:
        # Create Auth
        user = User(**kwargs)
        user.save()
        # Create Additional Info
        user_additional_info = UserAdditionalInfo(id_user=user.id, ip_user=get_ip_addr())
        user_additional_info.save()
        # Create Default Avatar
        default_path = f"{ConfigAWS.AWS_ENDPOINT}{ConfigAWS.AWS_DEFAULT_AVATAR_PATH}"
        user_avatar = UserAvatar(user_id=user.id, path=default_path)
        user_avatar.save()
        # Login Auth
        return login_user_service(email=email, password=password)
    except Exception as e:
        return {'message': f"Server error: {e}"}, 501


# Login Auth

# Response code [200,405,400,500]
# Response schema error: 400
# {
#   message: {
#       fieldName: [ errorText ]
#    }
# }


def login_user_service(**kwargs):
    username = kwargs.get('username', None)
    email = kwargs.get('email', None)
    password = kwargs.get('password')

    if not username and not email:
        return '', 405
    if username and email:
        return '', 405

    try:
        # Auth by email
        if email:
            user = User.auth(email=email, password=password)
            return is_login(user)
        # Auth by email
        if username:
            user = User.auth(username=username, password=password)
            return is_login(user)
    except Exception as e:
        return {'message': f"Server error: {e}"}, 500


# is_login Helper function for login_user_service


def is_login(user):
    if user['auth']:
        tokens = jwt_tokens(user['data'].id)
        response = {"jwt": tokens, "data": user["data"]}
        return response, 200
    if not user['auth']:
        return {'message': user['error']}, 400


def refresh_token_service(**kwargs):
    try:
        identity = kwargs.get('identity')
        user = User.query.filter(User.id == identity).first()
        if user:
            response = jwt_tokens(user.id)
            return response, 200
        else:
            return '', 401
    except Exception as e:
        return {'message': f"Server error: {e}"}, 500


def logout_service(user_id):
    try:
        user_token = UserTokens.query.filter(UserTokens.user_id == user_id).first()

        if user_token:
            user_token.remove()
            return '', 204
    except Exception as e:
        return {'message': f"Server error: {e}"}, 500


def additional_info_service(identity, **kwargs):
    try:
        user_data = UserAdditionalInfo.query.filter(UserAdditionalInfo.id_user == identity).first()
        if not user_data:
            return {'message': 'Not found user'}, 404
        if not user_data.is_fill:
            for key, value in kwargs.items():
                setattr(user_data, key, value)
            setattr(user_data, 'is_fill', True)
            setattr(user_data, 'updated_at', func.now())
            user_data.commit()
            return user_data, 200
        else:
            return {'message': 'Data already update!'}, 400
    except Exception as e:
        return {'message': f'Error Server: {str(e)}'}, 500



