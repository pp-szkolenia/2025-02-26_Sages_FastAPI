from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from db.utils import get_connection_string


connection_string = get_connection_string()
engine = create_engine(connection_string)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
