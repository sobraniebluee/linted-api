from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required
from main.service.size_service import add_sizes_service, get_sizes_service
from main.schemas.size_schema import SizeSchema

sizes = Blueprint('sizes', __name__)


@sizes.route('', methods=["GET"])
# @jwt_required()
def get_sizes():
    category_id = request.args.get('category_id')
    sizes_resp = get_sizes_service(category_id)
    if sizes_resp[1] == 404:
        return sizes_resp
    else:
        schema = SizeSchema(many=True)
        return jsonify(schema.dump(sizes_resp[0])), sizes_resp[1]


@sizes.route('', methods=["POST"])
@use_kwargs(SizeSchema)
@marshal_with(SizeSchema)
# @jwt_required()
def add_sizes(**kwargs):
    return add_sizes_service(**kwargs), 200

