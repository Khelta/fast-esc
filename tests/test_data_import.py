import pytest
from fastapi import status

from data import country_import_data, contest_import_data, song_import_data
from tests.helper import client, test_app, db_session

# Needed for fill_database
country_import_data
contest_import_data
song_import_data

# Needed for testing
test_app
db_session


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
