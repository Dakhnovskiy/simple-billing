from decimal import Decimal

import pytest

from src.app.db import db
from src.exceptions import WalletNotFound, NotEnoughBalance
from src.models import transactions, wallets_operations, make_transfer_in_db
from tests.fixtures import create_clients_and_wallets_in_db
from tests.test_transfers.fixtures_transfers import create_transfer_data


@pytest.mark.asyncio
async def test_make_transfer_in_db(db_connect, create_clients_and_wallets_in_db):
    transaction_number = '39ba4a9b-aa0c-4e81-a134-60271ebb49ed'
    amount = Decimal('10.227')

    client_data_from, client_data_to = create_clients_and_wallets_in_db

    transfer_info = await make_transfer_in_db(
        transaction_number,
        client_data_from['wallet_id'],
        client_data_to['wallet_id'],
        amount
    )

    assert transfer_info['wallet_from_balance'] == Decimal('112.896')
    assert transfer_info['wallet_to_balance'] == Decimal('1010.4503')

    query = transactions.select().where(transactions.c.number == transaction_number)
    transaction = await db.fetch_one(query)
    assert transaction is not None

    query = wallets_operations.select().where(wallets_operations.c.transaction_id == transaction['id'])
    wallets_operation_list = await db.fetch_all(query)
    assert len(wallets_operation_list) == 2

    query = wallets_operations.select().where(
        wallets_operations.c.transaction_id == transaction['id'] and
        wallets_operations.c.wallet_id == client_data_from['wallet_id']
    )
    wallets_operation = await db.fetch_one(query)
    assert wallets_operation['amount'] == -amount

    query = wallets_operations.select().where(
        wallets_operations.c.transaction_id == transaction['id'] and
        wallets_operations.c.wallet_id == client_data_to['wallet_id']
    )
    wallets_operation = await db.fetch_one(query)
    assert wallets_operation['amount'] == -amount


@pytest.mark.asyncio
async def test_make_transfer_in_db_wallet_not_found(db_connect, create_transfer_data):
    transaction_number = '39ba4a9b-aa0c-4e81-a134-60271ebb49ed'

    with pytest.raises(WalletNotFound) as exc_info:
        await make_transfer_in_db(transaction_number=transaction_number, **create_transfer_data['params'])
    assert exc_info.value.message == create_transfer_data['error_message_wallet_from_not_found']

    query = transactions.select().where(transactions.c.number == transaction_number)
    transaction = await db.fetch_one(query)
    assert transaction is None


@pytest.mark.asyncio
async def test_make_transfer_in_db_not_enough_balance(db_connect, create_clients_and_wallets_in_db):

    amount = Decimal('1001.227')
    client_data_from, client_data_to = create_clients_and_wallets_in_db
    transaction_number = '39ba4a9b-aa0c-4e81-a134-60271ebb49ed'

    with pytest.raises(NotEnoughBalance):
        await make_transfer_in_db(
            transaction_number,
            client_data_from['wallet_id'],
            client_data_to['wallet_id'],
            amount
        )

    query = transactions.select().where(transactions.c.number == transaction_number)
    transaction = await db.fetch_one(query)
    assert transaction is None
