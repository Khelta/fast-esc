from sqlmodel import Field, Session, SQLModel, select


class LocationBase(SQLModel):
    name: str = Field(unique=True, index=True)

    city_id: int = Field(foreign_key="city.id")


class Location(LocationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class LocationWithId(LocationBase):
    id: int


class LocationPublic(LocationBase):
    id: int


def get_or_create_location(session: Session, input_data: Location):
    if input_data.id:
        instance = session.get(Location, input_data.id)
    else:
        instance = session.exec(
            select(Location).where(
                Location.name == input_data.name
                and Location.city_id == input_data.city_id
            )
        ).first()

    if not instance:
        instance = Location(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return LocationWithId(**instance.model_dump())
