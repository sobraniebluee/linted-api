from main.models.Advert.advert_model import Advert, AdvertInfo, AdvertImage, AdvertCondition, AdvertWatches, session
from main.models.File.file_model import File
from main.models.User.user_model import User
from main.models.Category.category_model import Category
from main.models.Size.size_model import Size
from main.middleware.error import Error


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


# Нужно для проверки категории
def recursive_find_root_category(id_root):
    root_category = Category.query.filter(Category.id_category == id_root).first()
    if root_category.id_root == 1:
        return root_category
    else:
        recursive_find_root_category(root_category.id_root)
