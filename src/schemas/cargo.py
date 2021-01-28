from typing import List

from pydantic import BaseModel
from uuid import UUID
from datetime import date

from .cargo_type import CargoType

from models.cargo import Cargo as CargoModel

import tortoise


class CargoIn(BaseModel):
    cargo_type: CargoType
    date_supplied: date
    price: float


class Cargo(CargoIn):
    id: UUID
    insurance_price: float

    @staticmethod
    async def from_model(model: CargoModel) -> 'Cargo':
        if isinstance(model.cargo_type, tortoise.queryset.QuerySet):
            cargo_type = await model.cargo_type.first()
        else:
            cargo_type = model.cargo_type
        return Cargo(id=model.id, cargo_type=cargo_type.name,
                     date_supplied=model.date_supplied, price=model.price,
                     insurance_price=model.insurance_price)


class CargoList(BaseModel):
    __root__: List[Cargo]
