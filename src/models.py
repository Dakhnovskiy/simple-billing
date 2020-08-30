from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from asyncpg import UniqueViolationError
from sqlalchemy import CheckConstraint

from src.app.db import metadata, db


clients = sa.Table(
    'clients',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('login', sa.String(256), unique=True, nullable=False),
    sa.Column('name', sa.String(256), nullable=False),
)

wallets = sa.Table(
    'wallets',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('client_id', sa.BigInteger, sa.ForeignKey('clients.id'), nullable=False),
    sa.Column('balance', sa.Numeric, nullable=False),
    CheckConstraint('balance >= 0', name='check_positive_balance')
)

transactions = sa.Table(
    'transactions',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('number', sa.String(36), nullable=False),
)

wallets_operations = sa.Table(
    'wallets_operations',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('wallet_id', sa.BigInteger, sa.ForeignKey('wallets.id'), nullable=False),
    sa.Column('transaction_id', sa.BigInteger, sa.ForeignKey('transactions.id'), nullable=False),
    sa.Column('amount', sa.Numeric, nullable=False),
    sa.Column('operation_date', sa.DateTime(), nullable=True, default=datetime.utcnow),
)


class Client:
    @classmethod
    async def create(cls, login: str, name: str) -> int:
        query = clients.insert().values(login=login, name=name)
        client_id = await db.execute(query)
        return client_id


class Wallet:
    @classmethod
    async def create(cls, client_id: int, balance: Decimal) -> int:
        query = wallets.insert().values(client_id=client_id, balance=balance)
        wallet_id = await db.execute(query)
        return wallet_id


@db.transaction()
async def create_client_and_wallet_in_db(login: str, name: str):
    """
    Create client and wallet in database
    :param login: client login
    :param name: client name
    :return: crated client info
    """

    try:
        client_id = await Client.create(login, name)
        wallet_id = await Wallet.create(client_id, Decimal(0))
    except UniqueViolationError as exc:
        raise
    return {
        'id': client_id,
        'login': login,
        'name': name,
        'wallet_id': wallet_id
    }
