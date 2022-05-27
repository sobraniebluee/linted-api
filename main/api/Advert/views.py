from flask import Blueprint
from flask_apispec import use_kwargs, marshal_with
from main.models.Adverts.adverts_model import Advert, AdvertInfo, AdvertImage
from main.schemas.advert_schema import AdvertAddSchema

adverts = Blueprint('adverts', __name__)


@adverts.route('<id_advert>', methods=["GET"])
def get_advert_by_id(id_advert):
    return {'id': id_advert}, 200


@adverts.route('add', methods=["POST"])
@use_kwargs(AdvertAddSchema)
def add_new_advert():
    pass