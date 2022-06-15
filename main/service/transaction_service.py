from main.models.Advert.advert_model import Advert, session
from main.models.Offer.offer_model import Offer
from main.models.Transaction.transaction_model import Transaction
from main.models.User.user_model import User
from main.middleware.error import Error


def create_transaction_service(id_user, id_advert):
    advert = Advert.query.filter(Advert.id == id_advert, Advert.id_user != id_user).first()
    if not advert:
        return Error.server_error()
    if advert.is_bought:
        return Error.error_default(msg="Product already bought", status_code=400)
    buyer = User.query.filter(User.id == id_user).first()
    seller = User.query.filter(User.id == advert.id_user).first()

    if not buyer or not seller:
        return Error.server_error()

    offer = session.query(Offer.price).filter(Offer.id_advert == advert.id,
                                              Offer.id_buyer == id_user,
                                              Offer.is_accepted == True).first()
    if offer:
        price = offer.price
    else:
        price = advert.info.price

    if buyer.balance < price:
        return Error.error_default(msg="Sorry,please top up your balance!", status_code=400)

    try:
        new_transaction = Transaction(buyer.id, seller.id, advert.id, price)
        new_transaction.save()
    except Exception:
        return Error.server_error(msg="Something went wrong")
    return new_transaction, 200


def complete_transaction_service(id_transaction, id_buyer):
    transaction = Transaction.query.filter(Transaction.id == id_transaction).first()
    if not transaction:
        return Error.server_error()
    if transaction.is_finish:
        return Error.error_default(msg='You already finish this transaction!', status_code=400)

    advert = Advert.query.filter(Advert.id == transaction.id_advert).first()
    if not advert:
        return Error.error_not_found(msg="Sorry,this advert doesn't exist", status_code=400)
    if advert.is_bought:
        return Error.error_default(msg="Product already bought", status_code=400)

    buyer = User.query.filter(User.id == id_buyer).first()
    seller = User.query.filter(User.id == advert.id_user).first()

    if not buyer or not seller:
        return Error.server_error()

    try:
        setattr(buyer, 'balance', buyer.balance - transaction.price)
        setattr(seller, 'balance', seller.balance + transaction.price)
        buyer.commit()
        seller.commit()
        setattr(transaction, 'is_finish', True)
        transaction.commit()
        setattr(advert, 'is_bought', True)
        advert.commit()
        return {
            'status': 'ok'
        }
    except Exception:
        session.rollback()
        return Error.server_error()

# def advert_purchase_service(id_user, url_advert):
#     advert = Advert.query.filter(Advert.url == url_advert).first()
#     if not advert:
#         Error.server_error()
#     buyer = User.query.filter(User.id == id_user).first()
#     seller = User.query.filter(User.id == advert.id_user).first()
#
#     if not buyer or not seller:
#         Error.server_error()
#
#     offer = session.query(Offer.price).filter(Offer.id_advert == advert.id,
#                                               Offer.id_buyer == id_user,
#                                               Offer.is_accepted == True).first()
#     if offer:
#         price = offer.price
#     else:
#         price = advert.price
#
#     try:
#
#         setattr(buyer, 'balance', buyer.balance - price)
#         setattr(seller, 'balance', seller.balance + price)
#
#     except Exception:
#         session.rollback()
#         return Error.server_error()
# return '', 204