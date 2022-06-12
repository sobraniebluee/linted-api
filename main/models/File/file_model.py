from main.db import db, session, Base
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from uuid import uuid4


class File(Base):
    __tablename__ = 'files'

    id = db.Column(UUIDType(binary=False), primary_key=True)
    id_user = db.Column(UUIDType(binary=False), nullable=False)
    type = db.Column(db.VARCHAR(12), nullable=False)
    path = db.Column(db.VARCHAR(300), nullable=False)
    size = db.Column(db.BIGINT, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, id_user, type_file, path, size):
        self.id = uuid4()
        self.id_user = id_user
        self.type = type_file
        self.path = path
        self.size = size

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
