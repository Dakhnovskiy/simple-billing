from decimal import Decimal


async def make_resupply(wallet_id: int, amount: Decimal) -> dict:
    """
    Replenish wallets balance
    :param wallet_id: wallet identifier
    :param amount: amount
    :return: resupply info
    """
    return {}


async def make_transfer(wallet_from_id: int, wallet_to_id: int, amount: Decimal) -> dict:
    """
    Transfer funds from one wallet to another
    :param wallet_from_id: wallet(from) identifier
    :param wallet_to_id: wallet(to) identifier
    :param amount: amount
    :return: transfer info
    """
    return {}
