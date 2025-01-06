from __future__ import annotations

from pydantic import constr

from app.entity.address.db import AddressOrm
from app.entity.base.schema import BaseSchema


class AddressSchema(BaseSchema):
    __orm__ = AddressOrm

    model_config = {
        'from_attributes': True,
    }

    address_1: str | None = None
    address_2: str | None = None
    city: str | None
    state_province: str | None
    country: str | None
    postal_code: constr(min_length=5, max_length=10)
    timezone: str | None
    latitude: float
    longitude: float
