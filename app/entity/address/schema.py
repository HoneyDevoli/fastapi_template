from __future__ import annotations

from typing import Optional

from pydantic import constr

from app.entity.address.db import AddressOrm
from app.entity.base.schema import BaseSchema


class AddressSchema(BaseSchema):
    __orm__ = AddressOrm

    model_config = {
        "from_attributes": True,
    }

    address_1: str | None = None
    address_2: str | None = None
    city: Optional[str]
    state_province: Optional[str]
    country: Optional[str]
    postal_code: constr(min_length=5, max_length=10)
    timezone: Optional[str]
    latitude: float
    longitude: float
