from fastapi import APIRouter

from src.api.views.serializers import ResupplyCreateRequest, ResupplyCreateResponse

resupplies_views = APIRouter()


@resupplies_views.post('/resupplies', response_model=ResupplyCreateRequest, status_code=201)
async def create_resupply(
        resupply: ResupplyCreateResponse
):
    return {}
