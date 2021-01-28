from fastapi import APIRouter, HTTPException

from models.tarrif import Tarrif
from models.cargo import Cargo
from models.cargo_type import CargoType

from schemas.status import Status
from schemas.cargo import (
    Cargo as Cargo_Pydantic, CargoIn as CargoIn_Pydantic,
    CargoList as CargoList_Pydantic
)

from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter(
    prefix="/cargos",
    tags=["cargos"]
)


@router.get("/", response_model=CargoList_Pydantic)
async def get_all():
    cargos = await Cargo.all()
    return [await Cargo_Pydantic.from_model(cargo_obj)
            for cargo_obj in cargos]


@router.post("/", response_model=Cargo_Pydantic)
async def create(cargo: CargoIn_Pydantic):
    cargo_type = await CargoType.get(name=cargo.cargo_type.value)

    tarrif = await Tarrif.get_or_none(date=cargo.date_supplied,
                                      cargo_type=cargo_type)
    if tarrif is None:
        raise HTTPException(
            status_code=404, detail="Tarrif for specified cargo not found")

    insurance_price = tarrif.rate * cargo.price

    cargo_values = cargo.dict(exclude_unset=True)
    cargo_values['cargo_type'] = cargo_type

    cargo_obj = await Cargo.create(**cargo_values,
                                   insurance_price=insurance_price)
    return await Cargo_Pydantic.from_model(cargo_obj)


@router.get("/{cargo_id}", response_model=Cargo_Pydantic,
            responses={404: {"model": HTTPNotFoundError}})
async def get_by_id(cargo_id: str):
    cargo_obj = await Cargo.get(id=cargo_id)
    return await Cargo_Pydantic.from_model(cargo_obj)


@router.delete("/{cargo_id}", response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete(cargo_id: str):
    deleted_count = await Cargo.filter(id=cargo_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Cargo {cargo_id} not found")
    return Status(message=f"Deleted Cargo {cargo_id}")
