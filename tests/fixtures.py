from decimal import Decimal

import pytest

from src.app.db import db
from src.models import clients, wallets, wallets_operations, transactions


@pytest.fixture()
async def create_clients_and_wallets_in_db():
    first_client_data = {'login': 'client1', 'name': 'name1', 'balance': Decimal('123.123')}
    second_client_data = {'login': 'client2', 'name': 'name2', 'balance': Decimal('1000.2233')}

    for data in (first_client_data, second_client_data):
        query = clients.insert().values(login=data['login'], name=data['name'])
        client_id = await db.execute(query)
        query = wallets.insert().values(client_id=client_id, balance=data['balance'])
        wallet_id = await db.execute(query)
        data['wallet_id'] = wallet_id

    yield first_client_data, second_client_data

    await db.execute(wallets_operations.delete())
    await db.execute(transactions.delete())
    await db.execute(wallets.delete())
    await db.execute(clients.delete())
