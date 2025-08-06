from sqlmodel import Field, SQLModel


class HostBase(SQLModel):
    contest_id: int = Field(foreign_key="contest.id")
    person_id: int = Field(foreign_key="person.id")


class Host(HostBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class HostWithId(HostBase):
    id: int


class HostPublic(HostBase):
    id: int
