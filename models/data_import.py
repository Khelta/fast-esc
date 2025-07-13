from datetime import datetime

from pydantic import BaseModel, field_serializer, field_validator


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
