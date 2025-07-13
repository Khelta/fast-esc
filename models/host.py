from sqlmodel import Field, Session, SQLModel, select


class HostBase(SQLModel):
    contest_id: int = Field(foreign_key="contest.id")
    person_id: int = Field(foreign_key="person.id")


class Host(HostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class HostWithId(HostBase):
    id: int


class HostPublic(HostBase):
    id: int


def get_or_create_host(session: Session, input_data: Host):
    if input_data.id:
        instance = session.get(Host, input_data.id)
    else:
        instance = session.exec(
            select(Host).where(
                Host.contest_id == input_data.contest_id
                and Host.person_id == input_data.person_id
            )
        ).first()

    if not instance:
        instance = Host(**input_data.model_dump())
        session.add(instance)
        session.commit()
        session.refresh(instance)

    return HostWithId(**instance.model_dump())
