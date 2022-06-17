from main.models.Advert.advert_model import Advert, AdvertLikes, session
from main.middleware.error import Error


def like_advert_service(id_user, url_advert):
    advert = Advert.query.filter(Advert.url == url_advert).first()
    if not advert or advert.is_ban is not False:
        return Error.error_not_found(msg="Advert not found!")
    is_liked = AdvertLikes.query.filter(AdvertLikes.id_user == id_user, AdvertLikes.id_advert == advert.id).first()
    if is_liked:
        return Error.error_default("Is Advert already added to favourites", 400)

    like = AdvertLikes(id_user=id_user, id_advert=advert.id)
    like.save()
    return '', 204


def unlike_advert_service(id_user, url_advert):
    advert = Advert.query.filter(Advert.url == url_advert).first()
    if not advert:
        return Error.error_not_found("Advert not found!")
    like = AdvertLikes.query.filter(AdvertLikes.id_user == id_user, AdvertLikes.id_advert == advert.id).first()
    if not like:
        return Error.server_error(msg="Sorry,something went wrong!")
    like.delete()
    return '', 204




