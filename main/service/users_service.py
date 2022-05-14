from main.models.users import User, UserAvatar
from utils import get_ip_addr,_error_response


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
        user = User(**kwargs, ip=get_ip_addr())
        user.save()
        data = user.auth(email=email, password=password)
        return {"access_token": user.get_access_token(), "data": data}, 200
    except Exception:
        return {'message': 'Error Server!'}, 500


def login_user_service(**kwargs):
    username = kwargs.get('username', None)
    email = kwargs.get('email', None)
    password = kwargs.get('password')

    if not username and not email:
        return '', 405
    if email:
        try:
            user = User.auth(email=email, password=password)
            return {"access_token": user.get_access_token(), "data": user}, 200
        except Exception as e:
            return {'message': str(e)}, 400
    if username:
        try:
            user = User.auth(username=username, password=password)
            return {"access_token": user.get_access_token(), "data": user}, 200
        except Exception as e:
            return {'message': str(e)}, 400


