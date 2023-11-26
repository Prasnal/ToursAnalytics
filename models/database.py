from connection import engine, Base
from sqlalchemy.orm import Session
from test import User

Base.metadata.create_all(engine)



with Session(engine) as session:
    test_table = User('ed2', 'Ed Jones', 'edspassword')
    session.add_all([test_table])
    session.commit()
