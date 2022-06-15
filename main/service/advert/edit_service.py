from main.models.Advert.advert_model import Advert, AdvertImage, session
from main.models.File.file_model import File
from main.models.User.user_model import User
from main.middleware.error import Error


def edit_advert_service(id_user, url_advert, images, **kwargs):
    user = User.query.filter(User.id == id_user).first()
    if not user:
        return Error.server_error()
    advert = Advert.query.filter(Advert.url == url_advert).first()
    if not advert:
        return Error.error_default("This advert doesn't exists!", 400)

    images = list(set((images)))

    for key, value in kwargs.items():
        setattr(advert.advert_info, key, value)
    # Check waste images in database and delete this
    # First must be found all images than we check used or unused this
    all_images = AdvertImage.query.filter(AdvertImage.id_advert == advert.id).all()
    all_id_images_advert = list(map(lambda x: str(x.id_image), all_images))
    for id_image_advert in all_id_images_advert:
        if id_image_advert not in images:
            try:
                waste_image = list(filter(lambda item: str(item.id_image) == id_image_advert, all_images))
                if waste_image:
                    waste_image[0].delete()
            except Exception as e:
                return Error.server_error(e)

    for image in images:
        advert_image = AdvertImage.query.filter(AdvertImage.id_image == image).first()
        is_preview = True if images[0] == image else False
        if not advert_image:
            file_image = File.query.filter(File.id == image).first()
            if file_image:
                new_advert_image = AdvertImage(id_advert=advert.id, id_image=file_image.id, is_preview=is_preview)
                new_advert_image.save()
        else:
            setattr(advert_image, 'is_preview', is_preview)

    return '', 204

