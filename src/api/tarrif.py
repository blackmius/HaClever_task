from fastapi import APIRouter, HTTPException

from models.tarrif import Tarrif
from models.cargo_type import CargoType

from schemas.status import Status
from schemas.tarrif import (
    Tarrif as Tarrif_Pydantic, TarrifIn as TarrifIn_Pydantic,
    TarrifList as TarrifList_Pydantic
)

from tortoise.contrib.fastapi import HTTPNotFoundError


router = APIRouter(
    prefix="/tarrifs",
    tags=["tarrifs"]
)


@router.get("/", response_model=TarrifList_Pydantic)
async def get_all():
    tarrifes = await Tarrif.all()
    return [await Tarrif_Pydantic.from_model(tarrif_obj)
            for tarrif_obj in tarrifes]


@router.post("/", response_model=Tarrif_Pydantic)
async def create(tarrif: TarrifIn_Pydantic):
    cargo_type = await CargoType.get_or_none(name=tarrif.cargo_type.value)

    tarrif_values = tarrif.dict(exclude_unset=True)
    tarrif_values['cargo_type'] = cargo_type
    tarrif_obj = await Tarrif.create(**tarrif_values)

    return await Tarrif_Pydantic.from_model(tarrif_obj)


@router.get("/{tarrif_id}", response_model=Tarrif_Pydantic,
            responses={404: {"model": HTTPNotFoundError}})
async def get_by_id(tarrif_id: str):
    tarrif_obj = await Tarrif.get(id=tarrif_id)
    return await Tarrif_Pydantic.from_model(tarrif_obj)


@router.put("/{tarrif_id}", response_model=Tarrif_Pydantic,
            responses={404: {"model": HTTPNotFoundError}})
async def update(tarrif_id: str, tarrif: TarrifIn_Pydantic):
    cargo_type = await CargoType.get(name=tarrif.cargo_type.value)

    tarrif_values = tarrif.dict(exclude_unset=True)
    tarrif_values['cargo_type'] = cargo_type

    await Tarrif.filter(id=tarrif_id).update(**tarrif_values)
    tarrif_obj = await Tarrif.get(id=tarrif_id)
    return await Tarrif_Pydantic.from_model(tarrif_obj)


@router.delete("/{tarrif_id}", response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete(tarrif_id: str):
    deleted_count = await Tarrif.filter(id=tarrif_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Tarrif {tarrif_id} not found")
    return Status(message=f"Deleted tarrif {tarrif_id}")
