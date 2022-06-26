from passlib.hash import bcrypt
from main.db import db, session, Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from main.utils import hash_password, _error_response
from sqlalchemy.sql import func
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
import uuid


class User(Base):
    __tablename__ = 'users'

    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())
    username = db.Column(db.VARCHAR(length=64), nullable=False, unique=True)
    email = db.Column(db.VARCHAR(length=64), nullable=False, unique=True)
    password = db.Column(db.VARCHAR(length=250), nullable=False)
    verified = db.Column(db.BOOLEAN, default=False, nullable=False)
    balance = db.Column(db.Float, default=100, nullable=False)
    avatar = relationship('UserAvatar', backref='users', uselist=False)
    additional_info = relationship('UserAdditionalInfo', uselist=False, backref='users', lazy='joined')
    tokens = relationship('UserTokens', uselist=False, backref='users')

    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        self.username = f"@{kwargs.get('username')}"
        self.email = kwargs.get('email'),
        self.password = hash_password(kwargs.get('password'))
        self.balance = 1000

    def save(self):
        session.add(self)
        session.commit()

    @classmethod
    def auth(cls, password, email=None, username=None):
        if username:
            user = cls.query.filter(cls.username == f'@{username}').first()
            if not user:
                return {'auth': False, 'error': _error_response('username', 'Sorry,this username not found!')}
            if not bcrypt.verify(password, user.password):
                return {'auth': False, 'error': _error_response('password', 'Sorry,this password wrong!')}
            return {'auth': True, 'data': user}
        if email:
            user = cls.query.filter(cls.email == email).first()
            if not user:
                return {'auth': False, 'error': _error_response('email', 'Sorry,this email not found!')}
            if not bcrypt.verify(password, user.password):
                return {'auth': False, 'error': _error_response('password', 'Password wrong!')}
            return {'auth': True, 'data': user}

    def commit(self):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


class UserAdditionalInfo(Base):
    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    is_fill = db.Column(db.BOOLEAN, default=False)
    id_user = db.Column(UUIDType(binary=False),
                        db.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    first_name = db.Column(db.VARCHAR(length=64), nullable=True)
    second_name = db.Column(db.VARCHAR(length=64), nullable=True)
    phone_number = db.Column(db.VARCHAR(length=20), nullable=True)
    sex = db.Column(db.VARCHAR(length=12), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=(func.now()))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=(func.now()))
    ip = db.Column(db.String(24), nullable=False)

    def __init__(self, ip_user, **kwargs):
        self.id_user = kwargs.get('id_user')
        self.first_name = kwargs.get('first_name', None)
        self.second_name = kwargs.get('second_name', None)
        self.phone_number = kwargs.get('phone_number', None)
        self.ip = ip_user

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def commit(self):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


class UserTokens(Base):
    __tablename__ = 'user_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete='CASCADE'))
    access_token = db.Column(db.VARCHAR(500), nullable=False)
    refresh_token = db.Column(db.VARCHAR(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=(func.now()))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=(func.now()))

    def __init__(self, user_id):
        self.user_id = user_id
        self.access_token = self.get_access_token(identity=user_id)
        self.refresh_token = self.get_refresh_token(identity=user_id)

    @classmethod
    def get_access_token(cls, identity):
        return create_access_token(identity=identity)

    @classmethod
    def get_refresh_token(cls, identity):
        return create_refresh_token(identity=identity)

    def commit(self):
        session.commit()

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def remove(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class UserAvatar(Base):
    __tablename__ = 'avatars'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"))
    full_avatar_path = db.Column(db.VARCHAR(length=500), nullable=True)
    mini_avatar_path = db.Column(db.VARCHAR(length=500), nullable=True)
    name = db.Column(db.VARCHAR(length=500), nullable=True)
    size = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=(func.now()))
    update_at = db.Column(db.DateTime(timezone=True), onupdate=(func.now()))

    def __init__(self, user_id, path):
        self.id_user = user_id
        self.mini_avatar_path = path

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        session.commit()


