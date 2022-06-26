from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

notifications = Blueprint('notifications', __name__)


@notifications.route('count', methods=['GET'])
@jwt_required()
def get_notification_count():
    return '', 204
