from sqlmodel import Field, SQLModel


class ParticipationBase(SQLModel):
    song_id: int = Field(foreign_key="song.id", index=True)
    contest_id: int = Field(foreign_key="contest.id", index=True)

    place: int | None = Field(default=None, index=True)
    running: int | None = Field(default=None, index=True)

    points: int | None = Field(default=None)
    jury_points: int | None = Field(default=None)
    public_points: int | None = Field(default=None)


class Participation(ParticipationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ParticipationWithId(ParticipationBase):
    id: int


class ParticipationPublic(ParticipationBase):
    id: int
