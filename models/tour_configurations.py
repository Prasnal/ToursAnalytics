
from sqlalchemy import String, Column, Table, Boolean, Integer, Sequence, Date, Float
from models.connection import Base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import Annotated
import datetime
from typing import List

intpk = Annotated[int, mapped_column(primary_key=True)]


class TourConfig(Base):
    __tablename__ = 'tour_config'
    id: Mapped[intpk] = mapped_column(init=False)
    tour_length: Mapped[int] = mapped_column(Integer())
    start_tour_date: Mapped[datetime.datetime] = mapped_column(Date())
    end_tour_date: Mapped[datetime.datetime] = mapped_column(Date())

    tour_id: Mapped[int] = mapped_column(ForeignKey("tour.id"))
    tour: Mapped["Tour"] = relationship(back_populates="tour_config")

    start_location: Mapped[str] = mapped_column(String(100), nullable=True)
    location_additional_cost: Mapped[int] = mapped_column(Float(), nullable=True)

    tour_prices: Mapped[List["TourPrice"]] = relationship(back_populates="tour_config")

    # scraper_active = Column(Boolean, default=True)
