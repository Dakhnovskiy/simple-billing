from fastapi import APIRouter

from src.api.views.serializers import ClientCreate, ClientInfo

clients_views = APIRouter()


@clients_views.post('/clients', response_model=ClientInfo, status_code=201)
async def create_client(
        client: ClientCreate
):
    return {
        'login': 'aa',
        'name': 'qq',
        'wallet_id': 123,
        'id': 12
    }
