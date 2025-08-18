import pytest
import pytest_asyncio
from fastapi import status

from tests.helper import client, test_app, db_session

db_session
test_app


@pytest_asyncio.fixture()
def test_data():
    yield [
        {
            "name": "Germany",
            "alpha2": "de"
        },
        {
            "name": "Sweden",
            "alpha2": "se"
        },
    ]


@pytest_asyncio.fixture()
async def import_countries(client, test_data):
    response = await client.post("/data_import/countries/",
                                 json=test_data
                                 )


class TestCountriesAPI:
    @pytest.mark.asyncio
    async def test_get_all_countries(self, client, import_countries):
        response = await client.get("/countries")
        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Germany"
        assert response.json()[0]["alpha2"] == "de"
        assert response.json()[1]["name"] == "Sweden"
        assert response.json()[1]["alpha2"] == "se"

    @pytest.mark.asyncio
    async def test_get_country(self, client, import_countries):
        response = await client.get("/countries/1")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["name"] == "Germany"
        assert response.json()["alpha2"] == "de"

        response = await client.get("/countries/3")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_country_by_name(self, client, import_countries):
        response = await client.get("/countries/by_name/germany")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Germany"
        assert response.json()["alpha2"] == "de"

        response = await client.get("/countries/by_name/ireland")
        assert response.status_code == status.HTTP_404_NOT_FOUND
