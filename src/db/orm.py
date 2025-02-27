from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from db.utils import get_connection_string


connection_string = get_connection_string()
engine = create_engine(connection_string)
Base = declarative_base()

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
