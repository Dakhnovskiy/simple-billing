from decimal import Decimal

import pytest

from src.app.db import db
from src.exceptions import WalletNotFound
from src.models import transactions, wallets_operations, make_resupply_in_db
from tests.fixtures import create_clients_and_wallets_in_db
from tests.test_resupplies.fixtures_resupplies import create_resupply_data


@pytest.mark.asyncio
async def test_make_resupply_in_db(db_connect, create_clients_and_wallets_in_db):
    transaction_number = '39ba4a9b-aa0c-4e81-a134-60271ebb49ed'
    amount = Decimal('222.227')

    client_data = create_clients_and_wallets_in_db[0]

    resupply_info = await make_resupply_in_db(
        transaction_number,
        client_data['wallet_id'],
        amount
    )

    assert resupply_info['wallet_balance'] == Decimal('345.35')

    query = transactions.select().where(transactions.c.number == transaction_number)
    transaction = await db.fetch_one(query)
    assert transaction is not None

    query = wallets_operations.select().where(wallets_operations.c.transaction_id == transaction['id'])
    wallets_operation_list = await db.fetch_all(query)
    assert len(wallets_operation_list) == 1
    assert wallets_operation_list[0]['amount'] == amount


@pytest.mark.asyncio
async def test_make_resupply_in_db_wallet_not_found(db_connect, create_resupply_data):
    transaction_number = '39ba4a9b-aa0c-4e81-a134-60271ebb49ed'

    with pytest.raises(WalletNotFound) as exc_info:
        await make_resupply_in_db(transaction_number=transaction_number, **create_resupply_data['params'])
    assert exc_info.value.message == create_resupply_data['error_message']

    query = transactions.select().where(transactions.c.number == transaction_number)
    transaction = await db.fetch_one(query)
    assert transaction is None
