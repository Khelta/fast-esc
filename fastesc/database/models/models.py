from datetime import date
from typing import List

from sqlalchemy import String, ForeignKey, CheckConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastesc.database.models.base import Base


class Artist(Base):
    __tablename__ = 'artist'

    name: Mapped[str] = mapped_column("name", nullable=False, index=True)

    affiliations: Mapped[List["Affiliation"]] = relationship(back_populates="artist", lazy="selectin")
    songs: Mapped[List["Song"]] = relationship(back_populates="artist", lazy="selectin")

    class Config:
        orm_mode = True


class Affiliation(Base):
    __tablename__ = 'affiliation'

    role: Mapped[str] = mapped_column("role", nullable=False, index=True)

    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"), nullable=False, index=True)
    person: Mapped["Person"] = relationship(back_populates="affiliations", lazy="selectin")
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"), nullable=True, index=True)
    artist: Mapped["Artist"] = relationship(back_populates="affiliations", lazy="selectin")
    contest_id: Mapped[int] = mapped_column(ForeignKey("contest.id"), nullable=False, index=True)
    contest: Mapped["Contest"] = relationship(back_populates="affiliations", lazy="selectin")

    class Config:
        orm_mode = True


class Broadcaster(Base):
    __tablename__ = 'broadcaster'

    name: Mapped[str] = mapped_column("name", nullable=False, index=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"), index=True)
    country: Mapped["Country"] = relationship(back_populates="broadcasters", lazy="selectin")

    contests: Mapped[List["Contest"]] = relationship(back_populates="broadcaster", lazy="selectin")

    class Config:
        orm_mode = True


class City(Base):
    __tablename__ = 'city'

    name: Mapped[str] = mapped_column("name", nullable=False, index=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"), index=True)
    country: Mapped["Country"] = relationship(back_populates="cities", lazy="selectin")

    locations: Mapped[List["Location"]] = relationship(back_populates="city", lazy="selectin")

    class Config:
        orm_mode = True


class Contest(Base):
    __tablename__ = 'contest'

    date: Mapped[date] = mapped_column("date", type_=Date, nullable=False, index=True)
    final: Mapped[int] = mapped_column("final", nullable=False, index=True)

    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"), index=True)
    location: Mapped["Location"] = relationship(back_populates="contests", lazy="selectin")
    broadcaster_id: Mapped[int] = mapped_column(ForeignKey("broadcaster.id"), index=True)
    broadcaster: Mapped["Broadcaster"] = relationship(back_populates="contests", lazy="selectin")

    participations: Mapped[List["Participation"]] = relationship(back_populates="contest", lazy="selectin")
    affiliations: Mapped[List["Affiliation"]] = relationship(back_populates="contest", lazy="selectin")

    __table_args__ = (
        CheckConstraint("final BETWEEN 0 AND 2", name="final_value_check"),
    )

    class Config:
        orm_mode = True


class Country(Base):
    __tablename__ = 'country'

    name: Mapped[str] = mapped_column("name", nullable=False, index=True)
    alpha2: Mapped[str] = mapped_column("alpha2", String(length=2), nullable=False, index=True)

    cities: Mapped[List["City"]] = relationship(back_populates="country", lazy="selectin")
    broadcasters: Mapped[List["Broadcaster"]] = relationship(back_populates="country", lazy="selectin")
    songs: Mapped[List["Song"]] = relationship(back_populates="country", lazy="selectin")

    class Config:
        orm_mode = True


class Location(Base):
    __tablename__ = 'location'

    name: Mapped[str] = mapped_column("name", nullable=False)

    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"), index=True)
    city: Mapped["City"] = relationship(back_populates="locations", lazy="selectin")

    contests: Mapped[List["Contest"]] = relationship(back_populates="location", lazy="selectin")

    class Config:
        orm_mode = True


class Participation(Base):
    __tablename__ = 'participation'

    place: Mapped[int] = mapped_column("place", nullable=True, index=True)
    running: Mapped[int] = mapped_column("running", index=True)
    points: Mapped[int] = mapped_column("points", nullable=True, index=True)
    jury_points: Mapped[int] = mapped_column("jury_points", nullable=True, index=True)
    public_points: Mapped[int] = mapped_column("public_points", nullable=True, index=True)

    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"), index=True)
    song: Mapped["Song"] = relationship(back_populates="participations", lazy="selectin")
    contest_id: Mapped[int] = mapped_column(ForeignKey("contest.id"), index=True)
    contest: Mapped["Contest"] = relationship(back_populates="participations", lazy="selectin")

    class Config:
        orm_mode = True


class Person(Base):
    __tablename__ = 'person'

    name: Mapped[str] = mapped_column("name", nullable=False, index=True)

    affiliations: Mapped[List["Affiliation"]] = relationship(back_populates="person", lazy="selectin")

    class Config:
        orm_mode = True


class Song(Base):
    __tablename__ = 'song'

    title: Mapped[str] = mapped_column("title", nullable=False, index=True)

    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"), index=True)
    country: Mapped["Country"] = relationship(back_populates="songs", lazy="selectin")
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id"), index=True)
    artist: Mapped["Artist"] = relationship(back_populates="songs", lazy="selectin")

    participations: Mapped[List["Participation"]] = relationship(back_populates="song", lazy="selectin")

    class Config:
        orm_mode = True
