from fastapi import APIRouter, Depends
from sqlmodel import Session

from fastesc.api.models.country import Country
from fastesc.database import get_session
from fastesc.repositories.country_repo import get_or_create_country

router = APIRouter(prefix="/data_import", tags=["import"])


@router.post("/countries/", response_model=list[Country])
def import_country_data(
        *, session: Session = Depends(get_session), data: list[Country]
):
    result = []

    for country in data:
        Country.model_validate(country)
        db_country = get_or_create_country(session, country)
        result.append(db_country)

    return result
