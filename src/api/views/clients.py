from fastapi import APIRouter

from src.api.views.serializers import ClientCreate, ClientInfo
from src.clients import create_client_with_wallet

clients_views = APIRouter()


@clients_views.post('/clients', response_model=ClientInfo, status_code=201)
async def create_client(
        client: ClientCreate
):
    client_data = await create_client_with_wallet(client.login, client.name)

    return client_data
