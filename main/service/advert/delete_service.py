from main.models.Advert.advert_model import Advert, session
from main.models.User.user_model import User
from main.middleware.error import Error


def delete_advert_service(id_user, url_advert):
    user = User.query.filter(User.id == id_user).first()
    if not user:
        return Error.server_error()
    advert = Advert.query.filter(Advert.url == url_advert).first()
    if not advert:
        return Error.error_default("This advert doesn't exists!", 400)
    try:
        advert.delete()
        return '', 204
    except Exception as e:
        return Error.server_error(e)