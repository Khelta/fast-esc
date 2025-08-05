from sqlmodel import Field, Session, SQLModel, select


class CityBase(SQLModel):
    name: str = Field(index=True)
    country_id: int = Field(foreign_key="country.id")


class City(CityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CityWithId(CityBase):
    id: int


class CityPublic(CityBase):
    id: int


def get_or_create_city(session: Session, input_data: City):
    if input_data.id:
        instance = session.get(City, input_data.id)
    else:
        instance = session.exec(
            select(City).where(
                City.name == input_data.name
                and City.country_id == input_data.country_id
            )
        ).first()

    if not instance:
        instance = City(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return CityWithId(**instance.model_dump())
