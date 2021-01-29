from typing import List

from pydantic import BaseModel
from uuid import UUID
from datetime import date

from .cargo_type import CargoType

from models.tariff import Tariff as TariffModel


class TariffIn(BaseModel):
    cargo_type: CargoType
    date: date
    rate: float


class Tariff(TariffIn):
    id: UUID

    @staticmethod
    async def from_model(model: TariffModel) -> 'Tariff':
        """ Я не смог победить tortoise с его pydantic_model_creator
            поэтому сделал свой сериализатор в dict, который потом
            pydantic уже может проверить """
        return Tariff(id=model.id, cargo_type=model.cargo_type.name,
                      date=model.date, rate=model.rate)


class TariffList(BaseModel):
    __root__: List[Tariff]
