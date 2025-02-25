import random
import string

from sqlalchemy import (
    BigInteger,
    Column,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

from app.entity.address.db import AddressOrm
from app.entity.base.db import BaseOrm


class OrderOrm(BaseOrm):
    __tablename__ = 'orders'

    order_number = Column(String, default=lambda: ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
    name = Column(String)
    price = Column(Float)
    pickup_id = Column(BigInteger, ForeignKey('addresses.id'))
    dropoff_id = Column(BigInteger, ForeignKey('addresses.id'))

    pickup_address = relationship(AddressOrm, foreign_keys='OrderOrm.pickup_id', lazy='joined', cascade='all,delete')
    dropoff_address = relationship(AddressOrm, foreign_keys='OrderOrm.dropoff_id', lazy='joined', cascade='all,delete')
