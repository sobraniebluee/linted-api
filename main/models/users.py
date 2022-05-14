from passlib.hash import bcrypt
from main.db import db, session, Base
from sqlalchemy.orm import relationship
from main.utils import hash_password, _error_response
import time
import datetime
from flask_jwt_extended import create_access_token


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.BIGINT, nullable=False)
    ip = db.Column(db.String(24), nullable=False)
    avatar = relationship('UserAvatar', backref='users')

    def __init__(self, **kwargs):
        self.username = f"@{kwargs.get('username')}"
        self.email = kwargs.get('email'),
        self.password = hash_password(kwargs.get('password'))
        self.ip = kwargs.get('ip')
        self.created_at = int(time.time())

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def get_access_token(self, expire=24):
        time_expire = datetime.timedelta(expire)

        token = create_access_token(
            identity=self.id,
            expires_delta=time_expire
        )
        return token

    @classmethod
    def auth(cls, password, email=None, username=None):
        if username:
            user = cls.query.filter(cls.username == f'@{username}').first()
            if not user:
                raise Exception(_error_response('username', 'Please fill username'))
            if not bcrypt.verify(password, user.password):
                raise Exception(_error_response('password', 'Password wrong!'))
            return user
        if email:
            user = cls.query.filter(cls.email == email).first()
            if not user:
                raise Exception(dict(_error_response('username', 'Please fill username')))
            if not bcrypt.verify(password, user.password):
                raise Exception(_error_response('password', 'Password wrong!'))
            return user


class UserAvatar(Base):
    __tablename__ = 'avatars'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    path = db.Column(db.String(250), nullable=False)

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise
