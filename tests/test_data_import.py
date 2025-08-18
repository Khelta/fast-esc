import pytest
from fastapi import status

from tests.helper import client, test_app, db_session

db_session
test_app


@pytest.fixture
def country_import_data():
    yield [
        {
            "name": "Germany",
            "alpha2": "de"
        },
        {
            "name": "Switzerland",
            "alpha2": "ch"
        },
    ]


@pytest.fixture
def contest_import_data():
    yield [
        {
            "year": 2025,
            "country": "Switzerland",
            "city": "Basel",
            "location": "St. Jakobshalle",
            "broadcaster": "SSR SRG",
            "final": 0,
            "date": "17.5.2025",
            "hosts": [
                "Hazel Brugger",
                "Michelle Hunzike",
                "Sandra Studer"
            ]
        },
        {
            "year": 2011,
            "country": "Germany",
            "city": "D\u00fcsseldorf",
            "location": "Fortuna D\u00fcsseldorf Arena",
            "broadcaster": "ARD",
            "final": 2,
            "date": "12.5.2011",
            "hosts": [
                "Anke Engelke",
                "Judith Rakers",
                "Stefan Raab"
            ]
        },
        {
            "year": 1956,
            "country": "Switzerland",
            "city": "Lugano",
            "location": "Teatro Kursaal",
            "broadcaster": "SSR SRG",
            "final": 0,
            "date": "24.5.1956",
            "hosts": [
                "Lohengrin Filipello"
            ]
        }
    ]


@pytest.fixture
def song_import_data():
    yield [
        {"year": 2025,
         "final": 0,
         "participations": [{
             "artist": "Zo\u00eb M\u00eb",
             "title": "Voyage",
             "people": {
                 "ARTIST": [
                     "Zo\u00eb M\u00eb"
                 ],
                 "SONGWRITER": [
                     "Emily Middlemas",
                     "Tom Oehler",
                     "Zo\u00eb M\u00eb"
                 ],
                 "STAGE DIRECTOR": [
                     "Theo Adams"
                 ],
                 "SPOKESPERSON": [
                     "M\u00e9lanie Freymond",
                     "Sven Epiney"
                 ],
                 "COMMENTATOR": [
                     "Ellis Cavallini",
                     "Gian-Andrea Costa",
                     "Jean-Marc Richard",
                     "Nicolas Tanner",
                     "Sven Epiney"
                 ],
                 "JURY MEMBER": [
                     "Cyrill Camenzind",
                     "Gabriela Mennel",
                     "Giordano Tatum Rush",
                     "Mary Clapasson",
                     "Tiffany Athena Limacher"
                 ]
             },
             "country": "ch",
             "place": 10,
             "running": 19,
             "points": 214,
             "public_points": 0,
             "jury_points": 214
         }]},
        {"year": 1956,
         "final": 0,
         "participations": [{
             "artist": "Lys Assia",
             "title": "Das alte Karussell",
             "people": {
                 "ARTIST": [
                     "Lys Assia"
                 ],
                 "BACKING": [
                     "Anita Traversi",
                     "Athos Beretta",
                     "Carmen Tumiati",
                     "Luciano Rezzonico",
                     "Silvano Beretta"
                 ],
                 "SONGWRITER": [
                     "Fernando Paggi",
                     "George Betz-Stahl"
                 ],
                 "CONDUCTOR": [
                     "Fernando Paggi"
                 ],
                 "COMMENTATOR": [
                     "Georges Hardy"
                 ]
             },
             "country": "ch2",
             "place": None,
             "running": 2,
             "points": None,
             "public_points": None,
             "jury_points": None
         }]}
    ]


class TestDataimportAPI:

    @pytest.mark.asyncio
    async def test_import_countries(self, client, country_import_data):
        response = await client.post("/data_import/countries/",
                                     json=country_import_data
                                     )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_import_contests(self, client, country_import_data, contest_import_data):
        # Countries must be in database before contest import
        await client.post("/data_import/countries/",
                          json=country_import_data)

        response = await client.post("/data_import/contests/",
                                     json=contest_import_data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_import_songs(self, client, country_import_data, contest_import_data, song_import_data):
        # Countries must be in database before contest import
        await client.post("/data_import/countries/",
                          json=country_import_data)

        # Contests must be in database before song import
        await client.post("/data_import/contests/",
                          json=contest_import_data)

        response = await client.post("/data_import/songs/",
                                     json=song_import_data)
        assert response.status_code == status.HTTP_200_OK
