from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models.country import Country

router = APIRouter(prefix="/data_import", tags=["import"])


@router.post("/countries/", response_model=list[Country])
def import_country_data(
    *, session: Session = Depends(get_session), data: list[Country]
):
    result = []

    for country in data:
        Country.model_validate(country)

        db_country = session.exec(
            select(Country).where(Country.name == country.name)
        ).first()
        if db_country is None:
            db_country = Country(name=country.name, alpha2=country.alpha2)
            session.add(db_country)
        result.append(db_country)

    session.commit()
    for obj in result:
        session.refresh(obj)

    return result
