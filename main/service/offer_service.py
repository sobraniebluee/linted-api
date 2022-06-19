from main.models.Advert.advert_model import Advert, AdvertInfo, session
from main.models.Offer.offer_model import Offer
from main.models.User.user_model import User
from main.middleware.error import Error
from config import Const
import datetime

SELLER = 'seller'
BUYER = 'buyer'


def reqeust_offer_service(id_buyer, id_advert, price):
    advert = Advert.query.filter(Advert.id == id_advert).first()
    if not advert or advert.is_bought:
        return Error.server_error()
    buyer = User.query.filter(User.id == id_buyer).first()
    seller = User.query.filter(User.id == advert.id_user).first()
    if not buyer or not seller or str(seller.id) == str(buyer.id):
        return Error.server_error()
    if price >= advert.info.price:
        return Error.error_default(msg="Please enter price offer less than price product", status_code=400)
    min_offer_price = advert.info.price * Const.OFFER_PRICE_PERCENT
    if min_offer_price > price:
        return Error.error_default(msg=f"Price must equal or more than {min_offer_price}", status_code=400)
    buyer_offers = Offer.query.filter(Offer.id_buyer == id_buyer).all()
    buyer_offers_today = 0
    for item in buyer_offers:
        today = datetime.datetime.date(datetime.datetime.now())
        if today == item.created_at.date():
            buyer_offers_today += 1
    if buyer_offers_today >= Const.MAX_COUNT_OFFERS_PER_DAY:
        return Error.error_default(
            msg=f"Sorry, per day you can sent only {Const.MAX_COUNT_OFFERS_PER_DAY} offers",
            status_code=400)
    # prev_offers = Offer.query.filter(Offer.id_buyer == id_buyer, Offer.id_advert == Advert.id, Offer.from_who == BUYER).all()
    # for prev_offer in prev_offers:
    #     setattr(prev_offer, 'is_accepted', False)
    #     prev_offer.commit()
    new_offer = Offer(buyer.id, advert.id, price, None, BUYER)
    new_offer.save()
    return new_offer, 200


def accept_offer_service(id_offer, is_accept, user_id):
    offer = Offer.query.filter(Offer.id == id_offer).first()
    if not offer:
        return Error.server_error()
    if type(offer.is_accepted) is bool:
        msg = "accepted" if offer.is_accepted else "not accepted"
        return Error.error_default(msg=f"This offer already {msg}", status_code=400)
    advert = Advert.query.filter(Advert.id_user == user_id, Advert.id == offer.id_advert).first()
    if not advert:
        return Error.server_error()
    prev_offers = Offer.query.filter(Offer.id_buyer == offer.id_buyer, Offer.id_advert == advert.id).all()
    for prev_offer in prev_offers:
        setattr(prev_offer, 'is_accepted', False)
        prev_offer.commit()
    setattr(offer, 'is_accepted', is_accept)
    offer.commit()
    return offer, 200


def send_offer_service(seller_id, id_buyer, id_advert, price):
    advert = Advert.query.filter(Advert.id == id_advert).first()
    advert_price = advert.info.price
    if not advert or advert.is_bought:
        return Error.server_error()

    if not str(advert.id_user) == str(seller_id):
        return Error.server_error(msg="ddd")
    if price >= advert_price:
        return Error.error_default(msg="Please enter price offer less than price product", status_code=400)
    min_offer_price = advert_price * Const.OFFER_PRICE_PERCENT
    if min_offer_price > price:
        return Error.error_default(msg=f"Price must equal or more than {min_offer_price}", status_code=400)
    buyer_id, = session.query(User.id).filter(User.id == id_buyer).first()
    if not buyer_id or seller_id == buyer_id:
        return Error.server_error()
    prev_offers = Offer.query.filter(Offer.id_buyer == buyer_id, Offer.id_advert == advert.id).all()
    for prev_offer in prev_offers:
        setattr(prev_offer, 'is_accepted', False)
        prev_offer.commit()
    new_offer = Offer(buyer_id, advert.id, price, True, SELLER)
    new_offer.save()
    return new_offer, 200

