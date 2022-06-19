from flask import Blueprint, request
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.service.Member.member_service import (
    get_user_service,
    get_user_wardrobe_service,
    get_user_reviews_service,
    get_user_subscription_service,
    user_search_service)
from main.schemas.advert_schema import AllAdvertsSchema
from main.schemas.pagination_schema import ArgsPagination
from main.schemas.member_subscription_schema import RequestSubscription
from main.service.Member.subscription_service import toggle_subscription_service
from config import Const
from main.schemas.review_schema import AllMemberReviewsSchema
from main.schemas.member_schema import MemberSchema, QueryMemberSchema, AllMemberSubs,ResponseSearchMembersSchema
from main.schemas.user_schema import UserSchema
from main.decorators import pagination

members = Blueprint('members', __name__)


@members.route('search', methods=['GET'])
@jwt_required(optional=True)
@use_kwargs(QueryMemberSchema, location='query')
@marshal_with(ResponseSearchMembersSchema)
@pagination(_limit=Const.MAX_MEMBER_PER_PAGE)
def get_users_search(**kwargs):
    return user_search_service(**kwargs)


@members.route('<username>', methods=['GET'])
@jwt_required(optional=True)
@marshal_with(MemberSchema)
def get_user(username):
    return get_user_service(username)


@members.route('<username>/wardrobe', methods=['GET'])
@jwt_required(optional=True)
@use_kwargs(ArgsPagination, location='query')
@marshal_with(AllAdvertsSchema)
@pagination(_limit=Const.PAGE_COUNT_ADVERT)
def get_user_wardrobe(username, **kwargs):
    identity = get_jwt_identity()
    return get_user_wardrobe_service(username=username, id_user=identity)


@members.route('<username>/reviews', methods=['GET'])
@jwt_required(optional=True)
@use_kwargs(ArgsPagination, location='query')
@marshal_with(AllMemberReviewsSchema)
@pagination(_limit=24)
def get_user_reviews(username, **kwargs):
    return get_user_reviews_service(username, None)


@members.route('<username>/follows', methods=['GET'])
@jwt_required(optional=True)
@use_kwargs(ArgsPagination)
@marshal_with(AllMemberSubs)
@pagination(_limit=24)
def get_user_follows(username):
    return get_user_subscription_service(username, Const.FOLlOWS)


@members.route('<username>/followers', methods=['GET'])
@jwt_required(optional=True)
@use_kwargs(ArgsPagination)
@marshal_with(AllMemberSubs)
@pagination(_limit=24)
def get_user_followers(username):
    return get_user_subscription_service(username, Const.FOLLOWERS)


@members.route('subscription', methods=['POST', 'DELETE'])
@jwt_required()
@use_kwargs(RequestSubscription)
def toggle_subscription(**kwargs):
    id_follower = get_jwt_identity()
    type_toggle = Const.FOLLOW if request.method == 'POST' else Const.UNFOLLOW
    return toggle_subscription_service(id_follower, type_toggle, **kwargs)




