from models.connection import Base
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import Annotated
#from models.countries import Country
from sqlalchemy import Column, Table
from typing import Optional

# FK: tour agency, countries, tour_type,
# tour_type, tour_name, tour_url, klucz_omnibus, tour_id, grade, photos
# TODO: , cascade="all, delete-orphan"

association_table = Table('tours_countries_association',
    Base.metadata,
    Column("tour_id", ForeignKey("tour.id"), primary_key=True),
    Column("country_id", ForeignKey("country.id"), primary_key=True),
)

intpk = Annotated[int, mapped_column(primary_key=True)]


class Tour(Base):
    __tablename__ = 'tour'

    id: Mapped[intpk] = mapped_column(init=False) # TODO: unique
    original_tour_id: Mapped[str] = mapped_column(unique=False, nullable=True) #
    omnibus_key: Mapped[str] = mapped_column(nullable=True)
    #TODO: active, if tour is still in the website with this url, name and original tour id etc.

    tour_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tour_url: Mapped[str] = mapped_column(String(1000))

    tour_photos: Mapped[List["Photos"]] = relationship(back_populates="tour", cascade='all, delete-orphan')

    tour_type_id: Mapped[int] = mapped_column(ForeignKey("tour_type.id"))
    tour_type: Mapped["TourType"] = relationship(back_populates="tours",)

    tour_agency_id: Mapped[int] = mapped_column(ForeignKey("tour_agency.id"))
    tour_agency: Mapped["TourAgency"] = relationship(back_populates="tours")

    tour_config: Mapped[List["TourConfig"]] = relationship(back_populates="tour", cascade='all, delete-orphan')

    countries: Mapped[List["Country"]] = relationship(
        secondary=association_table, back_populates="tours"
    )


    def __repr__(self) -> str:
        return (f"Tour(id={self.id!r}, original_tour_id={self.original_tour_id!r}, omnibus_key={self.omnibus_key!r}, "
                f"tour_name={self.tour_name!r}, tour_type={self.tour_type.tour_type})")