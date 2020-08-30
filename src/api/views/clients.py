from fastapi import APIRouter

from src.api.views.serializers import ClientCreateRequest, ClientCreateResponse
from src.clients import create_client_with_wallet

clients_views = APIRouter()


@clients_views.post('/clients', response_model=ClientCreateResponse, status_code=201)
async def create_client_handler(
        client: ClientCreateRequest
):
    client_data = await create_client_with_wallet(client.login, client.name)

    return client_data
