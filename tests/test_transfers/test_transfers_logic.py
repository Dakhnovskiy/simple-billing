from unittest.mock import patch

import pytest
from asynctest import CoroutineMock

from src.billing_operations import make_transfer
from src.exceptions import WalletNotFound, NotEnoughBalance
from tests.test_transfers.fixtures_transfers import create_transfer_data


@pytest.mark.asyncio
async def test_make_transfer(db_connect, create_transfer_data):
    with patch(
        'src.models.Transaction.create',
        new=CoroutineMock(return_value=create_transfer_data['transaction_create_mock_data'])
    ), patch(
        'src.models.Wallet.change_balance',
        new=CoroutineMock(return_value=create_transfer_data['wallet_change_balance_mock_data'])
    ), patch(
        'src.models.WalletsOperation.create',
        new=CoroutineMock(return_value=create_transfer_data['wallets_operation_create_mock_data'])
    ), patch(
        'src.billing_operations.generate_transaction_number',
        return_value=create_transfer_data['generate_transaction_number_mock_data']
    ):
        result = await make_transfer(**create_transfer_data['params'])

    assert result == create_transfer_data['result']


@pytest.mark.asyncio
async def test_make_transfer_wallet_not_found(db_connect, create_transfer_data):
    with patch(
        'src.models.Transaction.create',
        new=CoroutineMock(return_value=create_transfer_data['transaction_create_mock_data'])
    ), patch(
        'src.models.Wallet.change_balance',
        new=CoroutineMock(side_effect=WalletNotFound(create_transfer_data['params']['wallet_to_id']))
    ):
        with pytest.raises(WalletNotFound) as exc_info:
            await make_transfer(**create_transfer_data['params'])
        assert exc_info.value.message == create_transfer_data['error_message_wallet_to_not_found']


@pytest.mark.asyncio
async def test_make_transfer_not_enough_balance(db_connect, create_transfer_data):
    with patch(
        'src.models.Transaction.create',
        new=CoroutineMock(return_value=create_transfer_data['transaction_create_mock_data'])
    ), patch(
        'src.models.Wallet.change_balance',
        new=CoroutineMock(side_effect=NotEnoughBalance(create_transfer_data['params']['wallet_from_id']))
    ):
        with pytest.raises(NotEnoughBalance) as exc_info:
            await make_transfer(**create_transfer_data['params'])
        assert exc_info.value.message == create_transfer_data['error_message_not_enough_balance']
