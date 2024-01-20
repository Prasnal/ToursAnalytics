# Todays datetime
# TourConfig
# TourPrice
# approved?

#grade


from sqlalchemy import String, Column, Table, Boolean, Integer, Sequence, Date, Float
from models.connection import Base
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import Annotated
import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]


class TourPrice(Base):
    __tablename__ = 'tour_price'
    id: Mapped[intpk] = mapped_column(init=False)
    scraped_date: Mapped[datetime.datetime] = mapped_column(Date(), nullable=False)
    tour_approved: Mapped[Boolean] = mapped_column(Boolean(), nullable=False)
    tour_price: Mapped[Float] = mapped_column(Float(), nullable=False)

    tour_config_id: Mapped[int] = mapped_column(ForeignKey("tour_config.id"))
    tour_config: Mapped["TourConfig"] = relationship(back_populates="tour_prices")