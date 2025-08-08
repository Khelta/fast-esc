from typing import Annotated

from fastapi import APIRouter, Depends

from fastesc.api.dependencies import get_repository
from fastesc.api.models.country import CountryBase
from fastesc.database.models.country import Country
from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/countries", tags=["countries"])

CountryRepository = Annotated[
    DatabaseRepository[Country],
    Depends(get_repository(Country))
]


@router.get("", response_model=list[CountryBase])
async def get_countries(repository: CountryRepository):
    countries = await repository.filter()
    return [CountryBase.model_validate(country) for country in countries]
