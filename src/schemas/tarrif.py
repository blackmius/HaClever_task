from typing import List

from pydantic import BaseModel
from uuid import UUID
from datetime import date

from .cargo_type import CargoType

from models.tarrif import Tarrif as TarrifModel

import tortoise


class TarrifIn(BaseModel):
    cargo_type: CargoType
    date: date
    rate: float


class Tarrif(TarrifIn):
    id: UUID

    @staticmethod
    async def from_model(model: TarrifModel) -> 'Tarrif':
        if isinstance(model.cargo_type, tortoise.queryset.QuerySet):
            cargo_type = await model.cargo_type.first()
        else:
            cargo_type = model.cargo_type
        return Tarrif(id=model.id, cargo_type=cargo_type.name,
                      date=model.date, rate=model.rate)


class TarrifList(BaseModel):
    __root__: List[Tarrif]
