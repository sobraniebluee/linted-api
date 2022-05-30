from main.models.Category.category_model import Category
from main.middleware.error import Error


def get_categories_service():
    try:
        items = Category.query.filter(Category.id_root == None).all()
        categories = []

        for item in items:
            get_all_categories(item.id_category, categories)

        return {'categories': categories}, 200
    except Exception as e:
        return Error.server_error(str(e))


def get_category_service(id_category):
    try:
        category = Category.query.filter(Category.id_category == id_category).first()
        if not category:
            return Error.server_error("Sorry,this category does not exists!")
        category_resp = []
        get_all_categories(category.id_category, category_resp)
        return category_resp[0], 200
    except Exception as e:
        return Error.server_error(e)


def get_all_categories(id_category, categories):
    category = Category.query.filter(Category.id_category == id_category).first()
    obj = {
        'id': category.id_category,
        'title': category.title,
        'url': category.url,
        'is_root': category.is_root,
        'categories': []
    }
    if category.is_root:
        sub_categories = Category.query.filter(Category.id_root == category.id_category)
        for sub_category in sub_categories:
            get_all_categories(sub_category.id_category, obj['categories'])
    categories.append(obj)



def add_category_service(id_category, id_root, is_root, title, url):
    try:
        root_category = Category.query.filter(Category.id_category == id_root).first()
        if not root_category:
            return Error.server_error(f'Sorry,category with id {id_root} not exist! ')
        new_category = Category(id_category=id_category, id_root=id_root, is_root=is_root, title=title, url=None)
        new_category.save()
        return new_category, 200
    except Exception as e:
        return Error.server_error(e)


def delete_category_service(id_category):
    try:
        category = Category.query.filter(Category.id_category == id_category).first()
        if not category:
            return Error.server_error('Sorry,this category doesn\'t exist!')
        if not category.is_root:
            category.delete()
        else:
            sub_category = Category.query.filter(Category.id_root == id_category).first()
            if not sub_category:
                category.delete()
            else:
                return Error.server_error('Sorry,this category have sub category!')

        return '', 204
    except Exception as e:
        return Error.server_error(e)
