
from app.entity.address.v1.schema import AddressSchema
from app.entity.base.schema import BaseSchema
from app.entity.order.db import OrderOrm


class OrderIn(BaseSchema):
    __orm__ = OrderOrm

    name: str | None
    price: float
    pickup_address: AddressSchema | None
    dropoff_address: AddressSchema | None


class OrderOut(OrderIn):
    model_config = {
        "from_attributes": True,  # Включаем поддержку объектов ORM
    }

    order_number: str | None
