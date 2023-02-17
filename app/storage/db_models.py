from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Float, Integer, Sequence, Text
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


def DEFAULT_TIME() -> int:
    """Returns the current timestamp

    Returns
    -------
    int
        Value of the current timestamp
    """
    return int(datetime.now(tz=timezone.utc).timestamp())


class MenTshirt(base):
    __tablename__ = "tshirt"

    idx = Column("id", Integer, Sequence("mens_tshirt_id_seq"), primary_key=True)
    status = Column(Integer, nullable=False)
    created_by = Column(Text, nullable=False)
    updated_by = Column(Text, nullable=False)
    created_at = Column(Integer, nullable=False, default=DEFAULT_TIME())
    updated_at = Column(Integer, nullable=False, default=DEFAULT_TIME())
    brand = Column(Text, nullable=False)
    additionalInfo = Column(Text, nullable=False)
    original_price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    review_count = Column(Float, nullable=False)
    out_of_stock = Column(Boolean, nullable=False, default=False)
