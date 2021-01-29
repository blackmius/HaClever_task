from fastapi import APIRouter, HTTPException

from models.tariff import Tariff
from models.cargo_type import CargoType

from schemas.status import Status
from schemas.tariff import (
    Tariff as Tariff_Pydantic, TariffIn as TariffIn_Pydantic,
    TariffList as TariffList_Pydantic
)

from tortoise.contrib.fastapi import HTTPNotFoundError


router = APIRouter(
    prefix="/tariffs",
    tags=["tariffs"]
)


@router.get("/", response_model=TariffList_Pydantic)
async def get_all():
    """ Получение всех тарифов """
    tariffes = await Tariff.all().prefetch_related('cargo_type')
    return [await Tariff_Pydantic.from_model(tariff_obj)
            for tariff_obj in tariffes]


@router.post("/", response_model=Tariff_Pydantic)
async def create(tariff: TariffIn_Pydantic):
    """ Добавление записи о тарифе """
    cargo_type = await CargoType.get_or_none(name=tariff.cargo_type.value)

    tariff_values = tariff.dict(exclude_unset=True)
    tariff_values['cargo_type'] = cargo_type
    tariff_obj = await Tariff.create(**tariff_values)

    return await Tariff_Pydantic.from_model(tariff_obj)


@router.get("/{tariff_id}", response_model=Tariff_Pydantic,
            responses={404: {"model": HTTPNotFoundError}})
async def get_by_id(tariff_id: str):
    """ Получение тарифа по его идентификатору """
    tariff_obj = await Tariff.get(id=tariff_id).prefetch_related('cargo_type')
    return await Tariff_Pydantic.from_model(tariff_obj)


@router.put("/{tariff_id}", response_model=Tariff_Pydantic,
            responses={404: {"model": HTTPNotFoundError}})
async def update(tariff_id: str, tariff: TariffIn_Pydantic):
    """ Редактирование полей тарифа """
    cargo_type = await CargoType.get(name=tariff.cargo_type.value)

    tariff_values = tariff.dict(exclude_unset=True)
    tariff_values['cargo_type'] = cargo_type

    await Tariff.filter(id=tariff_id).update(**tariff_values)
    tariff_obj = await Tariff.get(id=tariff_id).prefetch_related('cargo_type')
    return await Tariff_Pydantic.from_model(tariff_obj)


@router.delete("/{tariff_id}", response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete(tariff_id: str):
    """ Удаление записи о тарифе """
    deleted_count = await Tariff.filter(id=tariff_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Tarrif {tariff_id} not found")
    return Status(message=f"Deleted tarrif {tariff_id}")
