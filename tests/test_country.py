import pytest
from fastapi import status

from data import country_import_data, contest_import_data, song_import_data
from tests.helper import client, test_app, db_session, fill_database

# Needed for fill_database
country_import_data
contest_import_data
song_import_data

# Needed for testing
test_app
db_session


class TestCountriesAPI:
    @pytest.mark.asyncio
    async def test_get_all_countries(self, client, fill_database):
        response = await client.get("/countries")
        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Germany"
        assert response.json()[0]["alpha2"] == "de"
        assert response.json()[1]["name"] == "Switzerland"
        assert response.json()[1]["alpha2"] == "ch"

    @pytest.mark.asyncio
    async def test_get_country(self, client, fill_database):
        response = await client.get("/countries/1")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["name"] == "Germany"
        assert response.json()["alpha2"] == "de"

        response = await client.get("/countries/3")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_country_by_name(self, client, fill_database):
        response = await client.get("/countries/by_name/germany")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Germany"
        assert response.json()["alpha2"] == "de"

        response = await client.get("/countries/by_name/ireland")
        assert response.status_code == status.HTTP_404_NOT_FOUND
