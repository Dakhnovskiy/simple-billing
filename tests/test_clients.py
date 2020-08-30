from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from httpx import AsyncClient
from fastapi import status

from tests.fixtures import create_clients_invalid_body, create_clients_valid_body


@pytest.mark.asyncio
async def test_create_client_with_invalid_body(client: AsyncClient, create_clients_invalid_body):
    response = await client.post('/clients', json=create_clients_invalid_body['request_body'])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == create_clients_invalid_body['response_body']


@pytest.mark.asyncio
async def test_create_client(client: AsyncClient, create_clients_valid_body):

    with patch(
            'src.api.views.clients.create_client_with_wallet',
            new=CoroutineMock(return_value=create_clients_valid_body['mock_data'])
    ):
        response = await client.post('/clients', json=create_clients_valid_body['request_body'])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == create_clients_valid_body['response_body']
