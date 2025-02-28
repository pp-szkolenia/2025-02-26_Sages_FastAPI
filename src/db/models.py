from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import false
from db.orm import Base
from db.orm import Session


class User(Base):
    __tablename__ = 'users'

    id_number = Column("id", Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(60), nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default=false())

    @classmethod
    def find_all(cls):
        with Session() as session:
            return session.query(User).all()
