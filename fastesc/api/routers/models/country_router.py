from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from fastesc.api.dependencies import get_repository
from fastesc.api.models.models import CountryPublic
from fastesc.database.models.models import Country
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/countries", tags=["countries"])

CountryRepository = Annotated[
    DatabaseRepository[Country],
    Depends(get_repository(Country))
]


@router.get("", response_model=list[CountryPublic])
async def get_countries(repository: CountryRepository, offset: int = 0, limit: int = None):
    countries = await repository.filter(offset=offset, limit=limit)
    return [CountryPublic.model_validate(country) for country in countries]


@router.get("/{id}", response_model=CountryPublic)
async def get_country_by_id(repository: CountryRepository, id: int):
    country = await repository.get(id)
    if country:
        return CountryPublic.model_validate(country)
    raise HTTPException(status_code=404, detail=f"Country with id '{id}' not found.")


@router.get("/by_name/{name}", response_model=CountryPublic)
async def get_country_by_name(repository: CountryRepository, name: str):
    country = await repository.get_by_dict({"name": name.capitalize()})
    if country:
        return CountryPublic.model_validate(country)
    raise HTTPException(status_code=404, detail=f"Country '{name}' not found.")
