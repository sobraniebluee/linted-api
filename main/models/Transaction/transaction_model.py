from main.db import db, Base, session
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from main.utils import random_id


class Transaction(Base):
    __tablename__ = 'transactions'

    id = db.Column(db.BIGINT, primary_key=True)
    id_buyer = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'))
    id_seller = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'))
    id_advert = db.Column(UUIDType(binary=False), db.ForeignKey('adverts.id'))
    price = db.Column(db.Float, nullable=False)
    is_finish = db.Column(db.BOOLEAN, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    finish_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    advert = relationship('Advert', backref='transactions', uselist=False)

    def __init__(self, id_buyer, id_seller, id_advert, price):
        self.id = random_id()
        self.id_buyer = id_buyer
        self.id_seller = id_seller
        self.id_advert = id_advert
        self.price = price

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
