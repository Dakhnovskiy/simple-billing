import pytest
from httpx import AsyncClient

from src.app.app import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
