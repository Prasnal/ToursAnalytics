from sqlalchemy import ForeignKey
from connection import Base
from sqlalchemy import String, Column, Integer, Sequence


class TourTypes(Base):
   __tablename__ = 'tour_types'
   id = Column(Integer,Sequence('user_seq'), primary_key=True)
   tour_type = Column(String(50), nullable=False)


   #Tours [foregin key]


   def __init__(self, tour_type):
       self.tour_type = tour_type
