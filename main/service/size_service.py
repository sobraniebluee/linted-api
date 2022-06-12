from main.models.Size.size_model import Size
from main.models.Category.category_model import Category
from main.middleware.error import Error


def get_sizes_service(id_category):
    try:
        sizes = Size.query.filter(Size.id_category == id_category).all()
        if not sizes:
            return Error.error_not_found()
        return sizes, 200
    except Exception as e:
        return Error.server_error(str(e))


def add_sizes_service(id_category, title):
    try:
        category = Category.query.filter(Category.id_category == id_category).first()
        if not category:
            return Error.error_not_found()
        new_size = Size(id_category=id_category, title=title)
        new_size.save()
        return new_size
    except Exception as e:
        return Error.server_error(str(e))