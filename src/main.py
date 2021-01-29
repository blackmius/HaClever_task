from fastapi import FastAPI

from tortoise import Tortoise
from models.cargo_type import CargoType

from api import tariff, cargo

app = FastAPI(title="Haclever task")


app.include_router(tariff.router)
app.include_router(cargo.router)


@app.on_event('startup')
async def init():
    await Tortoise.init(db_url="sqlite://:memory:",
                        modules={"models": ["models"]})
    await Tortoise.generate_schemas()

    await CargoType.get_or_create(name='Glass')
    await CargoType.get_or_create(name='Other')
