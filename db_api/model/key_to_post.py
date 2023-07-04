from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Float
from db_api.base import Base


class PostIndex(Base):
    __tablename__ = 'post_index'

    id = Column(BigInteger, primary_key=True)
    msg_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, primary_key=True)
    username = Column(String)
