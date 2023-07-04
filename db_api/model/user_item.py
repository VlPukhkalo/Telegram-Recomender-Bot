from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Float
from db_api.base import Base


class UsersItem(Base):
    __tablename__ = 'user_item'

    user_id = Column(BigInteger, primary_key=True)
    item_id = Column(BigInteger, primary_key=True)
    rating = Column(Integer)
    time = Column(DateTime)
