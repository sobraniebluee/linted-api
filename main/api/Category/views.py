from flask import Blueprint
from main.schemas.category_schema import CategorySchema
from flask_apispec import use_kwargs, marshal_with
from main.service.category_service import (
    get_category_service,
    get_categories_service,
    add_category_service,
    delete_category_service)
from main import docs

categories = Blueprint('categories', __name__)


@categories.route('', methods=['GET'])
def get_categories():
    return get_categories_service()


@categories.route('<int:id_category>', methods=['GET'])
def get_categories_by_id(id_category):
    return get_category_service(id_category)


@categories.route('', methods=['POST'])
@use_kwargs(CategorySchema)
@marshal_with(CategorySchema)
def add_category(**kwargs):
    return add_category_service(**kwargs)


@categories.route('<int:id_category>', methods=['DELETE'])
def delete_category(id_category):
    return delete_category_service(id_category)


docs.register(get_categories, blueprint="categories")
docs.register(get_categories_by_id, blueprint="categories")
docs.register(add_category, blueprint="categories")
docs.register(delete_category, blueprint="categories")
