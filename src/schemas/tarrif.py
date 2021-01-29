from typing import List

from pydantic import BaseModel
from uuid import UUID
from datetime import date

from .cargo_type import CargoType

from models.tarrif import Tarrif as TarrifModel


class TarrifIn(BaseModel):
    cargo_type: CargoType
    date: date
    rate: float


class Tarrif(TarrifIn):
    id: UUID

    @staticmethod
    async def from_model(model: TarrifModel) -> 'Tarrif':
        """ Я не смог победить tortoise с его pydantic_model_creator
            поэтому сделал свой сериализатор в dict, который потом
            pydantic уже может проверить """
        return Tarrif(id=model.id, cargo_type=model.cargo_type.name,
                      date=model.date, rate=model.rate)


class TarrifList(BaseModel):
    __root__: List[Tarrif]
