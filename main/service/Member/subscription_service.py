from main.models.MemberSubscription.member_subscription_model import MemberSubscription, session
from main.models.User.user_model import User
from main.middleware.error import Error
from config import Const


def toggle_subscription_service(id_follower, type_toggle, id_leader):
    leader_id = session.query(User.id).filter(User.id == id_leader).first()
    follower_id = session.query(User.id).filter(User.id == id_follower).first()
    if not leader_id or not follower_id:
        return Error.server_error()
    leader_id, = leader_id
    follower_id, = follower_id
    is_have_subscription = MemberSubscription.query.filter(
        MemberSubscription.id_follower == follower_id,
        MemberSubscription.id_leader == leader_id).first()
    if type_toggle == Const.FOLLOW:
        if is_have_subscription:
            return Error.error_default(msg='You already follow this user', status_code=400)
        try:
            subscription = MemberSubscription(id_leader, id_follower)
            subscription.save()
            return '', 204
        except Exception:
            return Error.server_error()
    if type_toggle == Const.UNFOLLOW:
        if not is_have_subscription:
            return Error.server_error()
        try:
            is_have_subscription.delete()
            return '', 204
        except Exception:
            return Error.server_error()

