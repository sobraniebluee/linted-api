from main.models.User.user_model import User, session
from main.middleware.error import Error
from main.models.Advert.advert_model import Advert
from main.models.Review.review_model import MemberReview
from main.models.MemberSubscription.member_subscription_model import MemberSubscription
from sqlalchemy import func
from config import Const
import math
import re
from sqlalchemy import or_


def user_search_service(search_text, page):
    if search_text == '':
        return Error.error_not_found()
    stm = session.query(User.id)
    pattern = r"[.,\/#!$%\^&\*;:{}=\-_`~()]"
    search_text = re.sub(pattern, '', search_text)
    search_text = search_text.strip().upper().split(' ')
    for word in search_text:
        stm = stm.where(or_(
            User.username.ilike(f"%{word}%"),
        ))
    stm_cte = stm.cte()
    users_id = session.query(stm_cte).all()
    users = []
    if users_id:
        for user_id, in users_id:
            user = User.query.filter(User.id == user_id).first()
            users.append(user)
        users = [users[i:i + Const.MAX_MEMBER_PER_PAGE] for i in range(0, len(users_id), Const.MAX_MEMBER_PER_PAGE)]
        try:
            users = users[page]
        except IndexError:
            users = []
    else:
        users = []

    page = page + 1
    users_count = len(users_id)
    total_pages = math.ceil(users_count / Const.MAX_MEMBER_PER_PAGE)
    response = {
        'users': users,
        'pagination': {
            'current_page': page,
            'per_page': Const.MAX_MEMBER_PER_PAGE,
            'total_entries': users_count,
            'total_pages': total_pages
        }
    }
    return response, 200


def get_user_service(username):
    user = session.query(User.id).filter(User.username == username).first()
    if not user:
        return Error.error_not_found()
    user_id, = user
    followers = session.query(MemberSubscription.id).filter(MemberSubscription.id_leader == user_id).count()
    follows = session.query(MemberSubscription.id).filter(MemberSubscription.id_follower == user_id).count()
    rating, count_reviews = session.query(func.avg(MemberReview.rating), func.count(MemberReview.id)).filter(MemberReview.id_seller == user_id).first()
    if not rating:
        rating = 0.0
    else:
        rating = round(rating, 2)
    response = {
        'user': user,
        'followers': followers,
        'follows': follows,
        'rating': rating,
        'count_reviews': count_reviews
    }
    return response, 200


def get_user_wardrobe_service(username, id_user=None):
    if not id_user:
        id_user, = session.query(User.id).filter(User.username == username).first()
        if not id_user:
            return Error.error_not_found()
        condition_is_bought = Advert.is_bought == False
    else:
        condition_is_bought = Advert.is_bought.in_([True, False])
    adverts = Advert.query.filter(Advert.id_user == id_user, condition_is_bought).all()
    return adverts, 200


def get_user_reviews_service(username, me_id_user=None):
    user = session.query(User.id).filter(User.username == username).first()
    if not user:
        Error.server_error()
    id_user, = user
    user_reviews = MemberReview.query.filter(MemberReview.id_seller == id_user).all()

    return user_reviews, 200


def get_user_subscription_service(username, type_request):
    user = session.query(User.id).filter(User.username == username).first()
    if not user:
        Error.server_error()
    id_user, = user
    if type_request == Const.FOLlOWS:
        user_subscriptions = session.query(MemberSubscription.id_leader).filter(MemberSubscription.id_follower == id_user).all()
    else:
        user_subscriptions = session.query(MemberSubscription.id_follower).filter(MemberSubscription.id_leader == id_user).all()

    response = []
    for user_id, in user_subscriptions:
        user_sub = User.query.filter(User.id == user_id).first()
        response.append(user_sub)
    return response, 200
