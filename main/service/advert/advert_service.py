from main.models.Advert.advert_model import Advert, AdvertInfo, AdvertImage, AdvertCondition, AdvertWatches, session
from main.models.File.file_model import File
from main.models.User.user_model import User
from main.models.Category.category_model import Category
from main.models.Size.size_model import Size
from main.middleware.error import Error
from sqlalchemy import or_


def get_adverts_service():
    adverts = Advert.query.all()
    if not adverts:
        return Error.error_not_found()
    return adverts, 200


def get_advert_by_url_service(identity, url_advert):
    advert = Advert.query.filter(Advert.url == url_advert).first()
    if not advert:
        return Error.error_not_found()
    watch_advert(identity=identity, id_advert=advert.id)
    return advert, 200


def add_new_advert_data_service(id_user, title, description, price, category_id, condition_id, images, size_id=None):
    user = User.query.filter(User.id == id_user).first()
    category = Category.query.filter(Category.id_category == category_id).first()
    images = list(set((images)))
    for image in images:
        try:
            is_image = File.query.filter(File.id == image).first()
            if not is_image:
                return Error.server_error()
        except Exception:
            return Error.server_error()
    if not user:
        return Error.server_error()
    # if not user.verified:
    #     return Error.error_default('Please verified your account!', 401)
    if not category:
        return Error.error_default('Please,select correct category!', 400)
    if not check_size_id(category, size_id):
        return Error.error_default('Please,select correct size!', 400)
    try:
        new_advert = Advert(id_user)
        new_advert.save()
        id_advert = new_advert.id
        new_advert_info = AdvertInfo(id_advert=id_advert,
                                     title=title,
                                     description=description,
                                     price=round(price, 2),
                                     category_id=category_id,
                                     condition_id=condition_id,
                                     size_id=size_id)
        new_advert_info.save()
        for image in images:
            file_image = File.query.filter(File.id == image).first()
            if not file_image:
                return Error.server_error()
            is_preview = True if images[0] == image else False
            advert_image = AdvertImage(id_advert=id_advert, id_image=file_image.id, is_preview=is_preview)
            advert_image.save()
        return new_advert, 200
    except Exception as e:
        return Error.server_error(e)


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

    return advert, 200


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


def check_size_id(category, size_id):
    root_category = recursive_find_root_category(category.id_root)
    size = Size.query.filter(Size.id_category == root_category.id_category, Size.id == size_id).first()
    if not size:
        return False
    else:
        return True


def recursive_find_root_category(id_root):
    root_category = Category.query.filter(Category.id_category == id_root).first()
    if root_category.id_root == 1:
        return root_category
    else:
        recursive_find_root_category(root_category.id_root)


def get_advert_condition_service():
    try:
        adverts_condition = AdvertCondition.query.all()
        return adverts_condition, 200
    except Exception as e:
        return {'message': 'Server Error' + str(e)}, 500


def watch_advert(identity, id_advert):
    is_watch = AdvertWatches.query.filter(AdvertWatches.id_advert == id_advert, or_(AdvertWatches.id_user == identity['jwt'], AdvertWatches.ip_user == identity['ip'])).first()
    if not is_watch:
        watch = AdvertWatches(id_user=identity['jwt'], id_advert=id_advert, ip_user=identity['ip'])
        watch.save()
    else:
        if identity['jwt'] and is_watch.id_user is None:
            setattr(is_watch, 'id_user', identity['jwt'])
            session.commit()

