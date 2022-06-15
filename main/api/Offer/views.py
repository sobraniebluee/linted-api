from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

offers = Blueprint('offers', __name__)


@offers.route('request_offer', methods=['POST'])
@jwt_required()
def request_offer():
    identity = get_jwt_identity()
    return '', 204


