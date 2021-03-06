from typing import List

from pydantic import BaseModel
from uuid import UUID
from datetime import date

from .cargo_type import CargoType

from models.cargo import Cargo as CargoModel


class CargoIn(BaseModel):
    cargo_type: CargoType
    date_supplied: date
    price: float


class Cargo(CargoIn):
    id: UUID
    insurance_price: float

    @staticmethod
    async def from_model(model: CargoModel) -> 'Cargo':
        """ Я не смог победить tortoise с его pydantic_model_creator
            поэтому сделал свой сериализатор в dict, который потом
            pydantic уже может проверить """
        return Cargo(id=model.id, cargo_type=model.cargo_type.name,
                     date_supplied=model.date_supplied, price=model.price,
                     insurance_price=model.insurance_price)


class CargoList(BaseModel):
    __root__: List[Cargo]
