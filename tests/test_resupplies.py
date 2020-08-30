from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from httpx import AsyncClient
from fastapi import status

from tests.fixtures_resupplies import create_resupplies_invalid_body, create_resupplies_valid_body


@pytest.mark.asyncio
async def test_make_resupply_with_invalid_body(client: AsyncClient, create_resupplies_invalid_body):
    response = await client.post('/resupplies', json=create_resupplies_invalid_body['request_body'])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == create_resupplies_invalid_body['response_body']


@pytest.mark.asyncio
async def test_make_resupply(client: AsyncClient, create_resupplies_valid_body):

    with patch(
            'src.api.views.resupplies.make_resupply',
            new=CoroutineMock(return_value=create_resupplies_valid_body['mock_data'])
    ):
        response = await client.post('/resupplies', json=create_resupplies_valid_body['request_body'])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == create_resupplies_valid_body['response_body']
