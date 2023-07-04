from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
from db_api.base import Base


class Users(Base):
    __tablename__ = 'user'

    user_id = Column(BigInteger, primary_key=True)
    time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    type = Column(String, default='active')
    recommend = Column(String, default='[]')
    offset = Column(Integer, default=1)

