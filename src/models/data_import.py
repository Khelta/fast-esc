from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator


class DataImportContest(BaseModel):
    year: int
    country: str
    city: str
    location: str
    broadcaster: str
    final: int
    date: str
    hosts: list[str] | None = None

    @field_validator("date")
    def validate_date(cls, date: str):
        try:
            datetime.strptime(date, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Date must be in the format DD.MM.YYYY")
        return date

    @field_serializer("date")
    def serialize_date(self, date: str):
        return datetime.strptime(date, "%d.%m.%Y").date()


class DataImportSong(BaseModel):
    country: str = Field(examples=["ch"])
    final: int = Field(
        description="Decodes if the contest is a final (0) or semi-final (1) or (2)",
        examples=[0, 1, 2],
    )
    artist: str = Field(examples=["Lys Assia"])
    title: str = Field(examples=["Refrain"])
    place: int | None = None
    running: int | None = None
    points: int | None = None
    public_points: int | None = None
    jury_points: int | None = None
    people: dict[str, list[str]] | None = Field(
        default=None,
        description="Dict where the keys are the role and the value is a list of all people who have this role.",
        examples=[{"ARTIST": ["Lys Assia"], "COMPOSER": ["G\u00e9o Voumard"]}],
    )
