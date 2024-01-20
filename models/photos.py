from sqlalchemy import ForeignKey
from models.connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing_extensions import Annotated
from sqlalchemy.orm import mapped_column
from models.tours import Tour
from sqlalchemy_utils import URLType


intpk = Annotated[int, mapped_column(primary_key=True)]

class Photos(Base):
    __tablename__ = 'photos'

    id: Mapped[intpk] = mapped_column(init=False, primary_key=True)
    photo_url: Mapped[str] = mapped_column(URLType, unique=True, nullable=False)

    tour_id: Mapped[int] = mapped_column(ForeignKey("tour.id"))
    tour: Mapped["Tour"] = relationship(back_populates="tour_photos")

    # TODO: original_tour_id? omnibus_key?

    def __repr__(self) -> str:
        return f"Photo(id={self.id!r}, url={self.photo_url!r}), tour={self.tour_id!r})"