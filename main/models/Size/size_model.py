from main.db import db, session, Base


class Size(Base):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'))
    title = db.Column(db.VARCHAR(20))

    def __init__(self, id_category, title):
        self.id_category = id_category
        self.title = title

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


