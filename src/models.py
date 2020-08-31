from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from asyncpg import UniqueViolationError, CheckViolationError
from sqlalchemy import CheckConstraint

from src.app.db import metadata, db
from src.exceptions import ClientLoginAlreadyExists, WalletNotFound, NotEnoughBalance

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
        try:
            client_id = await db.execute(query)
        except UniqueViolationError as exc:
            if 'clients_login_key' in exc.message:
                raise ClientLoginAlreadyExists() from exc
            raise
        return client_id


class Wallet:
    @classmethod
    async def create(cls, client_id: int, balance: Decimal) -> int:
        query = wallets.insert().values(client_id=client_id, balance=balance)
        wallet_id = await db.execute(query)
        return wallet_id

    @classmethod
    async def change_balance(cls, wallet_id: int, amount: Decimal) -> Decimal:
        query = wallets.update().values(balance=wallets.c.balance + amount).where(wallets.c.id == wallet_id).returning(
            wallets.c.balance
        )

        try:
            balance = await db.execute(query)
        except CheckViolationError as exc:
            if 'check_positive_balance' in exc.message:
                raise NotEnoughBalance(wallet_id) from exc
            raise

        if balance is None:
            raise WalletNotFound(wallet_id)
        return balance


class Transaction:
    @classmethod
    async def create(cls, number: str) -> int:
        query = transactions.insert().values(number=number)
        transaction_id = await db.execute(query)
        return transaction_id


class WalletsOperation:
    @classmethod
    async def create(cls, wallet_id: int, transaction_id: int, amount: Decimal) -> int:
        query = wallets_operations.insert().values(wallet_id=wallet_id, transaction_id=transaction_id, amount=amount)
        wallets_operation_id = await db.execute(query)
        return wallets_operation_id


@db.transaction()
async def create_client_and_wallet_in_db(login: str, name: str) -> dict:
    """
    Create client and wallet in database
    :param login: client login
    :param name: client name
    :return: crated client info
    """

    client_id = await Client.create(login, name)
    wallet_id = await Wallet.create(client_id, Decimal('0'))

    return {
        'id': client_id,
        'login': login,
        'name': name,
        'wallet_id': wallet_id
    }


@db.transaction()
async def make_resupply_in_db(transaction_number: str, wallet_id: int, amount: Decimal) -> dict:
    """
    Replenish wallets balance in database
    :param transaction_number: transaction number
    :param wallet_id: wallet identifier
    :param amount: amount
    :return: resupply info
    """

    transaction_id = await Transaction.create(transaction_number)
    new_balance = await Wallet.change_balance(wallet_id, amount)
    await WalletsOperation.create(wallet_id, transaction_id, amount)

    return {
        'wallet_id': wallet_id,
        'amount': amount,
        'wallet_balance': new_balance,
        'transaction_number': transaction_number
    }


@db.transaction()
async def make_transfer_in_db(transaction_number: str, wallet_from_id: int, wallet_to_id: int, amount: Decimal) -> dict:
    """
    Transfer funds from one wallet to another in database
    :param transaction_number: transaction number
    :param wallet_from_id: wallet(from) identifier
    :param wallet_to_id: wallet(to) identifier
    :param amount: amount
    :return: transfer info
    """

    transaction_id = await Transaction.create(transaction_number)
    new_balance_wallet_from = await Wallet.change_balance(wallet_from_id, -amount)
    new_balance_wallet_to = await Wallet.change_balance(wallet_to_id, amount)
    await WalletsOperation.create(wallet_from_id, transaction_id, -amount)
    await WalletsOperation.create(wallet_to_id, transaction_id, amount)

    return {
        'wallet_from_id': wallet_from_id,
        'wallet_to_id': wallet_to_id,
        'amount': amount,
        'transaction_number': transaction_number,
        'wallet_from_balance': new_balance_wallet_from,
        'wallet_to_balance': new_balance_wallet_to,
    }
