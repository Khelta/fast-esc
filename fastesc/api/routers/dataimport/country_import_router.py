from typing import Annotated

from fastapi import APIRouter, Depends

from fastesc.api.dependencies import get_repository
from fastesc.api.models.models import CountryBase
from fastesc.database.models.models import Country

from fastesc.database.repositories.base_repo import DatabaseRepository

router = APIRouter(prefix="/data_import", tags=["import"])

CountryRepository = Annotated[
    DatabaseRepository[Country],
    Depends(get_repository(Country))
]


@router.post("/countries/", response_model=list[CountryBase])
async def import_country_data(repository: CountryRepository, data: list[CountryBase]):
    result = []

    for c in data:
        country = CountryBase.model_validate(c)
        await repository.create(country.model_dump())
        result.append(country)

    return result
