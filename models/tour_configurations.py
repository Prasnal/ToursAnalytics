from sqlalchemy import Integer, Date, Float, Index
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
    tour_length: Mapped[int] = mapped_column(Integer(), nullable=True)
    start_tour_date: Mapped[datetime.datetime] = mapped_column(Date())
    end_tour_date: Mapped[datetime.datetime] = mapped_column(Date())

    tour_id: Mapped[int] = mapped_column(ForeignKey("tour.id"))
    tour: Mapped["Tour"] = relationship(back_populates="tour_config")

    start_location: Mapped[str] = mapped_column(String(100), nullable=True)
    location_additional_cost: Mapped[int] = mapped_column(Float(), nullable=True)

    tour_prices: Mapped[List["TourPrice"]] = relationship(back_populates="tour_config", cascade='all, delete-orphan')

    # scraper_active = Column(Boolean, default=True)

    __table_args__ = (Index('tour_configs_index',
                            "tour_length", "start_tour_date",
                            "start_location", "location_additional_cost", "end_tour_date", "tour_id"),)



    def __repr__(self) -> str:
        return (f"Config(id={self.id!r}, tour_length={self.tour_length!r},"
                f"start_tour_date={self.start_tour_date!r},"
                f"end_tour_date={self.end_tour_date},"
                f" start_location={self.start_location}, additional_costs={self.location_additional_cost})")
