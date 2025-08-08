from sqlmodel import Session, select

from fastesc.models.city import City, CityWithId


def get_or_create_city(session: Session, input_data: City):
    if input_data.id:
        instance = session.get(City, input_data.id)
    else:
        instance = session.exec(
            select(City).where(
                City.name == input_data.name,
                City.country_id == input_data.country_id
            )
        ).first()

    if not instance:
        instance = City(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return CityWithId(**instance.model_dump())
