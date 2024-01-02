from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base


db_user = "tours_user"
db_pass = "Tours123"
db_addr = "localhost:5432"
db_name = "testdb"
url = f"postgresql://{db_user}:{db_pass}@{db_addr}/{db_name}"

engine = create_engine(url, echo=True)
Base = declarative_base()


if not database_exists(engine.url):
    create_database(engine.url)
else:
    engine.connect()

