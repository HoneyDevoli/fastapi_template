from typing import Optional

from app.entity.address.schema import AddressSchema
from app.entity.base.schema import BaseSchema
from app.entity.order.db import OrderOrm


class OrderIn(BaseSchema):
    __orm__ = OrderOrm

    name: Optional[str]
    price: float
    pickup_address: Optional[AddressSchema]
    dropoff_address: Optional[AddressSchema]


class OrderOut(OrderIn):
    model_config = {
        "from_attributes": True,  # Включаем поддержку объектов ORM
    }

    order_number: Optional[str]
