from fastapi import APIRouter


clients_views = APIRouter()


@clients_views.post('/clients', response_model=None, status_code=201)
async def create_client():
    return {}
