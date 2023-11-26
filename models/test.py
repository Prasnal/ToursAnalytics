from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from connection import Base
from sqlalchemy import String, Column, Table, Integer, Sequence



class User(Base):
   __tablename__ = 'users'
   id = Column(Integer,Sequence('user_seq'), primary_key=True)
   username = Column(String(50), unique=True)
   fullname = Column(String(150))
   password = Column(String(50))
   def __init__(self, name, fullname, password):
      self.username = name
      self.fullname = fullname
      self.password = password

