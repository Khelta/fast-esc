from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from fastesc.api.dependencies import get_repository
from fastesc.api.models.models import CountryBase, CountryPublic
from fastesc.database.models.models import Country
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/countries", tags=["countries"])

CountryRepository = Annotated[
    DatabaseRepository[Country],
    Depends(get_repository(Country))
]


@router.get("", response_model=list[CountryPublic])
async def get_countries(repository: CountryRepository):
    countries = await repository.filter()
    return [CountryPublic.model_validate(country) for country in countries]


@router.get("/{id}", response_model=CountryBase)
async def get_country(repository: CountryRepository, id: int):
    country = await repository.get(id)
    if country:
        return CountryBase.model_validate(country)
    raise HTTPException(status_code=404, detail="Country not found.")
