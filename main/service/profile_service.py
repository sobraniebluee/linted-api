from main.models.User.user_model import User, UserAdditionalInfo, UserAvatar, func
from sqlalchemy.exc import IntegrityError
from main.utils import _error_response
from main.service.Aws.upload_aws import UploadAws
from main.middleware.error import Error
from main.models.Advert.advert_model import AdvertLikes, Advert


def get_profile_data_service(user_id):
    user_data = User.query.filter(User.id == user_id).first()
    if user_data:
        return {'data': user_data}, 200
    else:
        return Error.error_not_found()


def update_profile_data_service(user_id, **kwargs):
    user = User.query.filter(User.id == user_id).first()
    user_additional_info = UserAdditionalInfo.query.filter(UserAdditionalInfo.id_user == user.id).first()
    if not user or not user_additional_info:
        return Error.error_not_found()
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
                    return Error.server_error(_error_response('username', 'Sorry,this username already taken'))
                else:
                    return Error.server_error(str(ex))
            user_additional_info.commit()

            return {'data': user}, 200
        return '', 405
    except Exception as e:
        return Error.server_error(str(e))


def update_avatar_service(user_id, file):
    try:
        user_avatar = UserAvatar.query.filter(UserAvatar.id_user == user_id).first()
        if not user_avatar:
            return Error.error_not_found()
        # Upload
        response_status, response_info = UploadAws.upload_full_avatar(file=file)
        if not response_status:
            return Error.server_error(response_info)
        for key, item in response_info.items():
            setattr(user_avatar, key, item)
        user_avatar.commit()
        return response_info, 200
    except Exception as e:
        return Error.server_error(e)


def get_user_favourites_service(id_user):
    favourites = Advert.query.filter(AdvertLikes.id_user == id_user, AdvertLikes.id_advert == Advert.id).all()
    return favourites, 200
