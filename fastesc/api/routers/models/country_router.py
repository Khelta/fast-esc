from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastesc.api.models.country import CountryBase
from fastesc.database.models.country import Country
from fastesc.db import get_db_session

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("", response_model=list[CountryBase])
async def get_countries(session: AsyncSession = Depends(get_db_session)):
    countries = list(await session.scalars(select(Country)))
    return [CountryBase.model_validate(country) for country in countries]
