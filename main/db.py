import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config import DB

engine = create_engine(DB, echo=False)
session = scoped_session(sessionmaker(autoflush=False, autocommit=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()


def create_metadata():
    Base.metadata.create_all(bind=engine)
