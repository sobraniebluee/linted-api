from main.db import Base, db, session
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class MemberSubscription(Base):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    id_leader = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'))
    id_follower = db.Column(UUIDType(binary=False), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, id_leader, id_follower):
        if id_leader == id_follower:
            raise
        self.id_leader = id_leader
        self.id_follower = id_follower

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