from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from connection import Base
from sqlalchemy import String, Column, Table, Integer, Sequence



class Country(Base):
   __tablename__ = 'countries'
   id = Column(Integer,Sequence('user_seq'), primary_key=True)
   country_name = Column(String(50))
   country_code = Column(String(3), unique=True, nullable=False)

   def __init__(self, country_name, country_code):
      self.country_name = country_name
      self.country_code = country_code
