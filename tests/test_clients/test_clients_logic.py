from unittest.mock import patch

import pytest
from asynctest import CoroutineMock

from src.clients import create_client_with_wallet
from src.exceptions import ClientLoginAlreadyExists
from tests.test_clients.fixtures_clients import create_client_with_wallet_data


@pytest.mark.asyncio
async def test_create_client_with_wallet(db_connect, create_client_with_wallet_data):
    with patch(
        'src.models.Client.create',
        new=CoroutineMock(return_value=create_client_with_wallet_data['client_create_mock_data'])
    ), patch(
        'src.models.Wallet.create',
        new=CoroutineMock(return_value=create_client_with_wallet_data['wallet_create_mock_data'])
    ):
        result = await create_client_with_wallet(**create_client_with_wallet_data['params'])

    assert result == create_client_with_wallet_data['result']


@pytest.mark.asyncio
async def test_create_client_with_wallet_already_exists(db_connect, create_client_with_wallet_data):
    with patch(
        'src.models.Client.create',
        new=CoroutineMock(side_effect=ClientLoginAlreadyExists())
    ):
        with pytest.raises(ClientLoginAlreadyExists) as exc_info:
            await create_client_with_wallet(**create_client_with_wallet_data['params'])
        assert exc_info.value.message == create_client_with_wallet_data['error_message']
