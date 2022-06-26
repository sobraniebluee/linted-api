from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.schemas.review_schema import MemberReviewSchema
from main.service.review_service import add_review_service, delete_review_service, update_review_service
from main import docs
reviews = Blueprint('reviews', __name__)


@reviews.route('', methods=['POST'])
@jwt_required()
@use_kwargs(MemberReviewSchema)
@marshal_with(MemberReviewSchema)
def add_review(**kwargs):
    identity = get_jwt_identity()
    return add_review_service(identity, **kwargs)


@reviews.route('<int:id_review>', methods=['PUT'])
@jwt_required()
@use_kwargs(MemberReviewSchema(only=('rating', 'description')))
@marshal_with(MemberReviewSchema)
def update_review(id_review, **kwargs):
    identity = get_jwt_identity()
    return update_review_service(identity, id_review, **kwargs)


@reviews.route('<int:id_review>', methods=['DELETE'])
@jwt_required()
def delete_review(id_review):
    identity = get_jwt_identity()
    return delete_review_service(identity, id_review)


docs.register(add_review, blueprint="reviews")
docs.register(delete_review, blueprint="reviews")
docs.register(update_review, blueprint="reviews")

