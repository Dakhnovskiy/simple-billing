from src.models import create_client_and_wallet_in_db


async def create_client_with_wallet(login: str, name: str) -> dict:
    """
    Create client and wallet
    :param login: client login
    :param name: client name
    :return: client info
    """
    return await create_client_and_wallet_in_db(login, name)
