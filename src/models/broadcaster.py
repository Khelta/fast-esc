from sqlmodel import Field, Session, SQLModel, select


class BroadcasterBase(SQLModel):
    name: str = Field(index=True)

    country_id: int = Field(foreign_key="country.id")


class Broadcaster(BroadcasterBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BroadcasterWithId(BroadcasterBase):
    id: int


class BroadcasterPublic(BroadcasterBase):
    id: int


def get_or_create_broadcaster(session: Session, input_data: Broadcaster):
    if input_data.id:
        instance = session.get(Broadcaster, input_data.id)
    else:
        instance = session.exec(
            select(Broadcaster).where(
                Broadcaster.name == input_data.name
                and Broadcaster.country_id == input_data.country_id
            )
        ).first()

    if not instance:
        instance = Broadcaster(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return BroadcasterWithId(**instance.model_dump())
