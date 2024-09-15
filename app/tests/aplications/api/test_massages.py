import pytest

from faker import Faker

from httpx import Response

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status


@pytest.mark.asyncio
async def test_create_chat_success(
        app: FastAPI,
        client: TestClient,
        faker: Faker
):
    url = app.url_path_for('create_chat_handler')
    title = faker.text(max_nb_chars=30)
    response: Response = client.post(url=url, json={'title': title})

    assert response.is_success
    json_data = response.json()

    assert json_data['title'] == title


@pytest.mark.asyncio
async def test_create_chat_fail_text_too_long(
        app: FastAPI,
        client: TestClient,
        faker: Faker
):
    url = app.url_path_for('create_chat_handler')
    title = faker.sentence(nb_words=50)
    print(title)
    response: Response = client.post(url=url, json={'title': title})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data['detail']['error']
