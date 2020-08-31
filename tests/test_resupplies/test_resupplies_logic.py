from unittest.mock import patch

import pytest
from asynctest import CoroutineMock

from src.billing_operations import make_resupply
from src.exceptions import WalletNotFound
from tests.test_resupplies.fixtures_resupplies import create_resupply_data


@pytest.mark.asyncio
async def test_make_resupply(db_connect, create_resupply_data):
    with patch(
        'src.models.Transaction.create',
        new=CoroutineMock(return_value=create_resupply_data['transaction_create_mock_data'])
    ), patch(
        'src.models.Wallet.change_balance',
        new=CoroutineMock(return_value=create_resupply_data['wallet_change_balance_mock_data'])
    ), patch(
        'src.models.WalletsOperation.create',
        new=CoroutineMock(return_value=create_resupply_data['wallets_operation_create_mock_data'])
    ), patch(
        'src.billing_operations.generate_transaction_number',
        return_value=create_resupply_data['generate_transaction_number_mock_data']
    ):
        result = await make_resupply(**create_resupply_data['params'])

    assert result == create_resupply_data['result']


@pytest.mark.asyncio
async def test_make_resupply_wallet_not_found(db_connect, create_resupply_data):
    with patch(
        'src.models.Transaction.create',
        new=CoroutineMock(return_value=create_resupply_data['transaction_create_mock_data'])
    ), patch(
        'src.models.Wallet.change_balance',
        new=CoroutineMock(side_effect=WalletNotFound(create_resupply_data['params']['wallet_id']))
    ):
        with pytest.raises(WalletNotFound) as exc_info:
            await make_resupply(**create_resupply_data['params'])
        assert exc_info.value.message == create_resupply_data['error_message']
