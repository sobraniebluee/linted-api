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
    buyer_id, buyer_balance = session.query(User.id, User.balance).filter(User.id == id_user).first()
    seller_id, = session.query(User.id).filter(User.id == advert.id_user).first()

    if not buyer_id or not seller_id:
        return Error.server_error()

    offer = session.query(Offer.price).filter(Offer.id_advert == advert.id,
                                              Offer.id_buyer == buyer_id,
                                              Offer.is_accepted == True).first()
    if offer:
        # got price from tuple
        price, = offer
    else:
        price = advert.info.price

    if buyer_balance < price:
        return Error.error_default(msg="Sorry,please top up your balance!", status_code=400)
    try:
        transaction = Transaction.query.filter(Transaction.id_buyer == buyer_id,
                                               Transaction.id_advert == advert.id).first()
        if transaction:
            setattr(transaction, 'price', price)
            transaction.commit()
        else:
            transaction = Transaction(buyer_id, seller_id, advert.id, price)
            transaction.save()
    except Exception:
        return Error.server_error(msg="Something went wrong")
    return transaction, 200


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

