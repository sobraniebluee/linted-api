from main.models.Advert.advert_model import Advert, AdvertInfo, AdvertCondition, AdvertWatches, session
from main.models.Category.category_model import Category
from main.models.Size.size_model import Size
from main.middleware.error import Error
from sqlalchemy import or_
from config import Config
import math
import re


def get_adverts_service(**kwargs):
    categories_id = kwargs.get('categories_id', None)
    conditions_id = kwargs.get('conditions_id', None)
    sizes_id = kwargs.get('sizes_id', None)
    search_text = kwargs.get('search_text', '')
    sort = kwargs.get('sort', None)
    price_from = kwargs.get('price_from', 0)
    price_to = kwargs.get('price_to', Config.MAX_PRICE)
    page = kwargs.get('page', 1)

    if sort == 'desc':
        order_sort = AdvertInfo.price.desc()
    elif sort == 'asc':
        order_sort = AdvertInfo.price.asc()
    elif sort == 'newest':
        order_sort = Advert.created_at.asc()
    else:
        order_sort = Advert.id.desc()

    stm = session.query(Advert)
    if categories_id:
        categories_id = find_all_sub_catalogs(categories_id)
        stm = stm.where(AdvertInfo.category_id.in_(categories_id))
    if sizes_id:
        stm = stm.where(AdvertInfo.size_id.in_(sizes_id))
    if conditions_id:
        stm = stm.where(AdvertInfo.condition_id.in_(conditions_id))
    if search_text:
        # Remove all symbols
        pattern = r"[.,\/#!$%\^&\*;:{}=\-_`~()]"
        search_text = re.sub(pattern, '', search_text)
        search_text = search_text.strip().upper().split(' ')
        # Check for each word in tables
        for word in search_text:
            stm = stm.where(or_(
                AdvertInfo.title.ilike(f"%{word}%"),
                AdvertInfo.description.ilike(f"%{word}%"),
                Category.title.ilike(f"%{word}%"),
                Size.title.ilike(f"%{word}%")
            )).filter(AdvertInfo.category_id == Category.id_category,
                      AdvertInfo.size_id == Size.id)

    stm = stm.filter(
        AdvertInfo.price >= price_from,
        AdvertInfo.price <= price_to,
        AdvertInfo.id_advert == Advert.id
    )
    stm_cte = stm.cte()
    adverts_id = session.query(stm_cte).all()
    if adverts_id:
        tmp_id = []
        for id_advert, *args in adverts_id:
            tmp_id.append(id_advert)
        adverts = Advert.query.where(
                Advert.id.in_(tmp_id)).filter(
                AdvertInfo.id_advert == Advert.id,
            ).order_by(order_sort).offset(
            page * Config.PAGE_COUNT_ADVERT
        ).limit(
            Config.PAGE_COUNT_ADVERT
        ).all()
    else:
        adverts = []

    page = page + 1 if page == 0 else page
    adverts_count = len(adverts_id)
    total_pages = math.ceil(adverts_count / Config.PAGE_COUNT_ADVERT)
    response = {
        'items': adverts,
        'pagination': {
            'current_page': page,
            'total_entries': adverts_count,
            'total_pages': total_pages
        }
    }
    return response, 200


def get_advert_by_url_service(identity, url_advert):
    advert = Advert.query.filter(Advert.url == url_advert).first()
    if not advert:
        return Error.error_not_found()
    watch_advert(identity=identity, id_advert=advert.id)
    return advert, 200


def find_all_sub_catalogs(categories_id):
    result = []
    for category_id in categories_id:
        category = Category.query.filter(Category.id_category == category_id).first()
        if category:
            recursive_find_sub_categories(category.id_category, category.is_root, result)
    return result


# find for one root category all sub categories
def recursive_find_sub_categories(id_category, is_root, result):
    if is_root:
        all_sub_categories = session.query(Category.id_category, Category.is_root).filter(Category.id_root == id_category).all()
        for id_category, is_root in all_sub_categories:
            recursive_find_sub_categories(id_category, is_root, result)
    else:
        result.append(id_category)


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



