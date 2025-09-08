import pytest
from fastapi import status

from tests.data import country_import_data, contest_import_data, song_import_data
from tests.helper import client, test_app, fill_database, db_session

# Needed for fill_database
country_import_data
contest_import_data
song_import_data

# Needed for testing
test_app
db_session


class TestSongtextAPI:

    @pytest.mark.asyncio
    async def test_find_in_songtext_case_sensitive(self, client, fill_database):
        response = await client.get("/songtext?text=karussell&case_sensitive=false")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["size"] == 1
        assert len(response.json()["songs"]) == 1
        assert response.json()["songs"][0]["title"] == "Das alte Karussell"

        response = await client.get("/songtext?text=karussell&case_sensitive=true")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["size"] == 0
        assert len(response.json()["songs"]) == 0

    @pytest.mark.asyncio
    async def test_find_in_songtext_whole_word(self, client, fill_database):
        response = await client.get("/songtext?text=spiel&whole_word=false")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["size"] == 1
        assert len(response.json()["songs"]) == 1
        assert response.json()["songs"][0]["title"] == "Das alte Karussell"

        response = await client.get("/songtext?text=spiel&whole_word=true")
        assert response.status_code == status.HTTP_200_OK

        assert response.json()["size"] == 0
        assert len(response.json()["songs"]) == 0

    @pytest.mark.asyncio
    async def test_find_in_songtext_case_sensitive(self, client, fill_database):
        response = await client.get("/songtext?text=Eine&case_sensitive=true&whole_word=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 1

        response = await client.get("/songtext?text=eine&case_sensitive=true&whole_word=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 1

        response = await client.get("/songtext?text=Eine&case_sensitive=true&whole_word=false")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 1

        response = await client.get("/songtext?text=eine&case_sensitive=true&whole_word=false")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 2

        response = await client.get("/songtext?text=Eine&case_sensitive=false&whole_word=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 2

        response = await client.get("/songtext?text=eine&case_sensitive=false&whole_word=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 2

        response = await client.get("/songtext?text=Eine&case_sensitive=false&whole_word=false")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 3

        response = await client.get("/songtext?text=eine&case_sensitive=false&whole_word=false")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["word_count"] == 3
