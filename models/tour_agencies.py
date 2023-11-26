from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from connection import Base
from sqlalchemy import String, Column, Table, Integer, Sequence


class TourAgency(Base):
   __tablename__ = 'tour_agencies'
   id = Column(Integer,Sequence('user_seq'), primary_key=True)
   name = Column(String(50), unique=True)
   url = Column(String(250))

   def __init__(self, name, url):
      self.name = name
      self.url = url
