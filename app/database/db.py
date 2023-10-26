from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from . import DB_URI

engine = create_engine(DB_URI)


def init_db(base):
    '''Creates the database tables'''
    base.metadata.create_all(engine)


def session():
    '''
    Creates a new SQLAlchemy session.

    Returns:
    session (sqlalchemy.orm.Session): A new SQLAlchemy session.
    '''
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session_factory = scoped_session(Session)
    session = session_factory()
    return session
