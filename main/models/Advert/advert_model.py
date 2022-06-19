from main.db import Base, session, db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
import uuid
from main.utils import random_url


class Advert(Base):
    __tablename__ = 'adverts'

    id = db.Column(UUIDType(binary=False), primary_key=True)
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"))
    url = db.Column(db.VARCHAR(32), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    is_ban = db.Column(db.BOOLEAN, default=False)
    is_bought = db.Column(db.BOOLEAN, default=False)
    is_fill = db.Column(db.BOOLEAN, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    watches = relationship('AdvertWatches', backref="adverts", uselist=True)
    likes = relationship('AdvertLikes', backref="adverts", uselist=True)
    info = relationship('AdvertInfo', backref='adverts', uselist=False)
    images = relationship('AdvertImage', backref='adverts', uselist=True)
    user = relationship('User', backref='adverts', uselist=False)

    def __init__(self, id_user):
        self.is_liked = None
        self.id = uuid.uuid4()
        self.id_user = id_user
        self.rating = 0
        self.is_ban = False
        self.is_bought = False
        self.is_fill = True
        self.url = random_url()

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def check_is_liked(self, id_user=None):
        if not id_user:
            self.is_liked = False
        else:
            is_liked = AdvertLikes.query.filter(AdvertLikes.id_advert == self.id, AdvertLikes.id_user == id_user).first()
            if is_liked:
                self.is_liked = True
            else:
                self.is_liked = False
        return self


class AdvertInfo(Base):
    __tablename__ = 'adverts_info'

    id = db.Column(db.Integer, primary_key=True)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id', ondelete="CASCADE", onupdate="CASCADE"))
    title = db.Column(db.VARCHAR(64), nullable=False)
    description = db.Column(db.VARCHAR(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('adverts_condition.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=True)
    size = relationship('Size', backref="adverts_info")
    condition = relationship('AdvertCondition', backref="adverts_info")
    category = relationship('Category', backref="adverts_info")

    def __init__(self, id_advert, title, description, price, category_id, condition_id, size_id):
        self.id_advert = id_advert
        self.title = title
        self.description = description
        self.price = price
        self.condition_id = condition_id
        self.size_id = size_id
        self.category_id = category_id

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise


class AdvertImage(Base):
    __tablename__ = 'adverts_image'

    id = db.Column(UUIDType(binary=False), primary_key=True)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    is_preview = db.Column(db.BOOLEAN)
    id_image = db.Column(UUIDType(binary=False), db.ForeignKey('files.id',  ondelete='CASCADE', onupdate='CASCADE'))
    image = relationship('File', backref='adverts_image', uselist=False)

    def __init__(self, id_advert, is_preview, id_image):
        self.id = uuid.uuid4()
        self.id_advert = id_advert
        self.is_preview = is_preview
        self.id_image = id_image

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class AdvertCondition(Base):
    __tablename__ = 'adverts_condition'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(32), nullable=False)
    description = db.Column(db.VARCHAR(250), nullable=False)

    def __init__(self, id_cond, title, description):
        self.id = id_cond
        self.title = title
        self.description = description

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            raise


class AdvertLikes(Base):
    __tablename__ = 'adverts_likes'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE"))
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id', ondelete="CASCADE"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, id_user, id_advert):
        self.id_user = id_user
        self.id_advert = id_advert

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class AdvertWatches(Base):
    __tablename__ = 'advert_watches'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id', ondelete="CASCADE"))
    ip_user = db.Column(db.VARCHAR(32), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, id_user, ip_user, id_advert):
        self.id_user = id_user
        self.ip_user = ip_user
        self.id_advert = id_advert

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def commit(cls):
        try:
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise



