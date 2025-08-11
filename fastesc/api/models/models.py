from datetime import date as dateClass
from typing import List

from pydantic import BaseModel, ConfigDict


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


class LocationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class PersonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class CountryPublic(CountryBase):
    cities: List[CityBase]


class CityPublic(BaseModel):
    country: CountryBase
    locations: List[LocationBase]


class LocationPublic(LocationBase):
    city: CityBase
