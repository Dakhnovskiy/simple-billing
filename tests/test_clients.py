import pytest
from httpx import AsyncClient
from fastapi import status

from tests.fixtures import create_clients_bad_body


@pytest.mark.asyncio
async def test_create_client_with_bad_body(client: AsyncClient, create_clients_bad_body):
    response = await client.post('/clients', json=create_clients_bad_body['request_body'])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    print(response.json())
    print(create_clients_bad_body['response_body'])
    assert response.json() == create_clients_bad_body['response_body']
