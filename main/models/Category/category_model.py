from main.db import db, session, Base


class Category(Base):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    id_category = db.Column(db.Integer, unique=True, primary_key=True)
    id_root = db.Column(db.Integer, nullable=True)
    is_root = db.Column(db.BOOLEAN)
    title = db.Column(db.VARCHAR(64))
    url = db.Column(db.VARCHAR(250), nullable=True)
    has_size = db.Column(db.BOOLEAN)

    def __init__(self, id_category, id_root, is_root, title, url):
        self.id_category = id_category
        self.id_root = id_root
        self.is_root = is_root
        self.title = title
        self.url = url

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

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
