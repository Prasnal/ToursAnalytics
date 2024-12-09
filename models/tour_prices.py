# Todays datetime
# TourConfig
# TourPrice
# approved?

#grade


from sqlalchemy import String, Column, Table, Boolean, Integer, Sequence, Date, Float, Time
from models.connection import Base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import Annotated
import datetime
from sqlalchemy import Index

intpk = Annotated[int, mapped_column(primary_key=True)]


class TourPrice(Base):
    __tablename__ = 'tour_price'
    __table_args__ = (
        Index('idx_tour_price_query',
              'scraped_time',
              'scraped_date',
              'tour_config_id',
              'tour_price',
              'tour_price_pp',
              'tour_approved',
              ),
    )
    id: Mapped[intpk] = mapped_column(init=False)
    scraped_date: Mapped[datetime.datetime] = mapped_column(Date(), nullable=False)
    scraped_time: Mapped[datetime.datetime] = mapped_column(Time(), nullable=True)
    tour_approved: Mapped[Boolean] = mapped_column(Boolean(), nullable=False)
    tour_price: Mapped[Float] = mapped_column(Float(), nullable=False)
    tour_price_pp: Mapped[Float] = mapped_column(Float(), nullable=False)

    tour_config_id: Mapped[int] = mapped_column(ForeignKey("tour_config.id"))
    tour_config: Mapped["TourConfig"] = relationship(back_populates="tour_prices")

    def __repr__(self) -> str:
        return f"Prices(id={self.id!r}, scraped_date={self.scraped_date!r}, tour_approved={self.tour_approved!r}, tour_price={self.tour_price!r}, tour_config={self.tour_config!r})"