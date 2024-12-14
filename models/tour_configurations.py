
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
from sqlalchemy import Index, UniqueConstraint

intpk = Annotated[int, mapped_column(primary_key=True)]

'''
SELECT tour_config.id, tour_config.tour_length, tour_config.start_tour_date, tour_config.end_tour_date, tour_config.tour_id, tour_config.start_location, tour_config.location_additional_cost 
FROM tour_config 
WHERE tour_config.tour_length = 13 AND tour_config.start_location IS NULL AND tour_config.location_additional_cost IS NULL AND tour_config.start_tour_date = '2025-04-07' AND tour_config.end_tour_date = '2025-04-19' AND 1 = tour_config.tour_id AND tour_config.tour_id = 1

'''

class TourConfig(Base):
    __tablename__ = 'tour_config'

    __table_args__ = (
        UniqueConstraint(
            'start_tour_date', 'end_tour_date', 'tour_id', 'tour_length',
            name='uq_tour_config_dates_tour'
        ),
        Index(
            'idx_tour_config_query',
            'start_tour_date',
            'end_tour_date',
            'tour_id',
            'tour_length',
            'start_location',
            'location_additional_cost'
        ),
    )
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

    def __repr__(self) -> str:
        return (f"Config(id={self.id!r}, tour_length={self.tour_length!r},"
                f"start_tour_date={self.start_tour_date!r},"
                f"end_tour_date={self.end_tour_date},"
                f" start_location={self.start_location}, additional_costs={self.location_additional_cost})")
