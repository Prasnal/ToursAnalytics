from sqlalchemy_utils import URLType
from models.connection import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated
from sqlalchemy.orm import relationship
from typing import List
from models.tours import Tour

intpk = Annotated[int, mapped_column(primary_key=True)]


class TourAgency(Base):
    __tablename__ = 'tour_agency'
    id: Mapped[intpk] = mapped_column(init=False, primary_key=True)
    agency_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    agency_url: Mapped[str] = mapped_column(URLType, unique=True, nullable=False)

    tours: Mapped[List["Tour"]] = relationship(back_populates="tour_agency")


    def __repr__(self) -> str:
        return f"Agency(id={self.id!r}, agency_name={self.agency_name!r}, agency_url={self.agency_url!r})"
