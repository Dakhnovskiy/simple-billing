from fastapi import APIRouter

from src.api.views.serializers import TransferCreateRequest, TransferCreateResponse

transfers_views = APIRouter()


@transfers_views.post('/transfers', response_model=TransferCreateResponse, status_code=201)
async def create_transfer(
        transfer: TransferCreateRequest
):
    return {}
