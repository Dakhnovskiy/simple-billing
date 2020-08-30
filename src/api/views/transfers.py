from fastapi import APIRouter

from src.api.views.serializers import TransferCreateRequest, TransferCreateResponse
from src.billing_operations import make_transfer

transfers_views = APIRouter()


@transfers_views.post('/transfers', response_model=TransferCreateResponse, status_code=201)
async def make_transfer_handler(
        transfer: TransferCreateRequest
):
    transfer_data = await make_transfer(transfer.wallet_from_id, transfer.wallet_to_id, transfer.amount)
    return transfer_data
