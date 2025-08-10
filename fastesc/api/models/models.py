from typing import List

from pydantic import BaseModel, ConfigDict


class ArtistBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class ArtistAffiliationBase(BaseModel):
    role: str


class CityBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class CountryBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    alpha2: str


class LocationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class CountryPublic(CountryBase):
    cities: List[CityBase]


class CityPublic(BaseModel):
    country: CountryBase
    locations: List[LocationBase]


class LocationPublic(LocationBase):
    city: CityBase
