from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from httpx import AsyncClient
from fastapi import status

from src.exceptions import WalletNotFound, NotEnoughBalance
from tests.fixtures_transfers import create_transfers_invalid_body, create_transfers_valid_body, \
    create_transfers_wallet_not_found


@pytest.mark.asyncio
async def test_make_transfer_with_invalid_body(client: AsyncClient, create_transfers_invalid_body):
    response = await client.post('/transfers', json=create_transfers_invalid_body['request_body'])
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == create_transfers_invalid_body['response_body']


@pytest.mark.asyncio
async def test_make_transfer(client: AsyncClient, create_transfers_valid_body):

    with patch(
            'src.api.views.transfers.make_transfer',
            new=CoroutineMock(return_value=create_transfers_valid_body['mock_data'])
    ):
        response = await client.post('/transfers', json=create_transfers_valid_body['request_body'])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == create_transfers_valid_body['response_body']


@pytest.mark.asyncio
async def test_make_transfer_wallet_not_found(client: AsyncClient, create_transfers_wallet_not_found):

    with patch(
            'src.api.views.transfers.make_transfer',
            new=CoroutineMock(
                side_effect=WalletNotFound(wallet_id=create_transfers_wallet_not_found['request_body']['walletToId'])
            )
    ):
        response = await client.post('/transfers', json=create_transfers_wallet_not_found['request_body'])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == create_transfers_wallet_not_found['response_body']


@pytest.mark.asyncio
async def test_make_transfer_not_enough_balance(client: AsyncClient, create_transfers_not_enough_balance):

    with patch(
            'src.api.views.transfers.make_transfer',
            new=CoroutineMock(
                side_effect=NotEnoughBalance(
                    wallet_id=create_transfers_not_enough_balance['request_body']['walletFromId']
                )
            )
    ):
        response = await client.post('/transfers', json=create_transfers_not_enough_balance['request_body'])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == create_transfers_not_enough_balance['response_body']
