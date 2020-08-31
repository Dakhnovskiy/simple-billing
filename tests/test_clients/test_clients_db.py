from decimal import Decimal

import pytest

from src.app.db import db
from src.exceptions import ClientLoginAlreadyExists
from src.models import clients, create_client_and_wallet_in_db, wallets
from tests.test_clients.fixtures_clients import create_client_with_wallet_data


@pytest.mark.asyncio
async def test_create_client_and_wallet_in_db(db_connect, create_client_with_wallet_data):
    client_data = await create_client_and_wallet_in_db(**create_client_with_wallet_data['params'])

    query = clients.select().where(clients.c.id == client_data['id'])
    client_from_db = await db.fetch_one(query)

    assert client_from_db is not None
    assert client_from_db['login'] == create_client_with_wallet_data['params']['login']
    assert client_from_db['name'] == create_client_with_wallet_data['params']['name']

    query = wallets.select().where(wallets.c.id == client_data['wallet_id'])
    wallet_from_db = await db.fetch_one(query)

    assert wallet_from_db is not None
    assert wallet_from_db['client_id'] == client_data['id']
    assert wallet_from_db['balance'] == Decimal(0)


@pytest.mark.asyncio
async def test_create_client_and_wallet_in_db_already_exists(db_connect, create_client_with_wallet_data):
    await create_client_and_wallet_in_db(**create_client_with_wallet_data['params'])
    with pytest.raises(ClientLoginAlreadyExists) as exc_info:
        await create_client_and_wallet_in_db(**create_client_with_wallet_data['params'])
    assert exc_info.value.message == create_client_with_wallet_data['error_message']
