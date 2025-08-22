from datetime import date as dateClass
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator


class AffiliationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str


class ArtistBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ArtistAffiliationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str


class BroadcasterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class CityBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ContestBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: dateClass
    final: int


class CountryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    alpha2: str


class LanguageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class LocationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ParticipationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    place: int | None
    running: int
    points: int | None
    jury_points: int | None
    public_points: int | None


class PersonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class SongBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str


class LocationWithCity(LocationBase):
    city: str

    @field_validator("city", mode="before")
    @classmethod
    def get_city_name(cls, value: CityBase) -> str:
        return value.name


class SongContest(SongBase):
    artist: str
    country: str

    @field_validator("artist", "country", mode="before")
    @classmethod
    def get_name(cls, value) -> str:
        return value.name


class ParticipationContest(ParticipationBase):
    song: SongContest


class ContestPublic(ContestBase):
    location: LocationWithCity
    participations: List[ParticipationContest]


class ParticipationPublic(ParticipationBase):
    contest: ContestBase


class SongPublic(SongBase):
    artist: ArtistBase
    participations: List[ParticipationPublic]


class CountryPublic(CountryBase):
    cities: List[CityBase]
    songs: List[SongPublic]
