import uuid
from decimal import Decimal

from src.models import make_resupply_in_db


async def make_resupply(wallet_id: int, amount: Decimal) -> dict:
    """
    Replenish wallets balance
    :param wallet_id: wallet identifier
    :param amount: amount
    :return: resupply info
    """
    transaction_number = str(uuid.uuid4())
    return await make_resupply_in_db(transaction_number, wallet_id, amount)


async def make_transfer(wallet_from_id: int, wallet_to_id: int, amount: Decimal) -> dict:
    """
    Transfer funds from one wallet to another
    :param wallet_from_id: wallet(from) identifier
    :param wallet_to_id: wallet(to) identifier
    :param amount: amount
    :return: transfer info
    """
    return {}
