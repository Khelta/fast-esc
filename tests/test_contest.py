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


class TestContestAPI:
    @pytest.mark.asyncio
    async def test_get_all_contests(self, client, fill_database):
        response = await client.get("/contests?limit=0")
        assert response.status_code == status.HTTP_200_OK

        assert len(response.json()) == 3
        assert response.json()[0]["date"] == "2025-05-17"
        assert response.json()[0]["final"] == 0

        assert len(response.json()[0]["participations"]) == 1
        participation = response.json()[0]["participations"][0]
        assert participation["place"] == 10
        assert participation["running"] == 19
        assert participation["points"] == 214
        assert participation["public_points"] == 0
        assert participation["jury_points"] == 214

        song = participation["song"]
        assert song["artist"] == "Zo\u00eb M\u00eb"
        assert song["title"] == "Voyage"
        assert song["country"] == "Switzerland"

    @pytest.mark.asyncio
    async def test_get_contest(self, client, fill_database):
        response = await client.get("/contests/4")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await client.get("/contests/1")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["date"] == "2025-05-17"
        assert response.json()["final"] == 0

        assert len(response.json()["participations"]) == 1
        participation = response.json()["participations"][0]
        assert participation["place"] == 10
        assert participation["running"] == 19
        assert participation["points"] == 214
        assert participation["public_points"] == 0
        assert participation["jury_points"] == 214

        song = participation["song"]
        assert song["artist"] == "Zo\u00eb M\u00eb"
        assert song["title"] == "Voyage"
        assert song["country"] == "Switzerland"

    @pytest.mark.asyncio
    async def test_get_contest_by_year(self, client, fill_database):
        response = await client.get("/contests/by_year/2025/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await client.get("/contests/by_year/2025/0")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["date"] == "2025-05-17"
        assert response.json()["final"] == 0

        assert len(response.json()["participations"]) == 1
        participation = response.json()["participations"][0]
        assert participation["place"] == 10
        assert participation["running"] == 19
        assert participation["points"] == 214
        assert participation["public_points"] == 0
        assert participation["jury_points"] == 214

        song = participation["song"]
        assert song["artist"] == "Zo\u00eb M\u00eb"
        assert song["title"] == "Voyage"
        assert song["country"] == "Switzerland"
