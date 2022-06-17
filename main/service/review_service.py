from main.models.Review.review_model import MemberReview, session
from main.models.Advert.advert_model import Advert
from main.models.User.user_model import User
from main.models.Transaction.transaction_model import Transaction
from main.middleware.error import Error


def add_review_service(id_buyer, id_advert, rating, description=None):
    advert = session.query(Advert.id_user).filter(Advert.id == id_advert).first()
    if not advert:
        return Error.server_error()
    id_seller, = advert
    is_seller = session.query(User.id).filter(User.id == id_seller).first()
    is_buyer = session.query(User.id).filter(User.id == id_buyer).first()

    if not is_seller or not is_buyer:
        return Error.server_error()

    transaction = session.query(Transaction.is_finish).filter(
        Transaction.id_advert == id_advert,
        Transaction.id_buyer == id_buyer,
        Transaction.id_seller == id_seller,
        Transaction.is_finish == True
    ).first()
    if not transaction:
        return Error.server_error(msg="tran")

    has_review = session.query(MemberReview.id).filter(
        MemberReview.id_buyer == id_buyer,
        MemberReview.id_seller == id_seller
    ).first()

    if has_review:
        return Error.server_error()
    new_review = MemberReview(id_seller, id_buyer, id_advert, rating, description)
    new_review.save()

    return new_review, 200


def update_review_service(id_user, id_review, rating, description=None):
    review = MemberReview.query.filter(MemberReview.id == id_review, MemberReview.id_buyer == id_user).first()
    if not review:
        return Error.error_not_found()

    setattr(review, 'rating', rating)
    setattr(review, 'description', description)
    review.commit()
    return review, 200


def delete_review_service(id_user, id_review):
    review = MemberReview.query.filter(MemberReview.id == id_review, MemberReview.id_buyer == id_user).first()
    if not review:
        return Error.error_not_found()
    review.delete()
    return '', 204

