from main.db import Base, session, db
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from config import Const
from main.utils import random_id


class MemberReview(Base):
    __tablename__ = 'reviews'

    id = db.Column(db.BIGINT, primary_key=True)
    id_seller = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'), nullable=False)
    id_buyer = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'), nullable=False)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id'), nullable=False)
    rating = db.Column(db.SMALLINT, nullable=False)
    description = db.Column(db.VARCHAR(Const.MAX_LENGTH_REVIEW), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id_seller, id_buyer, id_advert, rating, description):
        self.id = random_id()
        self.id_buyer = id_buyer
        self.id_seller = id_seller
        self.id_advert = id_advert
        self.rating = rating
        self.description = description

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
