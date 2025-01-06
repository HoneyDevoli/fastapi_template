from sqlalchemy import (
    Column,
    Float,
    String,
)

from app.entity.base.db import BaseOrm


class AddressOrm(BaseOrm):
    __tablename__ = "addresses"

    address_1 = Column(String)
    address_2 = Column(String)
    city = Column(String)
    state_province = Column(String)
    country = Column(String)
    postal_code = Column(String)
    timezone = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


