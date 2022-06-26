from main.models.User.user_model import UserTokens,func
import jwt
from config import Config


def jwt_tokens(user_id):
    item = UserTokens.query.filter(UserTokens.user_id == user_id).first()
    if item is not None:
        access = item.get_access_token(item.user_id)
        refresh = item.get_refresh_token(item.user_id)
        setattr(item, 'access_token', access)
        setattr(item, 'refresh_token', refresh)
        item.commit()
        return {
            "access_token": access,
            "refresh_token": refresh
        }
    else:
        new_item = UserTokens(user_id=user_id)
        new_item.save()
        return {
            "access_token": new_item.access_token,
            "refresh_token": new_item.refresh_token
        }


def is_revoked_token_service(identity, jwt_header, jwt_payload):
    try:
        token_encode = jwt.encode(jwt_payload, Config.JWT_SECRET_KEY, algorithm=jwt_header['alg'])
        token = UserTokens.query.filter(UserTokens.user_id == identity).scalar()
        if not token:
            return True
        if token_encode == token.access_token or token_encode == token.refresh_token:
            return False
        return True
    except Exception:
        raise


