from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy import text

db_user = "tours_user"
db_pass = "Tours123"
db_addr = "localhost:5432"
db_name = "testdb"
url = f"postgresql://{db_user}:{db_pass}@{db_addr}/{db_name}"

class Base(MappedAsDataclass, DeclarativeBase):
    pass


engine = create_engine(url, echo=False)
Session = sessionmaker(engine)


if not database_exists(engine.url):
    create_database(engine.url)
else:
    conn = engine.connect()





