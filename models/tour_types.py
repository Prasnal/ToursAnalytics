from sqlalchemy import ForeignKey
from models.connection import Base
from sqlalchemy import String, Column, Integer, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing import List
from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
from models.tours import Tour

intpk = Annotated[int, mapped_column(primary_key=True)]

class TourType(Base):
    __tablename__ = 'tour_type'

    id: Mapped[intpk] = mapped_column(init=False)
    tour_type: Mapped[str] = mapped_column(String(100), nullable=False)

    tours: Mapped[List["Tour"]] = relationship(back_populates="tour_type")

    def __repr__(self) -> str:
        return f"TourType(id={self.id!r}, tour_type={self.tour_type!r})"