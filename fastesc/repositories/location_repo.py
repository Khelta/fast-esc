from sqlmodel import Session, select

from fastesc.api.models import Location, LocationWithId


def get_or_create_location(session: Session, input_data: Location):
    if input_data.id:
        instance = session.get(Location, input_data.id)
    else:
        instance = session.exec(
            select(Location).where(
                Location.name == input_data.name,
                Location.city_id == input_data.city_id
            )
        ).first()

    if not instance:
        instance = Location(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return LocationWithId(**instance.model_dump())
