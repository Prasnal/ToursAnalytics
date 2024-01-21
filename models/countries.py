from models.connection import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated
from sqlalchemy.orm import relationship
from typing import List
from models.tours import association_table
from typing import Optional

intpk = Annotated[int, mapped_column(primary_key=True)]


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[intpk] = mapped_column(init=False, primary_key=True)
    country_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    country_code: Mapped[str] = mapped_column(unique=True, nullable=True)

    tours: Mapped[List["Tour"]] = relationship(
        secondary=association_table, back_populates="countries")

    def __repr__(self) -> str:
        return f"Country(id={self.id!r}, country_name={self.country_name!r}, country_code={self.country_code!r})"
