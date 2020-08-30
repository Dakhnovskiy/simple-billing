from fastapi import APIRouter

from src.api.views.serializers import ResupplyCreateRequest, ResupplyCreateResponse
from src.billing_operations import make_resupply

resupplies_views = APIRouter()


@resupplies_views.post('/resupplies', response_model=ResupplyCreateResponse, status_code=201)
async def make_resupply_handler(
        resupply: ResupplyCreateRequest
):
    resupply_data = await make_resupply(resupply.wallet_id, resupply.amount)
    return resupply_data
