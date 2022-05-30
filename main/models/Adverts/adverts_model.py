from main.db import Base, session, db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType


class Advert(Base):
    __tablename__ = 'adverts'

    id = db.Column(UUIDType(binary=False), primary_key=True)
    id_user = db.Column(UUIDType(binary=False), db.ForeignKey('users.id', ondelete="CASCADE", onupdate="CASCADE"))
    rating = db.Column(db.Integer, nullable=True)
    ban = db.Column(db.BOOLEAN, default=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    advert_info = relationship('AdvertInfo', backref='adverts')
    advert_images = relationship('AdvertImage', backref="adverts")


class AdvertInfo(Base):
    __tablename__ = 'adverts_info'

    id = db.Column(db.Integer, primary_key=True)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id', ondelete="CASCADE", onupdate="CASCADE"))
    title = db.Column(db.VARCHAR(64), nullable=False)
    description = db.Column(db.VARCHAR(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Integer, db.ForeignKey('adverts_condition.id'), nullable=False)
    brand = db.Column(db.VARCHAR(64), nullable=False)
    watches = db.Column(db.Integer, nullable=False, default=0)
    likes = db.Column(db.Integer, nullable=False, default=0)


class AdvertImage(Base):
    __tablename__ = 'adverts_image'

    id = db.Column(db.Integer, primary_key=True)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id', ondelete="CASCADE", onupdate="CASCADE"))
    path_image = db.Column(db.VARCHAR(500), nullable=True)
    size = db.Column(db.BIGINT, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class AdvertCondition(Base):
    __tablename__ = 'adverts_condition'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(32), nullable=False)
    description = db.Column(db.VARCHAR(250), nullable=False)

    def __init__(self, id_cond, name, description):
        self.id = id_cond
        self.name = name
        self.description = description

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            raise
