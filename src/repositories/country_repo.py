from sqlmodel import Session, select

from src.models.country import Country, CountryWithId


def get_or_create_country(session: Session, input_data: Country):
    if input_data.id:
        instance = session.get(Country, input_data.id)
    else:
        instance = session.exec(
            select(Country).where(
                Country.alpha2 == input_data.alpha2,
            )
        ).first()

    if not instance:
        instance = Country(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return CountryWithId(**instance.model_dump())


def get_country_by_alpha2(session: Session, alpha2: str):
    if len(alpha2) == 3:
        if alpha2[-1].isdigit():
            alpha2 = alpha2[:-1]

    instance = session.exec(
        select(Country).where(Country.alpha2 == alpha2)
    ).first()

    if instance is not None:
        return CountryWithId(**instance.model_dump())
    else:
        return None


def get_country_by_county_name(session: Session, countryname: str):
    instance = session.exec(
        select(Country).where(Country.name == countryname)
    ).first()

    if instance is not None:
        return CountryWithId(**instance.model_dump())
    else:
        return None
