from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from connection import Base
from sqlalchemy import String, Column, Table, Boolean, Integer, Sequence, Date



class TourConfig(Base):
   __tablename__ = 'tour_configuration'
   id = Column(Integer,Sequence('user_seq'), primary_key=True)
   start_date = Column(Date())
   end_date = Column(Date())
   start_location = Column(String(50))
   tour_length = Column(Integer)
   scraper_active = Column(Boolean, default=True)


   #TourID [foregin key]
   #TourPrices [foregin key]


   def __init__(self, start_date, end_date, start_location, tour_length, scraper_active):
       self.start_date = start_date
       self.end_date = end_date
       self.start_location = start_location
       self.tour_lenght = tour_length
       self.scraper_active = scraper_active #TODO: ???

