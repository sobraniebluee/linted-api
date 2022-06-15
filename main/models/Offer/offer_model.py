from main.db import db, Base, session
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func


class Offer(Base):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id'))
    id_buyer = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'))
    price = db.Column(db.Float, nullable=False)
    is_accepted = db.Column(db.BOOLEAN, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    update_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id_buyer, id_advert, price, is_accepted):
        self.id_buyer = id_buyer
        self.id_advert = id_advert
        self.price = price
        self.is_accepted = is_accepted

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
