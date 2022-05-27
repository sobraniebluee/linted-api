from main.models.User.user_model import User, UserAdditionalInfo, UserAvatar, func
from sqlalchemy.exc import IntegrityError
from main.utils import _error_response
from main.service.aws.upload_aws import UploadAws


def get_profile_data_service(user_id):
    user_data = User.query.filter(User.id == user_id).first()
    if user_data:
        return {'data': user_data}, 200
    else:
        return {'message': 'Not found!'}, 404


def update_profile_data_service(user_id, **kwargs):
    user = User.query.filter(User.id == user_id).first()
    user_additional_info = UserAdditionalInfo.query.filter(UserAdditionalInfo.id_user == user.id).first()
    if not user or not user_additional_info:
        return {'message': 'Not found!'}, 404
    try:
        if user_additional_info.is_fill:
            for key, value in kwargs.items():
                if key == 'username':
                    setattr(user, key, f'@{value}')
                setattr(user_additional_info, key, value)
            setattr(user_additional_info, 'updated_at', func.now())
            try:
                user.commit()
            except Exception as ex:
                if isinstance(ex, IntegrityError):
                    return {'message': _error_response('username', 'Sorry,this username already taken')}
                else:
                    return {'message': f'Server Error: {str(ex)}'}, 500
            user_additional_info.commit()

            return {'data': user}, 200
        return '', 405
    except Exception as e:
        return {'message': f'Server Error: {str(e)}'}, 500


def update_avatar_service(user_id, file):
    try:
        user_avatar = UserAvatar.query.filter(UserAvatar.id_user == user_id).first()
        if not user_avatar:
            return {'message': 'Not Found'}, 404
        # Upload
        response_status, response_info = UploadAws.upload_full_avatar(file=file)
        if not response_status:
            return {'message': response_info}, 500
        for key, item in response_info.items():
            setattr(user_avatar, key, item)
        user_avatar.commit()
        return response_info, 200
    except Exception as e:
        return {'message': f'Server Error: {str(e)}'}, 500

